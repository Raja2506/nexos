import json
from anthropic import Anthropic
from app.agents.base_agent import BaseAgent
from app.config import SETTINGS


class PlannerAgent(BaseAgent):
    """
    Takes a user's goal in plain English and breaks it into
    a structured list of smaller tasks (a task graph).
    """

    def __init__(self):
        super().__init__(name="PlannerAgent")
        self.client = Anthropic(api_key=SETTINGS["ANTHROPIC_API_KEY"])

    async def run(self, input_data: dict) -> dict:
        goal = input_data["goal"]
        self.log(f"Planning for goal: {goal}")

        prompt = f"""Break the following goal into 2-5 smaller, actionable steps.
Return ONLY valid JSON, no other text, in this exact format:
{{"steps": [{{"id": "1", "description": "..."}}, {{"id": "2", "description": "..."}}]}}

Goal: {goal}"""

        response = self.client.messages.create(
            model="claude-sonnet-5",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        raw_text = response.content[0].text
        task_graph = json.loads(raw_text)

        self.log(f"Generated {len(task_graph['steps'])} steps")
        return task_graph