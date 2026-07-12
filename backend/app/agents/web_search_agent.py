# backend/app/agents/web_search_agent.py
from google import genai
from app.agents.base_agent import BaseAgent
from app.config import SETTINGS


class WebSearchAgent(BaseAgent):
    """
    NOTE: Real-time Google Search grounding requires a billing-enabled
    Gemini project (free tier does not include it). Until billing is
    added, this agent answers from the model's own knowledge and is
    clearly labeled as ungrounded so downstream agents/users know not
    to treat it as live web data.
    """

    def __init__(self):
        super().__init__(name="WebSearchAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])

    async def run(self, input_data: dict) -> dict:
        query = input_data["query"]
        self.log(f"Answering from model knowledge (grounding disabled): {query}")

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=query,
        )

        return {
            "answer": response.text,
            "sources": [],
            "grounded": False,  # important flag — no real-time web data used
        }
        