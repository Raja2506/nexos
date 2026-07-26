from fastapi import APIRouter, Depends
from pydantic import BaseModel
import uuid

from app.security.rate_limiter import rate_limit_dependency

router = APIRouter(prefix="/api", tags=["tasks"])


class TaskCreateRequest(BaseModel):
    goal_text: str


@router.post("/tasks", dependencies=[Depends(rate_limit_dependency)])
async def create_task(payload: TaskCreateRequest):
    task_id = str(uuid.uuid4())
    return {"task_id": task_id, "goal_text": payload.goal_text, "status": "pending"}