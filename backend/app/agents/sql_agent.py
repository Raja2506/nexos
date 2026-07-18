# backend/app/agents/sql_agent.py
import re
from google import genai
from sqlalchemy import text
from app.agents.base_agent import BaseAgent
from app.database import SessionLocal
from app.config import SETTINGS

FORBIDDEN_SQL_KEYWORDS = [
    "DELETE", "DROP", "UPDATE", "INSERT", "ALTER",
    "TRUNCATE", "GRANT", "REVOKE", "CREATE", "EXEC",
]


class SQLPermissionError(Exception):
    pass


class SQLAgent(BaseAgent):
    """
    Converts a plain-English question into a SQL SELECT query, validates
    it's read-only, runs it against the NexOS database, and returns rows.
    """

    def __init__(self):
        super().__init__(name="SQLAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])
        self.schema_description = """
Tables:
- users(id, email, name, auth_provider, created_at)
- tasks(id, user_id, goal_text, status, created_at, completed_at)
- task_nodes(id, task_id, agent_name, depends_on, status, output_json,
             confidence_score, execution_time_ms, tokens_used, cost_usd)
"""

    async def run(self, input_data: dict) -> dict:
        question = input_data["question"]
        self.log(f"Answering with SQL: {question}")

        sql_query = await self._generate_sql(question)
        self._validate_read_only(sql_query)

        rows = self._execute_query(sql_query)
        self.log(f"Query returned {len(rows)} rows")
        return {"question": question, "sql": sql_query, "rows": rows}

    async def _generate_sql(self, question: str) -> str:
        prompt = f"""Given this database schema:
{self.schema_description}

Write a single PostgreSQL SELECT query to answer this question:
{question}

Rules:
- ONLY a SELECT statement, nothing else
- Return ONLY the raw SQL, no markdown fences, no explanation
- Never modify data (no INSERT/UPDATE/DELETE/DROP)"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        sql = response.text.strip()
        if sql.startswith("```"):
            sql = sql.split("```")[1].replace("sql", "", 1).strip()
        return sql

    def _validate_read_only(self, sql_query: str) -> None:
        normalized = sql_query.upper()

        if not normalized.strip().startswith("SELECT"):
            raise SQLPermissionError("Only SELECT queries are allowed")

        for keyword in FORBIDDEN_SQL_KEYWORDS:
            if re.search(rf"\b{keyword}\b", normalized):
                raise SQLPermissionError(f"Blocked forbidden keyword: {keyword}")

    def _execute_query(self, sql_query: str) -> list:
        db = SessionLocal()
        try:
            result = db.execute(text(sql_query))
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]
        finally:
            db.close()