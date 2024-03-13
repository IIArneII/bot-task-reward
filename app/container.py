from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton, Configuration, Resource
from aiogram import Bot, Dispatcher
from loguru import logger

from app.config import Config
from app.db.db import DataBase
from app.repositories.users import UsersRepository
from app.services.users import UsersService
from app.services.tasks import TasksService
from app.bot import init_bot, init_dispatcher
from app.infrastructure.social_network import ISocialNetwork
from app.infrastructure.social_networks.instagram import Instagram
from app.infrastructure.social_networks.twitter import Twitter
from app.infrastructure.social_networks.telegram import Telegram
from app.infrastructure.social_networks.discord import Discord


class Container(DeclarativeContainer):
    config: Config = Configuration()

    db: DataBase = Singleton(DataBase, config=config.db)
    
    users_repository: UsersRepository = Factory(UsersRepository, get_session=db.provided.get_session)

    dispatcher: Dispatcher = Resource(init_dispatcher)
    bot: Bot = Resource(init_bot, config=config.bot)

    discord: ISocialNetwork = Singleton(Discord, config=config.sn.discord)
    telegram: ISocialNetwork = Singleton(Telegram, config=config.sn.telegram, bot=bot)
    twitter: ISocialNetwork = Singleton(Twitter)
    instagram: ISocialNetwork = Singleton(Instagram, config=config.sn.instagram)

    users_service: UsersService = Factory(UsersService, users_repository=users_repository)
    tasks_service: TasksService = Factory(
        TasksService,
        users_repository=users_repository,
        twitter=twitter, instagram=instagram,
        telegram=telegram,
        discord=discord,
    )


container : Container | None = None


async def init_container(config: Config) -> Container:
    logger.info('Container initialization...')

    global container
    container = Container()
    container.config.from_dict(config.model_dump())

    container.dispatcher()
    b = await container.bot()
    container.db()
    container.instagram()
    container.telegram()
    container.discord()

    return container


def get_container() -> Container:
    global container
    return container
