# backend/tests/test_task_splitter_agent.py
import asyncio
from app.agents.task_splitter_agent import TaskSplitterAgent

async def main():
    agent = TaskSplitterAgent()
    result = await agent.run({
        "steps": [
            {"id": "1", "description": "Research competitor pricing"},
            {"id": "2", "description": "Write a summary report"},
        ]
    })
    print(result)

asyncio.run(main())