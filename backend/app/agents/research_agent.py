# backend/app/agents/research_agent.py
from google import genai
from app.agents.base_agent import BaseAgent
from app.agents.web_search_agent import WebSearchAgent
from app.config import SETTINGS


class ResearchAgent(BaseAgent):
    """
    Uses the Web Search Agent to gather raw information, then
    synthesizes it into a clean, structured research summary.
    """

    def __init__(self):
        super().__init__(name="ResearchAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])
        self.web_search_agent = WebSearchAgent()

    async def run(self, input_data: dict) -> dict:
        topic = input_data["topic"]
        self.log(f"Researching: {topic}")

        search_result = await self.web_search_agent.run({"query": topic})

        prompt = f"""Based on the following web search findings, write a concise
research summary (3-5 bullet points) about: {topic}

Findings:
{search_result['answer']}"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )

        self.log("Research summary generated")
        return {
            "topic": topic,
            "summary": response.text,
            "sources": search_result["sources"],
        }