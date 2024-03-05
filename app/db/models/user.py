from app.db.models.base import BaseModel

from sqlalchemy import Column, Integer, CheckConstraint, JSON


class User(BaseModel):
    __tablename__ = 'users'

    balance = Column(Integer, CheckConstraint('balance >= 0'), nullable=False, server_default='0', default=0)
    tasks = Column(JSON, nullable=False, server_default='[]', default=[])
