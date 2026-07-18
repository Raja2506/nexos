from google import genai
from app.agents.base_agent import BaseAgent
from app.config import SETTINGS


class SummarizerAgent(BaseAgent):
    """
    Condenses long content into a short summary at a chosen length.
    """

    def __init__(self):
        super().__init__(name="SummarizerAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])

    async def run(self, input_data: dict) -> dict:
        content = input_data["content"]
        max_sentences = input_data.get("max_sentences", 3)

        self.log(f"Summarizing {len(content)} characters into {max_sentences} sentences")

        prompt = f"""Summarize the following content in exactly {max_sentences} sentences
or fewer. Return ONLY the summary text, no preamble, no markdown.

Content:
{content}"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        summary = response.text.strip()

        self.log(f"Summary generated: {len(summary)} characters")
        return {"summary": summary}