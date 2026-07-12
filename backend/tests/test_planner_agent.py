import asyncio
from app.agents.planner_agent import PlannerAgent


async def main():
    agent = PlannerAgent()
    result = await agent.run({"goal": "Write a blog post about renewable energy"})
    print("\nTask Graph:")
    for step in result["steps"]:
        print(f"  Step {step['id']}: {step['description']}")


if __name__ == "__main__":
    asyncio.run(main())