from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from app.security.rate_limiter import rate_limit_dependency
from app.security.audit_log import log_action
from app.database import get_db

router = APIRouter(prefix="/api", tags=["tasks"])


class TaskCreateRequest(BaseModel):
    goal_text: str


@router.post("/tasks", dependencies=[Depends(rate_limit_dependency)])
async def create_task(payload: TaskCreateRequest, request: Request, db: Session = Depends(get_db)):
    task_id = str(uuid.uuid4())

    log_action(
        db,
        action="create_task",
        resource=task_id,
        ip_address=request.client.host,
    )

    return {"task_id": task_id, "goal_text": payload.goal_text, "status": "pending"}