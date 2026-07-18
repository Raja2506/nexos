# backend/tests/test_python_agent.py
import asyncio
from app.agents.python_agent import PythonAgent

async def main():
    agent = PythonAgent()
    result = await agent.run({"task": "Find the average of [12, 45, 67, 23, 89]"})
    print("Code:\n", result["code"])
    print("Output:", result["output"])

asyncio.run(main())
