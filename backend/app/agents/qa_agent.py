import json
from google import genai
from app.agents.base_agent import BaseAgent
from app.config import SETTINGS

QUALITY_THRESHOLD = 7


class QAAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="QAAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])

    async def run(self, input_data: dict) -> dict:
        content = input_data["content"]
        fact_check_verdict = input_data.get("fact_check_verdict", "uncertain")
        review_issues = input_data.get("review_issues", [])

        self.log("Scoring output quality")

        prompt = f"""Score this output from 0-10 based on:
- Accuracy (fact-check verdict: {fact_check_verdict})
- Quality issues found: {review_issues}
- Overall clarity and completeness

Content:
{content}

Return ONLY valid JSON in this exact format:
{{"score": 0-10, "reasoning": "short explanation"}}"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1].replace("json", "", 1).strip()

        result = json.loads(raw_text)
        score = result["score"]
        passed = score >= QUALITY_THRESHOLD

        self.log(f"Score: {score}/10 - {'PASS' if passed else 'FAIL'}")
        return {"score": score, "passed": passed, "reasoning": result["reasoning"]}