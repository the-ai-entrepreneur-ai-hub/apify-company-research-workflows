# Company research through Apify's hosted MCP server

Connect an MCP client to Apify, then request company research using the explicit actor ID `george.the.developer/linkedin-company-by-domain`. Actor execution uses your Apify account and can incur charges.

## Connect

Server URL:

```text
https://mcp.apify.com?tools=call-actor,get-actor-run,get-dataset-items
```

- **Cursor:** merge [the supplied configuration](../mcp/cursor-company-research.json) into your project's `.cursor/mcp.json` or your user-level `~/.cursor/mcp.json`. Keep existing server entries. Connect and authorize your Apify account through OAuth.
- **Remote connector clients:** add a custom remote MCP connector using the URL above, then authorize your Apify account. Follow [the connector instructions](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) for your account's available setup route.

The configuration contains no token. This connection uses Apify's shared hosted service. The generic runner accepts other actor IDs too; the request below explicitly selects the company resolver. The returned tool list also includes key-value-store retrieval and run abortion helpers.

## Run the three-domain example

Use [company-domain-run.json](../mcp/company-domain-run.json) as the arguments to `call-actor`. The run configuration belongs in `callOptions`:

```json
{
  "maxTotalChargeUsd": 0.1,
  "memory": 512,
  "timeout": 900
}
```

These values apply to that call. The connection configuration does not impose spending limits on future requests. The example bounds input to three domains and gives the resolver working time before its final three-minute reserve. The charge cap does not guarantee that every domain resolves.

After starting once:

1. Save the returned run ID. Call `get-actor-run` with that `runId` and `waitSecs:0`; wait approximately 15 seconds between checks until `SUCCEEDED`. Stop polling after 17 minutes and inspect the existing run before starting another.
2. On `FAILED`, `ABORTED` or `TIMED-OUT`, report the status and inspect the existing run. An ambiguous start response needs inspection before another start.
3. Retrieve results with `get-dataset-items`, passing the successful run's `storages.datasets.default.id` as `datasetId`, plus `clean:true` and `limit:1000`.
4. Inspect `confidence`, `linkedinUrl` and any `qualityState`. Keep unresolved rows visible. MCP retrieval does not add the n8n workflow's `needsReview` flag or independently verify company identity.

## Verification scope

On October 7, 2026, authenticated metadata probes returned HTTP 200 for initialization and tool listing, and HTTP 202 for the initialized notification. Both the actor-selected endpoint and this generic-runner endpoint were checked. The live `call-actor` schema exposes `actor`, `input`, `waitSecs` and `callOptions`; the example was validated against that returned schema.

No actor execution was requested. OAuth completion inside Cursor/Claude, client UI behavior, live resolution, customer acquisition and profit remain unverified. This guide is available from the workflow repository; no third-party MCP directory submission is claimed.

References: [Apify MCP server](https://docs.apify.com/integrations/mcp), [Cursor MCP configuration](https://cursor.com/docs/mcp).
