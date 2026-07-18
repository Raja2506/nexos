import asyncio
from app.agents.presentation_agent import PresentationAgent
from app.agents.email_writer_agent import EmailWriterAgent
from app.agents.summarizer_agent import SummarizerAgent


async def main():
    title = "Q1 Sales Report"
    sections = [
        {"heading": "Overview", "content": "Sales grew by 20% in Q1. The North region led with $50,000 in revenue. The South region grew the fastest at 35%."},
    ]
    long_content = sections[0]["content"] + " This growth was driven by a new marketing campaign and improved customer retention strategies across all regions."

    presenter = PresentationAgent()
    slides = await presenter.run({"title": title, "sections": sections})
    print("Slides:", slides)

    emailer = EmailWriterAgent()
    email = await emailer.run({
        "content": long_content,
        "tone": "professional",
        "recipient_context": "the sales director",
    })
    print("\nEmail Subject:", email["subject"])
    print("Email Body:", email["body"])

    summarizer = SummarizerAgent()
    summary = await summarizer.run({"content": long_content, "max_sentences": 2})
    print("\nSummary:", summary["summary"])


if __name__ == "__main__":
    asyncio.run(main())