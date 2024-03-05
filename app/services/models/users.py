from app.services.models.base import BaseModel, EntityBaseModel


class User(EntityBaseModel):
    balance: int
    tasks: list[str]


class UserCreate(BaseModel):
    id: int


class UserUpdate(BaseModel):
    balance: int | None = None
    tasks: list[str] | None = None
