# backend/tests/test_task_splitter_agent.py
from app.agents.task_splitter_agent import TaskSplitterAgent


async def test_task_splitter_agent_dependency_graph():
    agent = TaskSplitterAgent()
    result = await agent.run({
        "steps": [
            {"id": "1", "description": "Research competitor pricing"},
            {"id": "2", "description": "Write a summary report"},
        ]
    })

    assert result is not None
