# Company domain research with Gumloop and Apify

Use your own Apify account to request company research from [LinkedIn Company by Domain](https://apify.com/george.the.developer/linkedin-company-by-domain). Gumloop usage and Apify actor charges are separate.

## Connect an agent through MCP

Gumloop documents remote HTTPS MCP connections with OAuth discovery. In **Settings > Connectors**, open the menu beside **Add Connector** and choose **Add MCP Connector**. Select **Public URL** and enter:

```text
https://mcp.apify.com?tools=call-actor,get-actor-run,get-dataset-items
```

Choose **Connect**. If OAuth is detected, choose **Authenticate** and authorize your Apify account. Then add the configured connector from your private agent's **Connectors** section. These steps follow [Gumloop's connector documentation](https://docs.gumloop.com/nodes/mcp/custom_mcp_servers); native connection completion has not been tested for this pack.

This is Apify's shared hosted service. The generic runner can execute other actors too. Its URL selects tools; it does not enforce an actor-specific or account-wide spending budget. Gumloop documents direct access to exposed tools without a separate approval prompt. Use a private agent and your own connection; do not publish an agent that gives strangers access to your paid Apify account.

## Start one bounded research request

When you intend to incur actor charges, use [the supplied call arguments](../mcp/company-domain-run.json). They select `george.the.developer/linkedin-company-by-domain`, three sample domains, and:

```json
{
  "maxTotalChargeUsd": 0.1,
  "memory": 512,
  "timeout": 900
}
```

Keep these values under `callOptions`, outside the actor's `input`. The cap applies to that call, not every future agent request. Give the resolver its working time before its final three-minute reserve. Partial or unresolved results remain possible.

Start once, retain the run ID, and follow [the polling and dataset instructions](mcp.md#run-the-three-domain-example). Inspect the existing run after an ambiguous response before starting again. Review company identity and confidence; the actor does not supply employee profiles or email addresses.

## Existing workflow users: Task Runner

[Apify's Gumloop integration guide](https://docs.apify.com/integrations/gumloop) documents a separate **Apify Task Runner** node. It selects saved tasks rather than individual actors, and requires at least one completed task execution to discover output fields. Copy the [starter task](https://apify.com/george.the.developer/linkedin-company-by-domain/examples/company-domain-research-starter), review its limits, and deliberately run your own copy before using this route. That run can incur charges. The original starter still had zero runs when checked on October 8, 2026.

## What is verified

The connection instructions were checked against first-party documentation on October 8, 2026. The existing call example passed the pack's local contract checks and earlier authenticated Apify MCP schema checks. No Gumloop account connection, agent execution, native workflow/template publication, customer adoption or revenue is established. This page is a setup guide, not a Gumloop gallery listing or endorsement.
