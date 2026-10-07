# Discover company research tools for AI agents

Apify supports experimental agentic payments through x402 and Skyfire. Eligible actors can be discovered and paid for without a conventional Apify account. This guide helps you find the company-domain resolver; payment setup follows Apify's current documentation.

## Choose the company resolver

Use [LinkedIn Company by Domain](https://apify.com/george.the.developer/linkedin-company-by-domain) to turn website domains into company research records. It returns company information, not individual employee profiles or email addresses. Review its current input schema, pricing and output limitations before execution.

The October 7, 2026 [catalog](../verification/agentic-discovery.json) records 49 eligible actors among 83 public listings for this developer. The resolver, employee scraper, YouTube transcript scraper and calibrated Google Trends API appeared in the eligible filter. This is an eligibility snapshot; no agent purchase or actor execution was tested.

## Check current availability without running an actor

Open the [live eligible catalog](https://api.apify.com/v2/store?username=george.the.developer&allowsAgenticUsers=true&limit=1000). Find `linkedin-company-by-domain` and check its `isWhiteListedForAgenticPayments` response flag. The query parameter is named `allowsAgenticUsers`; the returned field has a different name.

This GET request retrieves public metadata. It does not start an actor run or purchase a prepaid token. If the actor is absent or its flag is false, do not assume it supports agentic payments.

## Connect and pay deliberately

Follow [Apify's x402 setup guide](https://docs.apify.com/integrations/x402) for current wallet, funding, prepaid-token and execution instructions. The documented flow buys a prepaid token first; execution then consumes its balance. Funding and execution incur costs. Keep wallet credentials and prepaid tokens private. No payment commands are executed by this page.

For an existing Apify account, use the [hosted MCP connection guide](mcp.md) instead. Its company-research example requests a $0.10 maximum actor charge, 512 MB and a 900-second timeout. Those example limits do not automatically carry over to a separately constructed agentic-payment request.

## Eligibility and verification limits

[Apify's monetization documentation](https://docs.apify.com/actors/publishing/monetize) requires pay-per-event pricing without added platform-usage billing, limited permissions, no Standby mode, and developer identity verification. Eligible actors become available automatically.

Shopify DTC Brand Discovery was absent from the eligible filter and had Standby enabled when inspected. Its configuration has not been changed. Do not disable a working API mode simply to gain another discovery placement without assessing existing consumers.

The snapshot was checked against unfiltered, eligible, excluded and include-unrunnable Store responses. The 49 eligible and 34 excluded IDs were disjoint and together matched all 83 listings. Returned eligibility flags agreed with both filters.

These checks establish discoverability and metadata consistency. They do not establish wallet authentication, successful payment, useful live results, recurring customers or profit. The existing n8n workflow's local-mock tests cover a different integration path.
