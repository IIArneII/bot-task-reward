from app.db.models.base import SoftDeletedBaseModel
from app.services.enums.users import Role

from sqlalchemy import Column, String, Enum, Integer, CheckConstraint


class User(SoftDeletedBaseModel):
    __tablename__ = 'users'

    email = Column(String, unique=True, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.member, server_default=Role.member)
    balance = Column(Integer, CheckConstraint('balance >= 0'), nullable=False, server_default='0', default=0)
