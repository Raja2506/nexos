# backend/tests/test_sql_agent.py
import asyncio
from app.agents.sql_agent import SQLAgent

async def main():
    agent = SQLAgent()
    result = await agent.run({"question": "How many tasks are there in total?"})
    print("SQL:", result["sql"])
    print("Rows:", result["rows"])

asyncio.run(main())