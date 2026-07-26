# backend/tests/test_python_agent.py
from app.agents.python_agent import PythonAgent


async def test_python_agent_average_calculation():
    agent = PythonAgent()
    result = await agent.run({"task": "Find the average of [12, 45, 67, 23, 89]"})

    assert result is not None
    assert "code" in result
    assert "output" in result
