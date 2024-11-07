from enum import Enum 

from app.services.models.base import BaseModel, EntityBaseModel
from app.services.models.tasks import TaskStatus


class Role(str, Enum):
    client = 'client'
    admin = 'admin'


class User(EntityBaseModel):
    balance: int
    role: Role
    tasks: list[TaskStatus]


class UserCreate(BaseModel):
    id: int


class UserUpdate(BaseModel):
    balance: int | None = None
    tasks: list[TaskStatus] | None = None
