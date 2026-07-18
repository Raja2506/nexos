import asyncio
from app.agents.security_agent import SecurityAgent
from app.agents.report_generator_agent import ReportGeneratorAgent


async def main():
    security = SecurityAgent()

    safe_content = "The average sales in Q1 was $45,000 across 3 regions."
    result1 = await security.run({"content": safe_content})
    print("Safe content scan:", result1)

    unsafe_content = "Here is the config: DATABASE_URL=postgresql://admin:hunter2@db.com/prod"
    result2 = await security.run({"content": unsafe_content})
    print("Unsafe content scan:", result2)

    reporter = ReportGeneratorAgent()
    report = await reporter.run({
        "title": "NexOS Weekly Summary",
        "sections": [
            {"heading": "Sales Overview", "content": safe_content},
            {"heading": "Security Check", "content": f"Scan passed: {result1['is_safe']}"},
        ],
    })
    print("\n--- REPORT ---")
    print(report["report"])


if __name__ == "__main__":
    asyncio.run(main())
    