# backend/tests/test_research_agent.py
import asyncio
from app.agents.research_agent import ResearchAgent

async def main():
    agent = ResearchAgent()
    result = await agent.run({"topic": "latest trends in AI agent frameworks 2026"})
    print("SUMMARY:\n", result["summary"])
    print("\nSOURCES:")
    for s in result["sources"]:
        print(f"- {s['title']}: {s['url']}")

asyncio.run(main())