# Company-domain research in Make

Use Make's existing Apify integration and your own Apify account with [LinkedIn Company by Domain](https://apify.com/george.the.developer/linkedin-company-by-domain).

## Build the scenario

1. Start with a manual trigger or a small existing spreadsheet input.
2. Add an Apify **Run an Actor** module and select the company-domain actor.
3. Supply the domain array and actor input shown below. Use Make's mapping controls to produce a JSON array when adding spreadsheet values.
4. Retrieve results only after the run has completed. Use the integration's finished-run monitoring and dataset modules, or a bounded status polling route if required by your chosen module version.
5. Add an iterator for dataset rows when the module returns an array, then map each company's fields to a Google Sheets row.
6. Route failed, timed-out and aborted runs to an error handler. Keep unresolved company rows and match by domain.

```json
{
  "domains": ["stripe.com", "vercel.com", "gitlab.com"],
  "maxDomains": 3,
  "mode": "resolve",
  "includeUnresolved": true,
  "concurrency": 3
}
```

Check the module's run options and set a charge cap and timeout before execution. Where the native module lacks a required option, configure an Apify task or use the HTTP API with those options explicitly. The n8n workflow's $0.10 cap does not apply automatically to Make.

## Share after validation

Test successful output, an unresolved domain, an empty dataset and actor failure. Confirm the scenario does not automatically create duplicate runs when an HTTP response is delayed.

For direct distribution, use **Share → Public scenario page** on the saved scenario. For the Make gallery, create and publish a template, then use **Request approval**. Gallery publication requires Make's review.

Exported blueprints require users to configure their own connections. Inspect the export and public preview for credentials and private data before sharing.

This guide is not an exported Make blueprint. A native scenario must be built and tested in an authenticated workspace before publishing a scenario link or requesting gallery approval.

Sources: [Apify and Make](https://apify.com/integrations/make), [scenario sharing](https://help.make.com/scenario-sharing), [template approval](https://help.make.com/create-and-manage-scenario-templates).
