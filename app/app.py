from typing import Tuple
from loguru import logger
from sys import stderr
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import Config, LogConfig, BotConfig
from app.container import init_container
from app.controllers.base import router


async def create_app(config: Config) -> Tuple[Bot, Dispatcher]:
    init_logger(config.log)
    init_container(config)
    bot, dp = await init_bot(config.bot)

    return bot, dp


def init_logger(config: LogConfig) -> None:
    logger.remove()
    logger.add(stderr, level=config.LEVEL.upper())
    
    if config.DIR:
        logger.add(
            f'{config.DIR}/logs.log',
            compression='zip',
            rotation=f'{config.ROTATION} MB',
            retention=config.RETENTION,
            level=config.LEVEL.upper()
        )


async def init_bot(config: BotConfig) -> Tuple[Bot, Dispatcher]:
    logger.info('Bot initialization...')

    bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    return bot, dp
