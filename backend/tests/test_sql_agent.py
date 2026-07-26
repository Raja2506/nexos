# backend/tests/test_sql_agent.py
from app.agents.sql_agent import SQLAgent


async def test_sql_agent_basic_query():
    agent = SQLAgent()
    result = await agent.run({"question": "How many tasks are there in total?"})

    assert result is not None
    assert "sql" in result
    assert "rows" in result
