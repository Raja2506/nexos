import asyncio
from app.agents.fact_checker_agent import FactCheckerAgent
from app.agents.reviewer_agent import ReviewerAgent
from app.agents.qa_agent import QAAgent


async def main():
    content = "The Eiffel Tower was built in 1889 and is located in Paris, France."

    fact_checker = FactCheckerAgent()
    fact_result = await fact_checker.run({
        "claim": content,
        "context": "General knowledge fact about a famous landmark",
    })
    print("\nFact Check:", fact_result)

    reviewer = ReviewerAgent()
    review_result = await reviewer.run({
        "content": content,
        "content_type": "factual statement",
    })
    print("Review:", review_result)

    qa = QAAgent()
    qa_result = await qa.run({
        "content": content,
        "fact_check_verdict": fact_result["verdict"],
        "review_issues": review_result["issues"],
    })
    print("QA Score:", qa_result)


if __name__ == "__main__":
    asyncio.run(main())