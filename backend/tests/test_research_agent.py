# backend/tests/test_research_agent.py
from app.agents.research_agent import ResearchAgent


async def test_research_agent_basic_topic():
    agent = ResearchAgent()
    result = await agent.run({"topic": "latest trends in AI agent frameworks 2026"})

    assert result is not None
    assert "summary" in result
    assert "sources" in result
