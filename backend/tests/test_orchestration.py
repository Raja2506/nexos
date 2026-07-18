import asyncio
from app.orchestration.graph_builder import build_graph


async def main():
    graph = build_graph()
    initial_state = {"goal": "How many tasks are there in total?"}

    print("Running graph...\n")
    final_state = await graph.ainvoke(initial_state)

    print("=" * 50)
    print("FINAL STATE")
    print("=" * 50)
    print("Task type:", final_state.get("task_type"))
    print("Raw data:", final_state.get("raw_data"))
    print("QA score:", final_state.get("qa_score"))
    print("\n--- FINAL REPORT ---")
    print(final_state.get("final_report"))


if __name__ == "__main__":
    asyncio.run(main())