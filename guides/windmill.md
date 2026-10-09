# Company domain research with Windmill and Apify

Use the [Python script](../windmill/company_domain_research.py) to turn a small domain list into company research records with [LinkedIn Company by Domain](https://apify.com/george.the.developer/linkedin-company-by-domain). Bring your own Apify account. Windmill usage and Apify charges are separate.

## Set up a private script

1. Create a Python script in your Windmill workspace and paste the downloaded script. It uses Python 3.10 or newer and standard-library modules only.
2. In **Resources > New Resource**, select **apify_api_key** and save your private Apify token in its **api_key** field. Select that resource for the script's **credentials** argument. Follow [Apify's Windmill resource instructions](https://docs.apify.com/integrations/windmill); do not paste a token into source or publish an exported resource value.
3. In script **Settings**, under **Runtime > Timeout**, set a custom timeout of 20 minutes (1200 seconds). Your instance must permit that duration. See [Windmill's settings documentation](https://www.windmill.dev/docs/script_editor/settings).
4. Set **domains** to the following example. The script accepts 1–10 entries, normalizes HTTP(S) URLs and removes duplicate domains.

```json
["stripe.com", "vercel.com", "gitlab.com"]
```

5. Check the actor's current pricing and run deliberately. Keep automatic retries and perpetual execution disabled. If used as a flow step, also disable flow retries for this step. Each new invocation can create a new paid actor run; the cap is per invocation.
6. Inspect **rows**, **missingDomains** and **needsReview** before exporting or connecting a destination. Keep the script private to authorized users of your account.

The `apify_api_key` TypedDict follows [Windmill's resource-type convention](https://www.windmill.dev/docs/core_concepts/resources_and_types). The resource is resolved by your workspace; no credentials are supplied by this pack.

## Execution and output

The script starts exactly one asynchronous run with 512 MB memory, a 900-second actor timeout and a **$0.10 maximum actor charge**. It polls the same run every 15 seconds for up to 17 minutes, then retrieves the dataset only after **SUCCEEDED**. HTTP requests have a 30-second timeout. Polling expiry or a transport failure stops the script and identifies the existing run when known; it does not abort that run. Inspect Apify Console before rerunning after an ambiguous start error.

The actor's final three-minute reserve means it needs the supplied 15-minute timeout to have useful working time. A charge cap or time limit may leave domains missing or unresolved. This script retrieves up to 100 rows for at most ten requested domains.

The returned object contains:

| Field | Meaning |
|---|---|
| `runId`, `datasetId` | Existing Apify objects for inspection; not new executions |
| `rows` | Company records, retaining unresolved rows and adding `needsReview` |
| `missingDomains` | Requested domains without an exact normalized host match in the returned dataset |
| `needsReview` | True if any row needs review or a domain is missing |

A row needs review unless its domain matches a requested host, confidence is `high` and its LinkedIn URL has a plausible company path on linkedin.com. The actor can normalize a subdomain to its parent domain: a request for `app.stripe.com` may return `stripe.com`. That row is retained for review and `app.stripe.com` remains in `missingDomains`; no parent-domain identity is assumed. This screens returned fields; it does not independently verify identity or guarantee correctness. Empty or malformed datasets and failed runs produce visible errors. The actor returns company research, not individual employee profiles or email addresses.

## Verification and Hub status

Thirteen Python tests execute the script against a local HTTP server with synthetic credentials. They cover the single-start request and charge cap, polling, invalid inputs, malformed responses, failure/expiry, redirect refusal, unresolved rows and missing-domain/parent-domain review. Run locally with:

```text
python -B -m unittest discover -s test -p test_windmill.py -v
```

These checks do not establish execution inside Windmill, a completed workspace connection or live actor resolution. No paid actor run was started for this publication.

This script was submitted to Windmill Hub on October 9, 2026: [Research company domains with Apify and review unresolved matches](https://hub.windmill.dev/scripts/apify/22820/research-company-domains-with-apify-and-review-unresolved-matches-apify). An anonymous HTTP read verified that its public source, summary and description match the reviewed pack. The page's approval fields are empty, so **moderator approval and placement in the [Apify integration catalog](https://hub.windmill.dev/integrations/apify) remain unverified**. See the [dated submission evidence](../verification/windmill-hub.json). Native execution, live actor resolution, customer adoption and revenue remain unmeasured. Follow [Windmill's Hub review process](https://www.windmill.dev/docs/misc/share_on_hub) before treating submission as approval.

Maintained by the developer of the linked actor. This pack is not endorsed by Windmill.
