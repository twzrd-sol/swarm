"""
TWZRD Agent Trust Checker - agents.py

Demonstrates using TWZRD Agent Intel MCP server to verify Solana agent
trustworthiness before processing requests. Agents with low trust scores
or failed preflight checks are rejected.

MCP server: https://intel.twzrd.xyz/mcp
Tools: score_agent, preflight_check (free); get_trust_receipt (x402 paid)
"""

import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from swarm import Agent

MCP_URL = "https://intel.twzrd.xyz/mcp"
TRUST_THRESHOLD = 0.5


async def _call_mcp_tool(tool_name: str, wallet: str) -> str:
    """Call a TWZRD MCP tool and return the result text."""
    async with streamablehttp_client(MCP_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, {"wallet": wallet})
            return result.content[0].text


def score_agent_wallet(wallet: str) -> str:
    """
    Score a Solana agent wallet using TWZRD Agent Intel.
    Returns trust score (0-1) and x402 payment history.
    """
    result = asyncio.run(_call_mcp_tool("score_agent", wallet))
    return result


def preflight_check_wallet(wallet: str) -> str:
    """
    Run a preflight check on a Solana agent wallet.
    Returns APPROVE or REJECT with detailed reasoning.
    """
    result = asyncio.run(_call_mcp_tool("preflight_check", wallet))
    return result


def transfer_to_payment_processor():
    """Transfer approved agents to the payment processing agent."""
    return payment_agent


def transfer_to_trust_checker():
    """Route back to trust checker for re-verification."""
    return trust_agent


trust_agent = Agent(
    name="Trust Checker",
    instructions=(
        "You verify Solana agent wallets before allowing them to proceed. "
        "For every request: "
        "1. Extract the wallet address from the user message. "
        "2. Call score_agent_wallet to get the trust score. "
        "3. Call preflight_check_wallet for a APPROVE/REJECT decision. "
        f"4. If the preflight result is APPROVE and score >= {TRUST_THRESHOLD}: "
        "   transfer to the payment_agent. "
        "5. Otherwise: inform the user their wallet is not trusted and stop. "
        "Always cite the trust score and preflight result in your response."
    ),
    functions=[score_agent_wallet, preflight_check_wallet, transfer_to_payment_processor],
)

payment_agent = Agent(
    name="Payment Processor",
    instructions=(
        "You process requests from verified, trusted Solana agents. "
        "The trust checker has already verified the agent wallet. "
        "Acknowledge the verified agent and process their request. "
        "If the user asks about their trust receipt, remind them they can call "
        "get_trust_receipt via https://intel.twzrd.xyz/mcp (paid endpoint, HTTP 402)."
    ),
    functions=[transfer_to_trust_checker],
)
