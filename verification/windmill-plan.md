# Windmill company research connector plan

October 8, 2026. Publish a customer-owned Python script and setup guide in this workflow pack. Native Hub submission requires login and moderator review; neither is established by publishing these files.

## Changes

- Add `windmill/company_domain_research.py`: standard-library Python, an `apify_api_key` resource, one capped asynchronous actor start, bounded polling, and explicit review of returned company rows and missing domains.
- Add `test/test_windmill.py`: local HTTP fixtures and synthetic credentials; observe failures before implementing the connector.
- Add `guides/windmill.md`, link it from README and record submission scope in SUBMISSIONS.
- Add the Python checks to the existing validation workflow. Expected change: approximately 450 lines including fixtures and documentation.

## Risks and checks

Actor execution can incur charges. Start requests must never retry automatically. Validate all inputs before starting; use a fixed API host, reject redirects and suppress raw error bodies. A $0.10 maximum actor charge does not guarantee full domain coverage. Polling expiry must retain the run ID and never start another run. Review flags screen fields rather than verify identity.

Run the existing Node suite, Python HTTP contract tests, whitespace and publication gates, then obtain fresh independent review. No live actor run or Windmill account execution is part of this check. Verify published downloads and the rendered guide after GitHub validation and Pages deployment.

## Rollback

Revert the connector publication commit. No actor deployment, account connection, schedule or public execution endpoint is created.
