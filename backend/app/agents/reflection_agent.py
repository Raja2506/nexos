import json
from google import genai
from app.agents.base_agent import BaseAgent
from app.config import SETTINGS


class ReflectionAgent(BaseAgent):
    """
    Looks back at a completed task's outcome and extracts a lesson
    learned - useful for improving future attempts at similar tasks.
    """

    def __init__(self):
        super().__init__(name="ReflectionAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])

    async def run(self, input_data: dict) -> dict:
        task_description = input_data["task_description"]
        outcome = input_data["outcome"]
        details = input_data.get("details", "")

        self.log(f"Reflecting on task: {task_description[:60]}... ({outcome})")

        prompt = f"""A task was attempted with the following result. Reflect on
what worked or didn't work, and extract ONE short, reusable lesson.

Task: {task_description}
Outcome: {outcome}
Details: {details}

Return ONLY valid JSON in this exact format:
{{"lesson": "short reusable lesson", "should_retry_differently": true | false}}"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1].replace("json", "", 1).strip()

        result = json.loads(raw_text)
        self.log(f"Lesson learned: {result['lesson']}")
        return result