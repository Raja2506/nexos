from typing import TypedDict, Optional, List


class NexOSState(TypedDict):
    """
    The shared 'memory' that flows through every node in the graph.
    Each agent reads what it needs from here and writes its result
    back in, so the next agent can use it.
    """
    goal: str
    plan_steps: Optional[List[dict]]
    task_type: Optional[str]
    raw_data: Optional[list]
    cleaned_data: Optional[list]
    chart_path: Optional[str]
    qa_score: Optional[int]
    qa_passed: Optional[bool]
    final_report: Optional[str]
    error: Optional[str]