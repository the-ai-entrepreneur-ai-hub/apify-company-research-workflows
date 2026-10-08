import importlib.util
import io
import json
from pathlib import Path
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import Mock, patch
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit


SCRIPT = Path(__file__).resolve().parents[1] / 'windmill/company_domain_research.py'
TOKEN = 'synthetic-local-token'


class WindmillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def handle_request(self):
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length).decode() if length else None
                cls.requests.append((self.command, self.path, dict(self.headers), body))
                status, value, headers = cls.responses.pop(0) if cls.responses else (500, {}, {})
                payload = value if isinstance(value, bytes) else json.dumps(value).encode()
                self.send_response(status)
                for name, value in headers.items():
                    self.send_header(name, value)
                self.end_headers()
                self.wfile.write(payload)

            do_GET = handle_request
            do_POST = handle_request

        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.assertTrue(SCRIPT.exists(), 'The standalone connector must be supplied')
        spec = importlib.util.spec_from_file_location('company_domain_research', SCRIPT)
        self.connector = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.connector)
        self.assertEqual(self.connector.API_BASE, 'https://api.apify.com/v2')
        self.connector.API_BASE = f'http://127.0.0.1:{self.server.server_port}/v2'
        type(self).requests = []
        type(self).responses = []
        self.age = 0
        self.clock = patch.object(self.connector.time, 'monotonic', lambda: self.age)
        self.sleep = patch.object(self.connector.time, 'sleep', self.advance)
        self.clock.start()
        self.sleep.start()
        self.addCleanup(self.clock.stop)
        self.addCleanup(self.sleep.stop)

    def advance(self, seconds):
        self.age += seconds

    def queue(self, value, status=200, headers=None):
        self.responses.append((status, value, headers or {}))

    def run_data(self, status='RUNNING', **extra):
        return {'data': {'id': 'run123', 'status': status, **extra}}

    def invoke(self, domains=None, credentials=None):
        return self.connector.main(
            credentials if credentials is not None else {'api_key': TOKEN},
            domains if domains is not None else ['stripe.com'])

    def ready(self, rows):
        self.queue(self.run_data())
        self.queue(self.run_data('SUCCEEDED', defaultDatasetId='data123'))
        self.queue(rows)

    def test_one_capped_start_polls_then_reads_rows(self):
        self.queue(self.run_data())
        self.queue(self.run_data())
        self.queue(self.run_data('SUCCEEDED', defaultDatasetId='data123'))
        self.queue([{'domain': 'stripe.com', 'confidence': 'high',
                     'linkedinUrl': 'https://www.linkedin.com/company/stripe/'}])
        result = self.invoke(['https://www.STRIPE.com/pricing'])
        self.assertFalse(result['needsReview'])
        self.assertEqual(result['missingDomains'], [])
        self.assertEqual(result['runId'], 'run123')
        self.assertEqual([r[0] for r in self.requests], ['POST', 'GET', 'GET', 'GET'])
        self.assertEqual(self.age, 15)
        method, target, headers, body = self.requests[0]
        parsed = urlsplit(target)
        self.assertEqual(parsed.path, '/v2/acts/george.the.developer~linkedin-company-by-domain/runs')
        self.assertEqual(parse_qs(parsed.query), {
            'memory': ['512'], 'timeout': ['900'], 'maxTotalChargeUsd': ['0.1']})
        self.assertEqual(json.loads(body), {
            'domains': ['stripe.com'], 'maxDomains': 1,
            'mode': 'resolve', 'includeUnresolved': True})
        self.assertEqual(urlsplit(self.requests[1][1]).path, '/v2/actor-runs/run123')
        dataset = urlsplit(self.requests[-1][1])
        self.assertEqual(dataset.path, '/v2/datasets/data123/items')
        self.assertEqual(parse_qs(dataset.query), {'format': ['json'], 'clean': ['true'], 'limit': ['100']})
        for _, target, headers, _ in self.requests:
            self.assertEqual(headers['Authorization'], f'Bearer {TOKEN}')
            self.assertNotIn(TOKEN, target)

    def test_invalid_inputs_never_start_a_run(self):
        for domains in ([], ['a.com'] * 11, 'stripe.com', ['localhost'], ['127.0.0.1'],
                        ['https://user:pass@stripe.com'], ['https://stripe.com:443'],
                        ['bad domain.com'], ['stri\npe.com'], [None], ['ftp://stripe.com'], ['-bad.com']):
            with self.subTest(domains=domains), self.assertRaises(ValueError):
                self.invoke(domains)
        for credentials in ({}, {'api_key': ''}, {'api_key': 'bad\nheader'}, {'api_key': 1}):
            with self.subTest(credentials=credentials), self.assertRaises(ValueError):
                self.invoke(credentials=credentials)
        self.assertEqual(self.requests, [])

    def test_duplicates_are_normalized_before_start(self):
        self.ready([{'domain': 'stripe.com', 'confidence': 'low', 'linkedinUrl': None}])
        result = self.invoke(['stripe.com', 'https://www.stripe.com/'])
        self.assertEqual(json.loads(self.requests[0][3])['maxDomains'], 1)
        self.assertTrue(result['needsReview'])

    def test_unresolved_and_missing_domains_remain_visible(self):
        self.ready([{'domain': 'stripe.com', 'confidence': 'unresolved', 'linkedinUrl': None}])
        result = self.invoke(['stripe.com', 'gitlab.com'])
        self.assertEqual(len(result['rows']), 1)
        self.assertTrue(result['rows'][0]['needsReview'])
        self.assertEqual(result['missingDomains'], ['gitlab.com'])
        self.assertTrue(result['needsReview'])

    def test_misleading_linkedin_urls_require_review(self):
        for url in ('https://linkedin.com.evil.test/company/foo',
                    'https://www.linkedin.com/in/person', 'https://www.linkedin.com/company/'):
            with self.subTest(url=url):
                self.ready([{'domain': 'stripe.com', 'confidence': 'high', 'linkedinUrl': url}])
                self.assertTrue(self.invoke()['rows'][0]['needsReview'])

    def test_terminal_or_unknown_status_never_retrieves_dataset(self):
        for status in ('FAILED', 'ABORTED', 'TIMED-OUT', 'MYSTERY', None, [], {}):
            with self.subTest(status=status):
                self.requests.clear()
                self.queue(self.run_data())
                self.queue(self.run_data(status))
                with self.assertRaisesRegex(RuntimeError, 'run123'):
                    self.invoke()
                self.assertEqual([r[0] for r in self.requests], ['POST', 'GET'])

    def test_expired_polling_retains_run_id_and_never_restarts(self):
        self.queue(self.run_data())
        self.queue(self.run_data())
        with patch.object(self.connector.time, 'sleep', lambda seconds: self.advance(1021)):
            with self.assertRaisesRegex(RuntimeError, 'run123'):
                self.invoke()
        self.assertEqual([r[0] for r in self.requests], ['POST', 'GET'])

    def test_ambiguous_start_is_not_retried_or_exposed(self):
        self.queue({'secret': TOKEN}, status=500)
        with self.assertRaisesRegex(RuntimeError, 'Console') as error:
            self.invoke()
        self.assertNotIn(TOKEN, str(error.exception))
        self.assertEqual(len(self.requests), 1)
        error_body = io.BytesIO(b'private error payload')
        opener = Mock()
        opener.open.side_effect = HTTPError('http://localhost', 500, 'error', {}, error_body)
        with self.assertRaises(RuntimeError):
            self.connector._request(opener, TOKEN, '/actor-runs/run123')
        self.assertTrue(error_body.closed, 'HTTP error responses must be closed')

    def test_redirect_never_forwards_credentials(self):
        self.queue({}, status=307, headers={'Location': f'http://127.0.0.1:{self.server.server_port}/leak'})
        with self.assertRaises(RuntimeError):
            self.invoke()
        self.assertEqual(len(self.requests), 1)

    def test_malformed_start_requires_console_check(self):
        for response in (b'not json', {}, {'data': {'id': '../escape'}}, {'data': []}):
            with self.subTest(response=response):
                self.requests.clear()
                self.queue(response)
                with self.assertRaisesRegex(RuntimeError, 'Console'):
                    self.invoke()
                self.assertEqual(len(self.requests), 1)

    def test_success_without_valid_dataset_id_fails(self):
        for dataset_id in (None, '../escape', ''):
            with self.subTest(dataset_id=dataset_id):
                self.requests.clear()
                self.queue(self.run_data())
                self.queue(self.run_data('SUCCEEDED', defaultDatasetId=dataset_id))
                with self.assertRaisesRegex(RuntimeError, 'run123'):
                    self.invoke()
                self.assertEqual(len(self.requests), 2)

    def test_empty_or_malformed_dataset_is_rejected(self):
        for rows in ([], {}, [None], [{'domain': None}]):
            with self.subTest(rows=rows):
                self.ready(rows)
                with self.assertRaisesRegex(RuntimeError, 'run123'):
                    self.invoke()

    def test_actor_normalized_parent_domain_is_retained_for_review(self):
        self.ready([{'domain': 'stripe.com', 'confidence': 'high',
                     'linkedinUrl': 'https://www.linkedin.com/company/stripe/'}])
        result = self.invoke(['app.stripe.com'])
        self.assertEqual(result['rows'][0]['domain'], 'stripe.com')
        self.assertTrue(result['rows'][0]['needsReview'])
        self.assertEqual(result['missingDomains'], ['app.stripe.com'])
        self.assertTrue(result['needsReview'])


if __name__ == '__main__':
    unittest.main()
