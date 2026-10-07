import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import vm from 'node:vm';

const read = name => {
  const file = new URL(`../${name}`, import.meta.url);
  assert.ok(existsSync(file), `Missing published artifact: ${name}`);
  return JSON.parse(readFileSync(file, 'utf8'));
};
const workflow = () => read('workflows/company-domain-research.n8n.json');
const node = name => workflow().nodes.find(n => n.name === name);
const now = Date.parse('2026-10-07T12:00:00Z');
function execute(name, rows) {
  const $input = { first: () => ({ json: rows[0] }), all: () => rows.map(json => ({ json })) };
  const Clock = class extends Date { static now() { return now; } };
  return vm.runInNewContext(`(function () { ${node(name).parameters.jsCode}\n})()`, { $input, Date: Clock });
}
const run = (status, extra = {}) => ({ data: {
  id: 'synthetic-run', status, startedAt: '2026-10-07T11:59:30Z',
  defaultDatasetId: 'synthetic-dataset', ...extra,
} });

test('sample configuration uses three domains and limits the actor input', () => {
  const [item] = execute('Prepare domains', [{}]);
  assert.equal(item.json.domains.length, 3);
  assert.equal(item.json.maxDomains, 3);
  assert.equal(item.json.mode, 'resolve');
  assert.equal(item.json.includeUnresolved, true);
});

test('invalid input and overly large batches fail before paid execution', () => {
  for (const domains of [[], 'stripe.com', [null], [''], ['http://'], Array(11).fill('example.com')]) {
    assert.throws(() => execute('Prepare domains', [{ domains }]));
  }
  const [item] = execute('Prepare domains', [{ domains: ['https://www.example.com/about', 'example.org'] }]);
  assert.equal(item.json.maxDomains, 2);
});

test('only successful runs reach dataset retrieval', () => {
  assert.equal(execute('Route run', [run('SUCCEEDED')])[0].json.routeIndex, 0);
  for (const status of ['READY', 'RUNNING', 'ABORTING', 'TIMING-OUT']) {
    assert.equal(execute('Route run', [run(status)])[0].json.routeIndex, 1);
  }
});

test('terminal and unknown statuses fail visibly', () => {
  for (const status of ['FAILED', 'ABORTED', 'TIMED-OUT', 'UNKNOWN', undefined]) {
    assert.throws(() => execute('Route run', [run(status)]), /status|failed|FAILED|ABORTED|TIMED-OUT/i);
  }
});

test('malformed run responses and polling beyond seventeen minutes stop', () => {
  for (const payload of [{}, { data: {} }, run('RUNNING', { id: null }), run('RUNNING', { startedAt: 'bad' }), run('RUNNING', { startedAt: '2026-10-07T11:42:59Z' }), run('SUCCEEDED', { defaultDatasetId: null })]) {
    assert.throws(() => execute('Route run', [payload]));
  }
});

test('starter time limits allow resolution after the actor shutdown reserve', () => {
  // The actor reserves its final 180 seconds before starting any domain work.
  const reserveSeconds = 180;
  const startQuery = Object.fromEntries(node('Start actor').parameters.queryParameters.parameters.map(p => [p.name, p.value]));
  const collection = read('postman/company-domain-research.postman_collection.json');
  const postmanQuery = Object.fromEntries(collection.item[0].request.url.query.map(p => [p.key, p.value]));
  for (const query of [startQuery, postmanQuery]) {
    assert.ok(Number(query.timeout) >= reserveSeconds + Math.ceil(10 / 3) * 120, 'Allow the shutdown reserve and watchdog budget for the largest starter batch.');
  }
  assert.equal(Number(startQuery.timeout), Number(postmanQuery.timeout));
  const startedAt = new Date(now - Number(startQuery.timeout) * 1000).toISOString();
  assert.equal(execute('Route run', [run('RUNNING', { startedAt })])[0].json.routeIndex, 1, 'Polling must outlast the actor timeout.');
  assert.ok(workflow().settings.executionTimeout > Number(startQuery.timeout) + 120);
});

test('unresolved results are retained and marked for review', () => {
  const rows = [
    { domain: 'example.com', confidence: 'high', linkedinUrl: 'https://www.linkedin.com/company/example/', charged: true },
    { domain: 'example.org', confidence: 'low', linkedinUrl: null, charged: false },
    { domain: 'example.net', confidence: 'medium', linkedinUrl: 'https://unrelated.example/company/example/', charged: true },
  ];
  const result = execute('Review company rows', rows);
  assert.equal(result.length, 3);
  assert.equal(result[0].json.needsReview, false);
  assert.equal(result[1].json.needsReview, true);
  assert.equal(result[2].json.needsReview, true);
  assert.equal(result[1].json.domain, 'example.org');
});

test('empty or malformed datasets are not presented as useful company results', () => {
  assert.throws(() => execute('Review company rows', []));
  assert.throws(() => execute('Review company rows', [{}]));
});

test('workflow graph authenticates all HTTP calls and bounds spending without POST retries', () => {
  const w = workflow();
  const names = new Set(w.nodes.map(n => n.name));
  assert.equal(w.active, false);
  for (const [from, c] of Object.entries(w.connections)) {
    assert.ok(names.has(from));
    for (const branch of c.main) for (const edge of branch) assert.ok(names.has(edge.node));
  }
  for (const n of w.nodes.filter(n => n.type === 'n8n-nodes-base.httpRequest')) {
    assert.equal(n.parameters.authentication, 'genericCredentialType');
    assert.equal(n.parameters.genericAuthType, 'httpHeaderAuth');
    assert.equal(n.continueOnFail ?? false, false);
    assert.ok(n.parameters.options.timeout <= 60000);
    assert.equal(n.credentials, undefined);
  }
  const start = node('Start actor');
  const q = Object.fromEntries(start.parameters.queryParameters.parameters.map(p => [p.name, p.value]));
  assert.equal(start.parameters.method, 'POST');
  assert.equal(Number(q.maxTotalChargeUsd), 0.1);
  assert.equal(Number(q.timeout), 900);
  assert.equal(Number(q.memory), 512);
  assert.equal(start.retryOnFail ?? false, false);
  assert.equal(node('Wait before polling').parameters.amount, 15);
  assert.equal(node('Get company rows').alwaysOutputData, true);
  assert.equal(w.connections['Branch by run status'].main[0][0].node, 'Get company rows');
  assert.equal(w.connections['Branch by run status'].main[1][0].node, 'Wait before polling');
});

test('Postman uses bearer variables, async polling and no saved token', () => {
  const c = read('postman/company-domain-research.postman_collection.json');
  assert.equal(c.info.schema, 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json');
  assert.equal(c.auth.type, 'bearer');
  assert.equal(c.auth.bearer[0].value, '{{APIFY_TOKEN}}');
  assert.ok(c.variable.every(v => v.key !== 'APIFY_TOKEN' || v.value === ''));
  assert.equal(c.item.length, 3);
  assert.equal(c.item[0].request.method, 'POST');
  assert.match(c.item[0].request.url.raw, /maxTotalChargeUsd=0\.10/);
  assert.match(c.item[2].event.find(e => e.listen === 'prerequest').script.exec.join('\n'), /skipRequest/);
});

test('distribution JSON exports contain no real token or token query parameter', () => {
  for (const path of ['workflows/company-domain-research.n8n.json', 'postman/company-domain-research.postman_collection.json']) {
    const text = JSON.stringify(read(path));
    assert.doesNotMatch(text, /apify_api_[A-Za-z0-9]+|gh[pous]_[A-Za-z0-9]+|[?&]token=/);
  }
});

test('MCP client config uses the hosted OAuth connection without embedded credentials', () => {
  const config = read('mcp/cursor-company-research.json');
  const server = config.mcpServers['apify-company-research'];
  const endpoint = new URL(server.url);
  assert.equal(endpoint.origin, 'https://mcp.apify.com');
  assert.equal(endpoint.searchParams.get('tools'), 'call-actor,get-actor-run,get-dataset-items');
  assert.deepEqual(Object.keys(server), ['url']);
});

test('MCP example keeps actor execution limits in callOptions', () => {
  const request = read('mcp/company-domain-run.json');
  assert.equal(request.actor, 'george.the.developer/linkedin-company-by-domain');
  assert.equal(request.waitSecs, 0);
  assert.equal(request.input.domains.length, 3);
  assert.equal(request.input.maxDomains, 3);
  assert.equal(request.input.includeUnresolved, true);
  assert.deepEqual(request.callOptions, { maxTotalChargeUsd: 0.1, memory: 512, timeout: 900 });
  for (const key of Object.keys(request.callOptions)) assert.equal(request.input[key], undefined);
  for (const file of ['mcp/cursor-company-research.json', 'mcp/company-domain-run.json']) {
    assert.doesNotMatch(JSON.stringify(read(file)), /apify_api_[A-Za-z0-9]+|[?&]token=|Bearer /);
  }
});
