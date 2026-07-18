# backend/app/agents/python_agent.py
from google import genai
from app.agents.base_agent import BaseAgent
from app.agents.sandbox_executor import run_code_safely, SandboxExecutionError
from app.config import SETTINGS


class PythonAgent(BaseAgent):
    """
    Generates and runs general-purpose Python code (data transforms,
    calculations) using the same sandbox built in Day 10.
    """

    def __init__(self):
        super().__init__(name="PythonAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])

    async def run(self, input_data: dict) -> dict:
        task = input_data["task"]
        self.log(f"Running Python task: {task}")

        prompt = f"""Write a Python script to accomplish this task:
{task}

Rules:
- Return ONLY the Python code, no explanations, no markdown fences
- Must print the final result using print()
- No file I/O, no network calls, no system commands
- Keep it under 30 lines"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        code = response.text.strip()
        if code.startswith("```"):
            code = code.split("```")[1].replace("python", "", 1).strip()

        try:
            output = run_code_safely(code)
        except SandboxExecutionError as e:
            self.log(f"Execution failed: {e}")
            raise

        return {"task": task, "code": code, "output": output}