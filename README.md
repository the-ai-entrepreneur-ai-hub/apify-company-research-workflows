# Company domain research workflows for Apify

Turn a list of company website domains into LinkedIn company research records. Includes an n8n workflow, a Postman collection, MCP connection examples, and setup guides for Clay and Make.

Uses [LinkedIn Company by Domain](https://apify.com/george.the.developer/linkedin-company-by-domain). Connect your own Apify account; actor usage is billed there. The workflow files are free under the MIT license.

## Download

- [Apify starter task](https://apify.com/george.the.developer/linkedin-company-by-domain/examples/company-domain-research-starter) — a public three-domain configuration; copy and edit it before running.
- [n8n workflow JSON](workflows/company-domain-research.n8n.json)
- [Postman collection JSON](postman/company-domain-research.postman_collection.json)
- [Remote MCP client setup](guides/mcp.md) with a capped actor-call example
- [AI agent discovery guide](guides/agentic-discovery.md) and [dated eligible catalog](verification/agentic-discovery.json)
- [Clay setup guide](guides/clay.md)
- [Make setup guide](guides/make.md)

## What the n8n workflow does

1. Accepts between 1 and 10 website domains; the sample uses Stripe, Vercel and GitLab.
2. Starts one actor run with a $0.10 maximum actor charge, 512 MB memory and a 900-second actor timeout.
3. Checks the run every 15 seconds, stopping on failure or after a 17-minute polling age limit. The workflow execution limit is 20 minutes.
4. Retrieves the completed dataset and retains unresolved rows for review.
5. Marks records `needsReview` when confidence is low or a plausible LinkedIn company URL is missing.

The added review flag checks the returned fields; it does not independently verify company identity. Partial results can occur if the actor reaches its charge limit. Review domain coverage before using the data.

The actor reserves its final three minutes before starting new domains. The 15-minute actor timeout gives it working time before that reserve. Earlier exports used 120 seconds, which falls entirely inside the reserve and can produce only unresolved `time-budget` rows; replace those exports with this corrected version.

## Import into n8n

1. Download the workflow JSON above. In n8n, create a workflow and choose **Import from File**.
2. Create a **Header Auth** credential with header name `Authorization` and value `Bearer YOUR_APIFY_TOKEN`. Replace that example value with your private Apify token.
3. Select that credential on **Start actor**, **Get run status**, and **Get company rows**. No credentials are embedded in the exported workflow.
4. In **Prepare domains**, edit the sample domain list or connect an upstream node that supplies a `domains` array.
5. Check the actor's current pricing and execute manually. Running it may incur actor charges.
6. Inspect **Review company rows**. Export its results or connect a spreadsheet destination.

To append to Google Sheets, add a Google Sheets node after **Review company rows**, select your Google account and spreadsheet, and map `domain`, `companyName`, `linkedinUrl`, `confidence`, `employeeCount`, `followers` and `needsReview`. Google Sheets is configured by the user; no Google credential or destination is included in this pack.

The workflow uses built-in Manual Trigger, Code, HTTP Request, Switch and Wait nodes. It is inactive on import. Start requests are not automatically retried because a retry could create another paid run. If a start request fails ambiguously, inspect Apify Console before trying again.

## Use with Postman

1. Import the collection JSON.
2. Create a private environment variable named `APIFY_TOKEN` with your Apify token. Keep its value local and do not include it in public exports.
3. Send **1. Start one capped actor run** once.
4. Send **2. Poll run status until SUCCEEDED**. If the run is still active, wait 15 seconds and send request 2 again.
5. Send **3. Retrieve company research rows** after success. The collection saves the run and dataset IDs automatically.

The collection intentionally does not loop in Collection Runner. A runner may reach request 3 while the run is still pending, in which case retrieval is skipped. Polling an existing run does not create another run. These requests use asynchronous endpoints so a long extraction is not mistaken for an HTTP request timeout.

## Actor pricing and limits

The public Store snapshot on October 7, 2026 lists $0.0075 per `company-resolved` event and $0.002 per platform start event. Start-event quantity depends on memory; review current pricing in the [actor listing](https://apify.com/george.the.developer/linkedin-company-by-domain) before execution. The $0.10 setting is a maximum actor charge, not a promise that every requested domain will be resolved.

Company records can contain a website domain, LinkedIn company URL, company name, confidence, employee count and followers. Fields may be absent or null. This actor does not return individual employee profiles or email addresses. Cached resolutions can reduce charges; billing follows the actor's current event rules.

## Verification

The embedded workflow code and request contracts have local tests covering input limits, success/failure routing, polling expiry, malformed responses, empty datasets, unresolved rows, authentication configuration and secret-free JSON exports. Tests use synthetic fixtures and do not start paid actor runs.

Run with Node.js 22 or newer:

```text
npm test
```

The workflow passed three CLI execution scenarios in n8n 2.42.4 using a local mock API and synthetic credentials: success, failed actor run and empty dataset. See the [engine report](verification/n8n-engine.json) and [verification scope](SUBMISSIONS.md). No paid actor execution was performed. Existing actor dataset fields were inspected read-only; current live resolution remains unverified. Clay and Make documents are setup guides, not exported native templates.

## Useful references

- [Apify actor run API](https://docs.apify.com/api/v2/actors-runs-post)
- [n8n HTTP Request documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
- [Clay's Apify integration](https://www.clay.com/integrations/data-provider/apify)
- [Apify and Make](https://apify.com/integrations/make)

Maintained by George, the developer of the linked actor. This pack has not been endorsed by n8n, Clay, Make or Postman. Integration platform subscriptions and actor charges are separate.
