# backend/tests/test_code_generator_agent.py
import asyncio
from app.agents.code_generator_agent import CodeGeneratorAgent
from app.agents.bug_fix_agent import BugFixAgent

async def main():
    gen = CodeGeneratorAgent()
    result = await gen.run({"task": "Calculate the sum of squares from 1 to 10"})
    print("Generated code:\n", result["code"])

    fixer = BugFixAgent()
    final = await fixer.run({"code": result["code"]})
    print("\nOutput:", final["output"])
    print("Attempts:", final["attempts"])

asyncio.run(main())