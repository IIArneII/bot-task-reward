from enum import Enum

from app.services.models.base import BaseModel


class SocialNetwork(str, Enum):
    instagram = 'instagram'
    twitter = 'twitter'
    telegram = 'telegram'
    discord = 'discord'


class Task(BaseModel):
    social_network: SocialNetwork
    name: str
    description: str
    link: str
    bonuses: int


class TaskForUser(Task):
    id: str
    is_done: bool
