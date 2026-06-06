"""run.py - Interactive TWZRD agent trust verification demo."""

from swarm.repl import run_demo_loop
from agents import trust_agent

if __name__ == "__main__":
    print("TWZRD Agent Trust Checker")
    print("=" * 40)
    print("Try: Check wallet D1QkbFJKiPsymJ65RKHhF6DFB8sPMfpBaFBzuHKfJGWi")
    print("MCP server: https://intel.twzrd.xyz/mcp")
    print()
    run_demo_loop(trust_agent, stream=True)
