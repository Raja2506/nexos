import asyncio
from app.agents.data_cleaning_agent import DataCleaningAgent
from app.agents.visualization_agent import VisualizationAgent


async def main():
    raw_rows = [
        {"month": "Jan", "sales": 100},
        {"month": "Feb", "sales": 150},
        {"month": "Jan", "sales": 100},
        {"month": "Mar", "sales": None},
    ]

    cleaner = DataCleaningAgent()
    cleaned = await cleaner.run({"rows": raw_rows})
    print("Report:", cleaned["report"])
    print("Cleaned rows:", cleaned["cleaned_rows"])

    visualizer = VisualizationAgent()
    chart = await visualizer.run({
        "rows": cleaned["cleaned_rows"],
        "x_column": "month",
        "y_column": "sales",
        "chart_type": "bar",
    })
    print("Chart saved at:", chart["chart_path"])


if __name__ == "__main__":
    asyncio.run(main())
    