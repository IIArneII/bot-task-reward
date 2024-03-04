from app.services.models.base import BaseModel, EntityBaseModel, BaseFilter
from app.services.enums.users import Role

from pydantic import EmailStr


class User(EntityBaseModel):
    email: EmailStr
    role: Role
    balance: int


class UserFilter(BaseFilter):
    email: str | None = None


class UserCreate(BaseModel):
    id: int
    email: EmailStr


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role: Role | None = None
    balance: int | None = None
