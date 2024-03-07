from typing import Tuple
from loguru import logger
from sys import stderr
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import GetUpdates, SendMessage

from app.config import Config, LogConfig, BotConfig
from app.container import init_container
from app.controllers.base import base_router
from app.controllers.tasks import tasks_router


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
    async def middleware(make_request, bot: Bot, method: SendMessage):
        if type(method) not in [GetUpdates]:
            if type(method) is SendMessage:
                msg = method.text.replace('\n', '')
                logger.info(f"Send message. Chat id: {method.chat_id}. Message: {msg}")
            else:
                logger.info(f"Method: {type(method)}")
        
        return await make_request(bot, method)

    logger.info('Bot initialization...')

    bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)
    bot.session.middleware(middleware)

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(base_router)
    dp.include_router(tasks_router)

    await bot.delete_webhook(drop_pending_updates=True)

    return bot, dp
