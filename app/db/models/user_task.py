from app.db.models.base import BaseModel
from app.services.enums.tasks import TaskStatus

from sqlalchemy import Column, DateTime, Enum, Integer, CheckConstraint, ForeignKey


class UserTask(BaseModel):
    __tablename__ = 'user_tasks'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    points = Column(Integer, CheckConstraint('points >= 0'), nullable=False)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.started, server_default=TaskStatus.started)
    checked_at = Column(DateTime, nullable=True)
