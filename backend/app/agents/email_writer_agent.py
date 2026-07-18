import json
from google import genai
from app.agents.base_agent import BaseAgent
from app.config import SETTINGS


class EmailWriterAgent(BaseAgent):
    """
    Converts a report/summary into a professional email with
    subject line and body, in a chosen tone.
    """

    def __init__(self):
        super().__init__(name="EmailWriterAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])

    async def run(self, input_data: dict) -> dict:
        content = input_data["content"]
        tone = input_data.get("tone", "professional")
        recipient_context = input_data.get("recipient_context", "a colleague")

        self.log(f"Writing {tone} email for {recipient_context}")

        prompt = f"""Write a {tone} email based on this content, addressed to {recipient_context}.

Content:
{content}

Return ONLY valid JSON in this exact format:
{{"subject": "...", "body": "..."}}"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1].replace("json", "", 1).strip()

        result = json.loads(raw_text)
        self.log(f"Email drafted: {result['subject']}")
        return result