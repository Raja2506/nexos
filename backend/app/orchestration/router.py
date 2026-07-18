from app.orchestration.state import NexOSState


def route_after_decision(state: NexOSState) -> str:
    """
    Reads state and returns the NAME of the next node to visit.
    This is how the graph 'branches' based on DecisionAgent's choice.
    """
    if state["task_type"] == "sql":
        return "sql_node"
    return "report_node"