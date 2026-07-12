# backend/app/agents/code_generator_agent.py
from google import genai
from app.agents.base_agent import BaseAgent
from app.config import SETTINGS


class CodeGeneratorAgent(BaseAgent):
    """
    Takes a plain-English task description and generates working Python
    code to solve it. Does NOT execute the code — that's the sandbox's job.
    """

    def __init__(self):
        super().__init__(name="CodeGeneratorAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])

    async def run(self, input_data: dict) -> dict:
        task = input_data["task"]
        self.log(f"Generating code for: {task}")

        prompt = f"""Write a Python script to accomplish this task:
{task}

Rules:
- Return ONLY the Python code, no explanations, no markdown fences
- The script must print its final result using print()
- Do not use any file I/O, network calls, or system commands
- Keep it under 30 lines"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )

        code = response.text.strip()
        # Strip markdown fences if the model added them anyway
        if code.startswith("```"):
            code = code.split("```")[1]
            code = code.replace("python", "", 1).strip()

        self.log(f"Generated {len(code.splitlines())} lines of code")
        return {"task": task, "code": code}