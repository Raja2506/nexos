import json
from google import genai
from app.agents.base_agent import BaseAgent
from app.config import SETTINGS


class TaskSplitterAgent(BaseAgent):
    """
    Takes the Planner's flat step list and builds a dependency graph:
    which steps must finish before others can start, and which agent
    should handle each step.
    """

    def __init__(self):
        super().__init__(name="TaskSplitterAgent")
        self.client = genai.Client(api_key=SETTINGS["GEMINI_API_KEY"])

    async def run(self, input_data: dict) -> dict:
        steps = input_data["steps"]
        self.log(f"Splitting {len(steps)} steps into a dependency graph")

        prompt = f"""You are given a list of task steps. For each step, decide:
1. Which OTHER step IDs it depends on (must finish first) — use [] if none
2. Which agent type should handle it (choose from: research_agent, code_generator_agent, sql_agent, document_reader_agent, data_cleaning_agent, summarizer_agent)

Steps:
{json.dumps(steps)}

Return ONLY valid JSON in this exact format, no other text:
{{"nodes": [{{"id": "1", "description": "...", "depends_on": [], "agent_name": "..."}}]}}"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )


        raw_text = response.text.strip()
        # Gemini sometimes wraps JSON in ```json fences — strip them if present
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1].replace("json", "", 1).strip()

        graph = json.loads(raw_text)

        self._validate_no_cycles(graph["nodes"])
        self.log(f"Built graph with {len(graph['nodes'])} nodes")
        return graph

    def _validate_no_cycles(self, nodes: list) -> None:
        """Guard against circular dependencies (A needs B, B needs A) — this
        would freeze the orchestrator forever in Day 17."""
        graph = {n["id"]: n["depends_on"] for n in nodes}
        visited, visiting = set(), set()

        def visit(node_id):
            if node_id in visiting:
                raise ValueError(f"Circular dependency detected at node {node_id}")
            if node_id in visited:
                return
            visiting.add(node_id)
            for dep in graph.get(node_id, []):
                visit(dep)
            visiting.remove(node_id)
            visited.add(node_id)

        for node_id in graph:
            visit(node_id)