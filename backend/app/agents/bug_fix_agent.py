# backend/app/agents/bug_fix_agent.py
from google import genai
from app.agents.base_agent import BaseAgent
from app.agents.sandbox_executor import run_code_safely, SandboxExecutionError
from app.config import SETTINGS


class BugFixAgent(BaseAgent):
    """
    Takes code that failed in the sandbox, sends the error back to the
    LLM, and asks it to fix the bug. Retries up to max_attempts times.
    """

    def __init__(self):
        super().__init__(name="BugFixAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])

    async def run(self, input_data: dict) -> dict:
        code = input_data["code"]
        max_attempts = input_data.get("max_attempts", 3)

        for attempt in range(1, max_attempts + 1):
            try:
                output = run_code_safely(code)
                self.log(f"Code ran successfully on attempt {attempt}")
                return {"code": code, "output": output, "attempts": attempt}
            except SandboxExecutionError as e:
                self.log(f"Attempt {attempt} failed: {e}")
                if attempt == max_attempts:
                    raise
                code = await self._fix_code(code, str(e))

        raise SandboxExecutionError("Exhausted all fix attempts")

    async def _fix_code(self, broken_code: str, error_message: str) -> str:
        prompt = f"""This Python code failed with an error. Fix it.

Code:
{broken_code}

Error:
{error_message}

Return ONLY the corrected Python code, no explanations, no markdown fences."""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        fixed_code = response.text.strip()
        if fixed_code.startswith("```"):
            fixed_code = fixed_code.split("```")[1].replace("python", "", 1).strip()
        return fixed_code