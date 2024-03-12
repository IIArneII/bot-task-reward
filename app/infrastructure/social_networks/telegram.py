from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from loguru import logger

from app.infrastructure.social_network import ISocialNetwork
from app.config import TelegramConfig


class Telegram(ISocialNetwork):
    def __init__(self, config: dict | TelegramConfig, bot: Bot) -> None:
        logger.info('Telegram initialization...')

        self._config: TelegramConfig = config if type(config) is TelegramConfig else TelegramConfig(config)
        self._bot = bot

        if self._config.CHANNEL and self._config.CHANNEL[0] != '@':
            self._config.CHANNEL = f'@{self._config.CHANNEL}'
    
    async def check_user(self, user_name: str | int) -> bool:
        user = await self._bot.get_chat_member(self._config.CHANNEL, int(user_name))

        if user.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
            return True

        return False
