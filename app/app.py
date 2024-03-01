from typing import Tuple
from loguru import logger
from sys import stderr
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import Config, LogConfig, BotConfig, APIConfig
from app.container import Container
from app.services.models.errors import NotFoundError, BadRequestError, ForbiddenError
from app.controllers.bot.base import router
from app.controllers.api.helpers.responses import INTERNAL_SERVER_ERROR
from app.controllers.api.helpers import exception_handlers
from app.controllers.api.users import users_api


async def create_app(config: Config) -> FastAPI:
    _init_logger(config.log)

    container = Container()
    container.config.from_dict(config.model_dump())

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield

    global_api = FastAPI(
        debug=config.app.DEBUG,
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan
    )
    global_api.container = container

    _init_api(global_api, config)

    return global_api


def _init_logger(config: LogConfig):
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


def _init_api(global_api: FastAPI, config: APIConfig, debug: bool=False):
    logger.info('Routes initialization...')

    api_v1 = FastAPI(
        debug=debug,
        version=config.VERSION,
        title=f'{config.TITLE} V1',
        summary=config.SUMMARY,
        description=config.DESCRIPTION,
        docs_url='/openapi' if config.IS_VISIBLE else None,
        redoc_url=None,
        responses=INTERNAL_SERVER_ERROR,
    )

    api_v1.add_exception_handler(NotFoundError, exception_handlers.not_found_handler)
    api_v1.add_exception_handler(BadRequestError, exception_handlers.bad_request_handler)
    api_v1.add_exception_handler(ForbiddenError, exception_handlers.forbidden_handler)
    api_v1.add_exception_handler(HTTPException, exception_handlers.http_error_handler)
    api_v1.add_exception_handler(Exception, exception_handlers.internal_server_error_handler)

    api_v1.include_router(users_api)
    
    global_api.mount(f'{config.PREFIX}/v1', api_v1)


async def _init_bot(config: BotConfig) -> Tuple[Bot, Dispatcher]:
    bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    return bot, dp
