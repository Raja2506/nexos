import json
from google import genai
from app.agents.base_agent import BaseAgent
from app.config import SETTINGS


class DecisionAgent(BaseAgent):
    """
    Given a situation and a list of possible options, picks the best
    one with reasoning. Used for routing decisions in orchestration.
    """

    def __init__(self):
        super().__init__(name="DecisionAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])

    async def run(self, input_data: dict) -> dict:
        situation = input_data["situation"]
        options = input_data["options"]

        self.log(f"Deciding among {len(options)} options for: {situation[:60]}...")

        options_list = "\n".join(f"- {opt}" for opt in options)
        prompt = f"""Given this situation, choose the single best option from the list.

Situation: {situation}

Options:
{options_list}

Return ONLY valid JSON in this exact format:
{{"chosen_option": "exact text of chosen option", "reasoning": "short explanation"}}"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1].replace("json", "", 1).strip()

        result = json.loads(raw_text)
        self.log(f"Chose: {result['chosen_option']}")
        return result