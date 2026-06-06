# TWZRD Agent Trust Checker

A Swarm example that gates agent requests behind on-chain Solana trust
verification using the [TWZRD Agent Intel](https://intel.twzrd.xyz) MCP server.

## What It Does

Two cooperating agents:

1. **Trust Checker** — calls the TWZRD MCP server to score a Solana wallet
   and run a preflight check. Wallets with a trust score ≥ 0.5 and an
   `APPROVE` preflight result are forwarded to the payment processor.
2. **Payment Processor** — handles requests from verified agents only.

## Setup

```bash
pip install swarm mcp openai
export OPENAI_API_KEY=sk-...
```

The TWZRD MCP server requires no API key for `score_agent` and
`preflight_check`. The `get_trust_receipt` tool is a paid endpoint
(HTTP 402 / x402 protocol) — see [intel.twzrd.xyz](https://intel.twzrd.xyz).

## MCP Config

```json
{
  "mcpServers": {
    "twzrd-agent-intel": {
      "url": "https://intel.twzrd.xyz/mcp"
    }
  }
}
```

## Run

```shell
python3 run.py
```

Then enter a prompt like:

```
Check wallet D1QkbFJKiPsymJ65RKHhF6DFB8sPMfpBaFBzuHKfJGWi
```

## Tools

| Tool | Description | Cost |
|------|-------------|------|
| `score_agent` | Trust score (0–1) + x402 payment count | Free |
| `preflight_check` | APPROVE/REJECT with reasoning | Free |
| `get_trust_receipt` | Signed on-chain trust receipt | HTTP 402 |
