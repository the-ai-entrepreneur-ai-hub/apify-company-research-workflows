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
| Public GitHub workflow pack | Prepared locally | Fresh review, commit, publication and anonymous download verification |
| n8n Creator Hub | Not submitted | Authenticated creator account, workflow verification and portal review |
| Postman Public API Network | Not published | Authenticated public workspace or Postman API key |
| Clay | Guide prepared; no native table | Authenticated workspace, table validation, public template sharing |
| Make | Guide prepared; no native scenario | Authenticated workspace, scenario validation and optional gallery approval |
| MCP directories | Not submitted | An owned, tested MCP server registration or supported connection listing |

## Verification scope

- Ten local workflow/collection contract tests pass against synthetic fixtures.
- Input/output field names were compared with the actor's local schema and existing dataset rows.
- No new paid actor run was started.
- A full n8n engine verification is being attempted separately; until recorded below, local tests do not prove successful import and execution in n8n.
- Postman collection schema validation is a separate gate before publication.
- No paying-user acquisition, channel attribution or revenue improvement has been measured.

## Publishing routes

- [n8n creator login](https://creators.n8n.io/login) and [registration](https://creators.n8n.io/register).
- [Postman public workspace instructions](https://learning.postman.com/docs/collaborating-in-postman/using-workspaces/public-workspaces/).
- [Clay sharing](https://university.clay.com/docs/workbook-table-sharing-guide).
- [Make sharing](https://help.make.com/scenario-sharing) and [template approval](https://help.make.com/create-and-manage-scenario-templates).
