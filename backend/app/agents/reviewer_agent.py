import json
from google import genai
from app.agents.base_agent import BaseAgent
from app.config import SETTINGS


class ReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ReviewerAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])

    async def run(self, input_data: dict) -> dict:
        content = input_data["content"]
        content_type = input_data.get("content_type", "text")
        self.log(f"Reviewing {content_type} output")

        prompt = f"""Review this {content_type} output for quality, clarity,
and correctness. Be specific about any issues.

Content:
{content}

Return ONLY valid JSON in this exact format:
{{"approved": true | false, "issues": ["issue1", "issue2"], "suggestion": "..."}}"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1].replace("json", "", 1).strip()

        result = json.loads(raw_text)
        self.log(f"Approved: {result['approved']}, {len(result['issues'])} issues found")
        return result