from app.services.models.base import BaseModel, EntityBaseModel, BaseFilter, Page
from app.services.enums.users import Role

from pydantic import Field, EmailStr


class UserEntity(EntityBaseModel):
    username: str
    email: EmailStr
    name: str
    role: Role


class UserFilter(BaseFilter):
    username: str | None = None
    email: str | None = None


class UserEntityWithPassword(UserEntity):
    password_hash: str


class UserEntityCreate(BaseModel):
    username: str
    email: EmailStr
    name: str
    role: Role
    password_hash: str


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    name: str
    password: str = Field(min_length=8)
    password_repeat: str = Field(min_length=8)
