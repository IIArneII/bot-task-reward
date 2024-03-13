from asyncio import create_task
from discord import Client, Guild, Intents
from loguru import logger

from app.infrastructure.social_network import ISocialNetwork
from app.config import DiscordConfig


class Discord(ISocialNetwork):
    def __init__(self, config: dict | DiscordConfig) -> None:
        logger.info('Discord initialization...')

        self._config: DiscordConfig = config if type(config) is DiscordConfig else DiscordConfig(config)
        intents = Intents.default()
        intents.members = True
        self._client = Client(intents=intents)
        self._guild: Guild | None = None

        create_task(self._start())

    async def _start(self):
        logger.info('Discord running...')
        await self._client.start(self._config.TOKEN)
        logger.info('Discord stopped')

    async def check_user(self, user_name: str | int) -> bool:
        if self._guild is None:
            self._guild = self._client.get_guild(self._config.GUILD)
            if self._guild is None:
                logger.warning(f'Could not find discord guild {self._config.GUILD}')
                return False

        if self._guild.get_member_named(user_name):
            return True
        
        return False
