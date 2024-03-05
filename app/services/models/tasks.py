from app.services.models.base import BaseModel


class Task(BaseModel):
    name: str
    description: str
    link: str
    bonuses: int


class TaskForUser(Task):
    id: str
    is_done: bool
