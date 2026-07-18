from langgraph.graph import StateGraph, START, END
from app.orchestration.state import NexOSState
from app.orchestration.router import route_after_decision
from app.orchestration.nodes import (
    plan_node,
    decide_task_type_node,
    sql_node,
    clean_data_node,
    qa_node,
    report_node,
)


def build_graph():
    builder = StateGraph(NexOSState)

    builder.add_node("plan_node", plan_node)
    builder.add_node("decide_task_type_node", decide_task_type_node)
    builder.add_node("sql_node", sql_node)
    builder.add_node("clean_data_node", clean_data_node)
    builder.add_node("qa_node", qa_node)
    builder.add_node("report_node", report_node)

    builder.add_edge(START, "plan_node")
    builder.add_edge("plan_node", "decide_task_type_node")

    builder.add_conditional_edges(
        "decide_task_type_node",
        route_after_decision,
        {"sql_node": "sql_node", "report_node": "report_node"},
    )

    builder.add_edge("sql_node", "clean_data_node")
    builder.add_edge("clean_data_node", "qa_node")
    builder.add_edge("qa_node", "report_node")
    builder.add_edge("report_node", END)

    return builder.compile()