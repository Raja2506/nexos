import asyncio
from app.agents.memory_agent import MemoryAgent
from app.agents.reflection_agent import ReflectionAgent
from app.agents.decision_agent import DecisionAgent


async def main():
    memory = MemoryAgent()

    await memory.run({
        "action": "remember_short",
        "session_id": "test_session",
        "key": "last_topic",
        "value": {"topic": "sales report"},
    })
    recalled = await memory.run({
        "action": "recall_short",
        "session_id": "test_session",
        "key": "last_topic",
    })
    print("Recalled short-term:", recalled)

    stored = await memory.run({
        "action": "remember_long",
        "text": "User prefers bar charts over pie charts for sales data",
        "metadata": {"category": "preference"},
    })
    print("Stored long-term:", stored)

    recalled_long = await memory.run({
        "action": "recall_long",
        "query": "what chart type does the user like",
    })
    print("Recalled long-term:", recalled_long)

    reflector = ReflectionAgent()
    reflection = await reflector.run({
        "task_description": "Generate a sales chart for Q1",
        "outcome": "success",
        "details": "Bar chart generated correctly on first attempt",
    })
    print("\nReflection:", reflection)

    decider = DecisionAgent()
    decision = await decider.run({
        "situation": "User asked to visualize sales trends over 12 months",
        "options": ["bar chart", "line chart", "pie chart"],
    })
    print("Decision:", decision)


if __name__ == "__main__":
    asyncio.run(main())