# Submission and verification status

n8n public listing checked October 10, 2026. Windmill retains its October 9 checkpoint. Gumloop retains its October 8 checkpoint. Other channel records retain their October 7 checkpoints.

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
| n8n Creator Hub | [Template 20634](https://n8n.io/workflows/20634) approved October 9; public gallery listing verified October 10 | Measure adoption and paid use; native cloud execution remains unverified |
| Postman Public API Network | Not published; signup browser reached a security verification page | Authenticated public workspace or Postman API key |
| Clay | Guide prepared; no native table | Authenticated workspace, table validation, public template sharing |
| Make | Guide prepared; no native scenario | Authenticated workspace, scenario validation and optional gallery approval |
| Gumloop | [Sourced MCP and Task Runner guide](guides/gumloop.md); no native connection or template | Customer-owned OAuth connection and deliberate bounded validation; Task Runner also requires a completed saved-task run |
| Windmill | [Native Hub script 22820](https://hub.windmill.dev/scripts/apify/22820/research-company-domains-with-apify-and-review-unresolved-matches-apify) submitted October 9; public source and description match the reviewed pack | Moderator approval and integration catalog placement remain unverified; native execution and paid adoption unmeasured |
| Apify hosted MCP connection | Initialization and tool discovery verified; connection guide and capped call example included | Client OAuth/UI setup and live actor execution remain unverified |
| MCP directories | Not submitted | An owned, tested MCP server registration or supported connection listing |
| Apify agentic discovery | Existing automatic discovery verified: 49 of 83 public listings matched the eligible filter on October 7 | [Guide](guides/agentic-discovery.md) and [snapshot](verification/agentic-discovery.json); payment, actor execution and commercial adoption unverified |

## Verification scope

- Thirteen local workflow/collection/MCP contract tests cover synthetic fixtures, the documented actor shutdown reserve and credential-free MCP examples.
- Thirteen additional Python HTTP tests exercise the Windmill script locally with synthetic credentials. Native Hub script 22820 is publicly accessible; moderator approval, integration catalog placement, native Windmill execution and live actor resolution remain unverified.
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

Creator registration initially displayed an email-verification instruction. A later authenticated login reached the dashboard and upload form, so that message did not block submission. Template `20634` was uploaded once, finalized and submitted for human review at `2026-10-07T13:14:10.217Z`. The owner received n8n's approval notification on October 9. On October 10, a normal browser read confirmed the public listing, **Resolve company domains to LinkedIn company pages with Apify**, creator George Kioko and the **Use for free** button. No import or actor run was started. Executable nodes, connections and limits in this repository are unchanged from the CLI-verified workflow.

At submission on October 7, the uploaded overview note was shorter than the finalized listing description. The repository's workflow and [description](guides/n8n-template.md) include every finalized description section. n8n rejected an edit with HTTP 400 while the template was under review. The published workflow's overview note has not been rechecked. Apply the prepared note correction when creator-portal edits are available; no duplicate submission was created. The prepared change affects instructions and layout only.

## Publishing routes

- [n8n creator login](https://creators.n8n.io/login) and [registration](https://creators.n8n.io/register).
- [Postman public workspace instructions](https://learning.postman.com/docs/collaborating-in-postman/using-workspaces/public-workspaces/).
- [Clay sharing](https://university.clay.com/docs/workbook-table-sharing-guide).
- [Make sharing](https://help.make.com/scenario-sharing) and [template approval](https://help.make.com/create-and-manage-scenario-templates).
