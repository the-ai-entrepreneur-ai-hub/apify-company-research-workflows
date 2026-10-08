"""Company research for Windmill; uses the caller's Apify resource."""

import ipaddress
import json
import re
import time
from typing import TypedDict
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

API_BASE = 'https://api.apify.com/v2'
ACTIVE = {'READY', 'RUNNING', 'ABORTING', 'TIMING-OUT'}
TERMINAL = {'SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT'}


class apify_api_key(TypedDict):
    api_key: str


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _domain(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Each domain must be a nonempty domain or HTTP(S) URL.')
    value = value.strip()
    if any(char.isspace() or ord(char) < 32 for char in value):
        raise ValueError('Domains and URLs cannot contain whitespace or control characters.')
    try:
        parsed = urlsplit(value if '://' in value else 'https://' + value)
        if (parsed.scheme not in ('http', 'https') or parsed.username is not None
                or parsed.password is not None or parsed.port is not None):
            raise ValueError()
        host = (parsed.hostname or '').encode('idna').decode('ascii').lower()
        if host.startswith('www.'):
            host = host[4:]
        try:
            ipaddress.ip_address(host)
        except ValueError:
            pass
        else:
            raise ValueError()
        labels = host.split('.')
        if (len(host) > 253 or len(labels) < 2 or labels[-1].isdigit()
                or any(not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', label)
                       for label in labels)):
            raise ValueError()
        return host
    except (ValueError, UnicodeError):
        raise ValueError('Each domain must be a public domain without credentials or a port.') from None


def _id(value):
    return isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9]{1,64}', value) is not None


def _linkedin(value):
    if not isinstance(value, str):
        return False
    try:
        url = urlsplit(value)
        return (url.scheme == 'https' and url.hostname in ('linkedin.com', 'www.linkedin.com')
                and url.username is None and url.password is None and url.port is None
                and re.fullmatch(r'/company/[^/\s]+/?', url.path) is not None)
    except ValueError:
        return False


def _request(opener, token, path, body=None):
    request = Request(API_BASE + path, data=json.dumps(body).encode() if body is not None else None,
                      headers={'Authorization': 'Bearer ' + token,
                               'Content-Type': 'application/json',
                               'x-apify-integration-platform': 'windmill'})
    try:
        with opener.open(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        error.close()
        raise RuntimeError('Apify request failed.') from None
    except (URLError, OSError, ValueError):
        raise RuntimeError('Apify request failed or returned invalid JSON.') from None


def _run(response):
    data = response.get('data') if isinstance(response, dict) else None
    if (not isinstance(data, dict) or not _id(data.get('id'))
            or not isinstance(data.get('status'), str)
            or data.get('status') not in ACTIVE | TERMINAL):
        raise RuntimeError('Invalid actor run response.')
    return data


def main(credentials: apify_api_key, domains: list[str]) -> dict:
    """Start once, poll the same run, and return company rows plus review flags."""
    token = credentials.get('api_key') if isinstance(credentials, dict) else None
    if not isinstance(token, str) or not token or any(ord(c) < 33 or ord(c) > 126 for c in token):
        raise ValueError('Select your own apify_api_key resource with a valid api_key.')
    if not isinstance(domains, list) or not 1 <= len(domains) <= 10:
        raise ValueError('Supply between 1 and 10 domains.')
    requested = list(dict.fromkeys(_domain(value) for value in domains))
    opener = build_opener(_NoRedirect())
    try:
        run = _run(_request(opener, token,
            '/acts/george.the.developer~linkedin-company-by-domain/runs'
            '?memory=512&timeout=900&maxTotalChargeUsd=0.1',
            {'domains': requested, 'maxDomains': len(requested),
             'mode': 'resolve', 'includeUnresolved': True}))
    except RuntimeError:
        raise RuntimeError('Start was not confirmed. Inspect Apify Console before retrying; '
                           'a paid run may already exist.') from None
    run_id = run['id']
    try:
        deadline = time.monotonic() + 17 * 60
        while run['status'] in ACTIVE:
            if time.monotonic() >= deadline:
                raise RuntimeError('Polling expired; inspect the existing run in Console.')
            run = _run(_request(opener, token, '/actor-runs/' + run_id))
            if run['id'] != run_id:
                raise RuntimeError('Run response changed its ID.')
            if run['status'] in ACTIVE:
                time.sleep(15)
        if run['status'] != 'SUCCEEDED':
            raise RuntimeError('Actor ended with status ' + run['status'] + '.')
        dataset_id = run.get('defaultDatasetId')
        if not _id(dataset_id):
            raise RuntimeError('Successful run has no valid dataset ID.')
        rows = _request(opener, token, '/datasets/' + dataset_id + '/items?format=json&clean=true&limit=100')
        if not isinstance(rows, list) or not rows:
            raise RuntimeError('Dataset is empty or malformed.')
        reviewed = []
        covered = set()
        for row in rows:
            if not isinstance(row, dict):
                raise RuntimeError('Dataset contains a malformed row.')
            try:
                domain = _domain(row.get('domain'))
            except ValueError:
                raise RuntimeError('Dataset row has no valid domain.') from None
            covered.add(domain)
            reviewed.append({**row, 'needsReview': domain not in requested or row.get('confidence') != 'high'
                             or not _linkedin(row.get('linkedinUrl'))})
        missing = [domain for domain in requested if domain not in covered]
        return {'runId': run_id, 'datasetId': dataset_id, 'rows': reviewed,
                'missingDomains': missing,
                'needsReview': bool(missing) or any(row['needsReview'] for row in reviewed)}
    except RuntimeError as error:
        raise RuntimeError(f'Run {run_id}: {error}') from None
