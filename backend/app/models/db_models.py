from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    auth_provider = Column(String)
    hashed_password = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    goal_text = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending|running|completed|failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="tasks")
    nodes = relationship("TaskNode", back_populates="task")


class TaskNode(Base):
    __tablename__ = "task_nodes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, ForeignKey("tasks.id"))
    agent_name = Column(String, nullable=False)
    depends_on = Column(ARRAY(String), default=[])
    status = Column(String, default="pending")
    output_json = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    cost_usd = Column(Float, nullable=True)

    task = relationship("Task", back_populates="nodes")