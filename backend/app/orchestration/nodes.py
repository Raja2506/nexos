from app.orchestration.state import NexOSState
from app.agents.planner_agent import PlannerAgent
from app.agents.sql_agent import SQLAgent
from app.agents.data_cleaning_agent import DataCleaningAgent
from app.agents.qa_agent import QAAgent
from app.agents.report_generator_agent import ReportGeneratorAgent
from app.agents.decision_agent import DecisionAgent


async def plan_node(state: NexOSState) -> dict:
    agent = PlannerAgent()
    result = await agent.run({"goal": state["goal"]})
    return {"plan_steps": result["steps"]}


async def decide_task_type_node(state: NexOSState) -> dict:
    agent = DecisionAgent()
    result = await agent.run({
        "situation": state["goal"],
        "options": ["sql", "no_data_needed"],
    })
    return {"task_type": result["chosen_option"]}


async def sql_node(state: NexOSState) -> dict:
    agent = SQLAgent()
    result = await agent.run({"question": state["goal"]})
    return {"raw_data": result["rows"]}


async def clean_data_node(state: NexOSState) -> dict:
    agent = DataCleaningAgent()
    result = await agent.run({"rows": state["raw_data"]})
    return {"cleaned_data": result["cleaned_rows"]}


async def qa_node(state: NexOSState) -> dict:
    agent = QAAgent()
    content_preview = str(state["cleaned_data"])[:500]
    result = await agent.run({
        "content": content_preview,
        "fact_check_verdict": "supported",
        "review_issues": [],
    })
    return {"qa_score": result["score"], "qa_passed": result["passed"]}


async def report_node(state: NexOSState) -> dict:
    agent = ReportGeneratorAgent()
    result = await agent.run({
        "title": f"Report: {state['goal']}",
        "sections": [
            {"heading": "Data", "content": str(state.get("cleaned_data", "N/A"))},
            {"heading": "QA Score", "content": f"{state.get('qa_score', 'N/A')}/10"},
        ],
    })
    return {"final_report": result["report"]}