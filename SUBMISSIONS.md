# Submission and verification status

Last checked: October 7, 2026.

## Ready submission copy

**Title:** Resolve company website domains to LinkedIn company research records

**Description:** Import an n8n workflow that sends a small domain list to an Apify actor, polls its run status, retrieves company records and marks low-confidence results for review. It uses your own Apify account, a capped actor run and visible error handling. Export the results or connect a spreadsheet destination.

**Tags:** Apify, company research, LinkedIn company, CRM enrichment, n8n, API

**Setup requirements:** n8n, an Apify account and Header Auth credential. Actor runs can incur charges. Spreadsheet destinations require a separate connection. Start with the included three-domain example and inspect the output before scaling.

**Actor:** https://apify.com/george.the.developer/linkedin-company-by-domain

## Channel status

| Channel | Status | Next gate |
|---|---|---|
| Public GitHub workflow pack | Published; anonymous downloads verified | Measure adoption and maintain assets |
| Apify public starter task | Published; visible in the actor's Tasks tab without login | Customers copy and evaluate it; adoption unmeasured |
| n8n Creator Hub | Template 20634 submitted for human review on October 7; local-mock engine checks passed | Publisher review and public gallery acceptance |
| Postman Public API Network | Not published; signup browser reached a security verification page | Authenticated public workspace or Postman API key |
| Clay | Guide prepared; no native table | Authenticated workspace, table validation, public template sharing |
| Make | Guide prepared; no native scenario | Authenticated workspace, scenario validation and optional gallery approval |
| Apify hosted MCP connection | Initialization and tool discovery verified; connection guide and capped call example included | Client OAuth/UI setup and live actor execution remain unverified |
| MCP directories | Not submitted | An owned, tested MCP server registration or supported connection listing |

## Verification scope

- Thirteen local workflow/collection/MCP contract tests cover synthetic fixtures, the documented actor shutdown reserve and credential-free MCP examples.
- Input/output field names were compared with the actor's local schema and existing dataset rows.
- No new paid actor run was started.
- Independent review identified and corrected an unavailable sandbox global; workflow tests do not inject that global.
- n8n 2.42.4 CLI imported and executed the workflow against a local mock API on October 7, 2026. All three scenarios passed: successful polling and row review, terminal actor failure without dataset retrieval, and empty-dataset rejection. See the [engine verification report](verification/n8n-engine.json). Synthetic credentials and localhost HTTP responses replaced the live API; workflow code, graph and 15-second waits were unchanged. Browser UI import, cloud-hosted behavior and live actor output were not tested by this check.
- Postman collection passes the official v2.1 collection schema validation.
- No paying-user acquisition, channel attribution or revenue improvement has been measured.

Publication review found that the original 120-second actor timeout was shorter than the resolver's documented 180-second shutdown reserve. Corrected exports use a 900-second actor timeout, 17-minute polling age limit and 20-minute workflow execution limit. A regression test reproduced the incompatibility before the correction. Existing users should reimport the corrected exports.

The [public starter task](https://apify.com/george.the.developer/linkedin-company-by-domain/examples/company-domain-research-starter) uses three sample domains, 512 MB, a 900-second timeout and a $0.10 maximum actor charge. Its input passed Apify's live input-schema validation. Publication returned `isPublic:true`, and a signed-out browser displayed the task in the actor's Tasks tab. The task had zero runs at publication; saving and publishing it did not execute the actor. The task links back to this workflow pack. The task API itself still requires authentication.

## Published assets

[Public repository](https://github.com/the-ai-entrepreneur-ai-hub/apify-company-research-workflows). Initial publication commit: `ad4d2e1`.

Anonymous requests retrieved the workflow JSON, Postman collection and README and matched them against the local files. The initial [automated validation run](https://github.com/the-ai-entrepreneur-ai-hub/apify-company-research-workflows/actions/runs/37615595771) completed successfully.

Creator registration initially displayed an email-verification instruction. A later authenticated login reached the dashboard and upload form, so that message did not block submission. Template `20634`, **Resolve company domains to LinkedIn company records with Apify**, was uploaded once for automatic review, finalized and submitted for human review at `2026-10-07T13:14:10.217Z`. The portal confirmed submission and stated a typical review time of 3-5 business days. Public gallery approval and publication remain pending. Executable nodes, connections and limits are unchanged from the CLI-verified workflow.

Post-submission review found that the portal's finalized listing description was longer than the uploaded overview note. The repository's workflow and [description](guides/n8n-template.md) now include every finalized description section. The native submission still holds the earlier, shorter overview note: n8n rejected an edit with HTTP 400 because the template is under review. Apply the prepared note correction when the publisher permits edits; no duplicate submission was created. The change affects instructions and layout only. Full compliance with the description-in-sticky guideline remains pending for the native submission.

## Publishing routes

- [n8n creator login](https://creators.n8n.io/login) and [registration](https://creators.n8n.io/register).
- [Postman public workspace instructions](https://learning.postman.com/docs/collaborating-in-postman/using-workspaces/public-workspaces/).
- [Clay sharing](https://university.clay.com/docs/workbook-table-sharing-guide).
- [Make sharing](https://help.make.com/scenario-sharing) and [template approval](https://help.make.com/create-and-manage-scenario-templates).
