import json
from google import genai
from app.agents.base_agent import BaseAgent
from app.config import SETTINGS


class FactCheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="FactCheckerAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])

    async def run(self, input_data: dict) -> dict:
        claim = input_data["claim"]
        context = input_data.get("context", "")
        self.log(f"Fact-checking: {claim[:60]}...")

        prompt = f"""You are a strict fact-checker. Evaluate this claim for
internal consistency and plausibility, given the context.

Context: {context}
Claim: {claim}

Return ONLY valid JSON in this exact format:
{{"verdict": "supported" | "unsupported" | "uncertain", "reason": "short explanation"}}"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1].replace("json", "", 1).strip()

        result = json.loads(raw_text)
        self.log(f"Verdict: {result['verdict']}")
        return result