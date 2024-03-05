from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton, Configuration
from loguru import logger

from app.config import Config
from app.db.db import DataBase
from app.repositories.users import UsersRepository
from app.services.users import UsersService
from app.services.tasks import TasksService


class Container(DeclarativeContainer):
    config: Config = Configuration()

    db: DataBase = Singleton(DataBase, config=config.db)
    
    users_repository = Factory(UsersRepository, get_session=db.provided.get_session)

    users_service: UsersService = Factory(UsersService, users_repository=users_repository)
    tasks_service: TasksService = Factory(TasksService, users_repository=users_repository)


container : Container | None = None


def init_container(config: Config) -> None:
    logger.info('Container initialization...')

    global container
    container = Container()
    container.config.from_dict(config.model_dump())
    container.db()


def get_container() -> Container:
    global container
    return container
