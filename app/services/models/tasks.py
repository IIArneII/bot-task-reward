from enum import Enum

from app.services.models.base import BaseModel


class SocialNetwork(str, Enum):
    instagram = 'instagram'
    twitter = 'twitter'
    telegram = 'telegram'
    discord = 'discord'
    youtube = 'youtube'
    tiktok = 'tiktok'

    @staticmethod
    def is_telegram(social_network: 'SocialNetwork'):
        return social_network == SocialNetwork.telegram
    
    @staticmethod
    def for_screenshot(social_network: 'SocialNetwork'):
        return social_network in (SocialNetwork.tiktok, SocialNetwork.youtube)


class Status(str, Enum):
    completed = 'completed'
    not_completed = 'not_completed'
    waiting_for_confirmation = 'waiting_for_confirmation'


class Task(BaseModel):
    social_network: SocialNetwork
    name: str
    description: str
    link: str
    bonuses: int


class TaskStatus(BaseModel):
    id: str
    status: Status
    screenshot_path: str | None = None


class TaskForUser(Task, TaskStatus):
    user_id: int
