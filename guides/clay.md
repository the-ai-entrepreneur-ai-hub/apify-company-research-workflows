# Company-domain enrichment in Clay

Use your existing domain column and Clay's native Apify connection to run [LinkedIn Company by Domain](https://apify.com/george.the.developer/linkedin-company-by-domain).

## Set up the table

1. Create a table with a `domain` column and add a few company website domains.
2. Add the **Run Apify Actor** action and connect your Apify account.
3. Select the company-domain actor. Supply `domains` as an array containing the mapped domain column value. Use Clay's field picker to insert the value as a JSON string rather than pasting a literal column name.
4. For an initial single-domain action, set `maxDomains` to 1, `mode` to `resolve`, `includeUnresolved` to `true` and `concurrency` to 1.
5. Complete a small manual test, then use **Import data from Apify Actor** to retrieve the completed run's dataset. Check whether your Clay action returns data directly or requires the import step in its current version.
6. Map company name, LinkedIn URL, confidence and available company counts to output columns.

A literal actor-input example for a single domain is:

```json
{
  "domains": ["stripe.com"],
  "maxDomains": 1,
  "mode": "resolve",
  "includeUnresolved": true,
  "concurrency": 1
}
```

Replace the literal domain with your mapped input before enabling automatic table execution. The actor's default charge cap is much higher than the starter n8n cap; configure run options in the integration if supported, or use an Apify task with verified bounds. Do not assume a cap in this guide changes the native Clay action.

## Review before sharing

Match imported results back to input rows by `domain`, never by array position. Retain low-confidence and unresolved rows so missing matches are visible. Verify that a failed run is surfaced and that an empty dataset does not look like successful enrichment. One run per table row can accumulate start fees; compare batch execution costs before scaling.

After testing in your Clay workspace, use the workbook/table menu's **Share as Template** option. Inspect the public preview and its sample row before sharing. Use a public example company instead of a private prospect record.

This is a setup guide. No native Clay table was created or shared as part of preparing it.

Sources: [Clay Apify integration](https://university.clay.com/docs/apify-integration-overview), [table sharing](https://university.clay.com/docs/workbook-table-sharing-guide).
