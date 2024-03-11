from loguru import logger
from TikTokApi import TikTokApi

from app.infrastructure.social_network import ISocialNetwork
from app.services.models.errors import AUTHORIZATION_FAILURE
from app.config import TikTokConfig


class TikTok(ISocialNetwork):
    def __init__(self, config: dict | TikTokConfig) -> None:
        self._config: TikTokConfig = config if type(config) is TikTokConfig else TikTokConfig(config)
        self._client = None
        self._check_user_id = 1

    async def create(self):
        api = TikTokApi()
        await api.create_sessions()
        user = await api.user(username='iiarneii').info()

        print(user)

    def check_user(self, user_name: str) -> bool:
        return True
