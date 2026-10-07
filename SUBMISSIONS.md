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
| n8n Creator Hub | Creator account created; not submitted | Email verification, workflow engine check and portal review |
| Postman Public API Network | Not published; signup browser reached a security verification page | Authenticated public workspace or Postman API key |
| Clay | Guide prepared; no native table | Authenticated workspace, table validation, public template sharing |
| Make | Guide prepared; no native scenario | Authenticated workspace, scenario validation and optional gallery approval |
| MCP directories | Not submitted | An owned, tested MCP server registration or supported connection listing |

## Verification scope

- Ten local workflow/collection contract tests pass against synthetic fixtures.
- Input/output field names were compared with the actor's local schema and existing dataset rows.
- No new paid actor run was started.
- Independent review identified and corrected an unavailable sandbox global; all ten tests pass without injecting that global.
- A full n8n engine verification is being attempted separately; until recorded below, local tests do not prove successful import and execution in n8n.
- Postman collection passes the official v2.1 collection schema validation.
- No paying-user acquisition, channel attribution or revenue improvement has been measured.

## Published assets

[Public repository](https://github.com/the-ai-entrepreneur-ai-hub/apify-company-research-workflows). Initial publication commit: `ad4d2e1`.

Anonymous requests retrieved the workflow JSON, Postman collection and README and matched them against the local files. The initial [automated validation run](https://github.com/the-ai-entrepreneur-ai-hub/apify-company-research-workflows/actions/runs/37615595771) completed successfully.

Creator account creation returned a successful response and the n8n portal displayed its email-verification instruction. This is not template submission or acceptance. Available mailbox connections did not provide the registration inbox.

## Publishing routes

- [n8n creator login](https://creators.n8n.io/login) and [registration](https://creators.n8n.io/register).
- [Postman public workspace instructions](https://learning.postman.com/docs/collaborating-in-postman/using-workspaces/public-workspaces/).
- [Clay sharing](https://university.clay.com/docs/workbook-table-sharing-guide).
- [Make sharing](https://help.make.com/scenario-sharing) and [template approval](https://help.make.com/create-and-manage-scenario-templates).
