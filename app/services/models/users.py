from enum import Enum 

from app.services.models.base import BaseModel, EntityBaseModel


class Role(str, Enum):
    client = 'client'
    admin = 'admin'


class User(EntityBaseModel):
    balance: int
    role: Role
    tasks: list[str]


class UserCreate(BaseModel):
    id: int


class UserUpdate(BaseModel):
    balance: int | None = None
    tasks: list[str] | None = None
