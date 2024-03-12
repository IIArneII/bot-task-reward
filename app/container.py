from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton, Configuration
from loguru import logger

from app.config import Config
from app.db.db import DataBase
from app.repositories.users import UsersRepository
from app.services.users import UsersService
from app.services.tasks import TasksService
from app.infrastructure.social_network import ISocialNetwork
from app.infrastructure.social_networks.instagram import Instagram
from app.infrastructure.social_networks.twitter import Twitter
from app.infrastructure.social_networks.youtube import YouTube


class Container(DeclarativeContainer):
    config: Config = Configuration()

    db: DataBase = Singleton(DataBase, config=config.db)
    
    users_repository = Factory(UsersRepository, get_session=db.provided.get_session)

    youtube: ISocialNetwork =Singleton(YouTube, config=config.sn.youtube)
    twitter: ISocialNetwork = Singleton(Twitter)
    instagram: ISocialNetwork = Singleton(Instagram, config=config.sn.instagram)

    users_service: UsersService = Factory(UsersService, users_repository=users_repository)
    tasks_service: TasksService = Factory(TasksService, users_repository=users_repository, twitter=twitter, instagram=instagram)


container : Container | None = None


def init_container(config: Config) -> None:
    logger.info('Container initialization...')

    global container
    container = Container()
    container.config.from_dict(config.model_dump())
    container.db()
    # container.instagram()
    container.youtube()


def get_container() -> Container:
    global container
    return container
