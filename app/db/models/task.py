from app.db.models.base import SoftDeletedBaseModel
from app.services.enums.tasks import TaskType

from sqlalchemy import Column, String, Enum, Integer, CheckConstraint


class Task(SoftDeletedBaseModel):
    __tablename__ = 'tasks'

    type = Column(Enum(TaskType), nullable=False, default=TaskType.base, server_default=TaskType.base)
    link = Column(String, nullable=False)
    description = Column(String, nullable=True)
    points = Column(Integer, CheckConstraint('points >= 0'), nullable=False, default=0, server_default='0')
