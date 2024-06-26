from typing import BinaryIO
from loguru import logger
from os.path import join, splitext
from uuid import uuid4

from app.repositories.users import UsersRepository
from app.infrastructure.social_network import ISocialNetwork
from app.infrastructure.file_manager import FileManager
from app.services.models.errors import NOT_FOUND_ERR, ALREADY_DONE, UNKNOWN_SOCIAL_NETWORK, NOT_FOR_SCREENSHOT, FORBIDDEN_ERR
from app.services.helpers.try_except import try_except
from app.services.models.tasks import Task, TaskStatus, TaskForUser, SocialNetwork, Status
from app.services.models.users import UserUpdate, Role


tasks = {
    'discord.subscribe': Task(
        social_network=SocialNetwork.discord,
        name='Вступить в дискорд',
        description='Вам необходимо присоединиться к серверу в дискорде',
        link='https://discord.gg/X2WsFPHHq9',
        bonuses=100,
    ),
    'telegram.subscribe': Task(
        social_network=SocialNetwork.telegram,
        name='Подписаться на телеграм',
        description='Вам необходимо подписаться на телеграм',
        link='https://t.me/mango_arne',
        bonuses=100,
    ),
    # 'twitter.subscribe': Task(
    #     social_network=SocialNetwork.twitter,
    #     name='Подписаться на твиттер',
    #     description='Вам необходимо подписаться на твиттер',
    #     link='https://twitter.com/DiscoverMag',
    #     bonuses=20,
    # ),
    'instagram.subscribe': Task(
        social_network=SocialNetwork.instagram,
        name='Подписаться на инстаграм',
        description='Вам необходимо подписаться на инстаграм',
        link='https://www.instagram.com/gzed_2001',
        bonuses=10,
    ),
    'youtube.subscribe': Task(
        social_network=SocialNetwork.youtube,
        name='Подписаться на ютуб',
        description='Вам необходимо подписаться на канал в ютубе',
        link='https://www.youtube.com/channel/UC-j1rIfnJkdzxs792FKS-PA',
        bonuses=30,
    ),
    'tiktok.subscribe': Task(
        social_network=SocialNetwork.tiktok,
        name='Подписаться на ТикТок',
        description='Вам необходимо подписаться на ТикТок',
        link='https://www.tiktok.com/@iitztimmy?_t=8lBhWpEbvHu&_r=1',
        bonuses=30,
    ),
}


def get_task_status(tasks: list[TaskStatus], id: str) -> TaskStatus:
    status = TaskStatus(id=id, status=Status.not_completed)
    for i in tasks:
        if i.id == id:
            status = i
            break
    return status


def set_task_status(tasks: list[TaskStatus], set_task: TaskStatus) -> list[TaskStatus]:
    for i, v in enumerate(tasks):
        if v.id == set_task.id:
            tasks[i] = set_task
            return tasks
    tasks.append(set_task)
    return tasks


class TasksService:
    def __init__(
            self,
            users_repository: UsersRepository,
            twitter: ISocialNetwork,
            instagram: ISocialNetwork,
            telegram: ISocialNetwork,
            discord: ISocialNetwork,
            file_manager: FileManager,
        ) -> None:
        self._users_repository = users_repository
        self._twitter = twitter
        self._instagram = instagram
        self._telegram = telegram
        self._discord = discord
        self._file_manager = file_manager
    
    def _get_social_network(self, name: SocialNetwork) -> ISocialNetwork:
        if name == SocialNetwork.twitter:
            return self._twitter
        if name == SocialNetwork.instagram:
            return self._instagram
        if name == SocialNetwork.telegram:
            return self._telegram
        if name == SocialNetwork.discord:
            return self._discord
        raise UNKNOWN_SOCIAL_NETWORK


    @try_except
    def get(self, user_id: str, id: str) -> TaskForUser:
        task = tasks.get(id)
        if task is None:
            raise NOT_FOUND_ERR
        
        user =  self._users_repository.get(user_id)
        if user is None:
            raise NOT_FOUND_ERR

        return TaskForUser(
            id=id,
            social_network=task.social_network,
            name=task.name,
            description=task.description,
            link=task.link,
            bonuses=task.bonuses,
            status=get_task_status(user.tasks, id).status,
            screenshot_path=get_task_status(user.tasks, id).screenshot_path,
            user_id=user_id,
        )

    @try_except
    def get_list(self, user_id: int) -> list[TaskForUser]:
        user =  self._users_repository.get(user_id)
        if user is None:
            raise NOT_FOUND_ERR
        
        tasks_for_user = [TaskForUser(
            id=i,
            social_network=v.social_network,
            name=v.name,
            description=v.description,
            link=v.link,
            bonuses=v.bonuses,
            status=get_task_status(user.tasks, i).status,
            screenshot_path=get_task_status(user.tasks, i).screenshot_path,
            user_id=user_id
        ) for i, v in tasks.items()]

        return tasks_for_user


    @try_except
    async def check_user_name(self, user_id: int, id: str, user_name: str) -> bool:
        task = tasks.get(id)
        if task is None:
            raise NOT_FOUND_ERR

        user =  self._users_repository.get(user_id)
        if user is None:
            raise NOT_FOUND_ERR

        if id in user.tasks:
            raise ALREADY_DONE

        social_network = self._get_social_network(task.social_network)
        
        return not await social_network.check_user(user_name)


    @try_except
    async def check_execution(self, user_id: int, id: str, user_name: str) -> bool:
        task = tasks.get(id)
        if task is None:
            raise NOT_FOUND_ERR

        user = self._users_repository.get(user_id)
        if user is None:
            raise NOT_FOUND_ERR
        
        if id in user.tasks:
            raise ALREADY_DONE

        social_network = self._get_social_network(task.social_network)
        if not await social_network.check_user(user_name):
            return False

        user = self._users_repository.update(user.id, UserUpdate(
            balance=user.balance+task.bonuses,
            tasks=set_task_status(user.tasks, TaskStatus(
                id=id,
                status=Status.completed,
            ))
        ))

        if user is None:
            raise NOT_FOUND_ERR

        return True

    @try_except
    async def save_screenshot(self, user_id: int, id: str, file_id: str) -> None:
        task = tasks.get(id)
        if task is None:
            raise NOT_FOUND_ERR
        
        user = self._users_repository.get(user_id)
        if user is None:
            raise NOT_FOUND_ERR
        
        if id in user.tasks:
            raise ALREADY_DONE
        
        if not SocialNetwork.for_screenshot(task.social_network):
            raise NOT_FOR_SCREENSHOT

        self._users_repository.update(user_id, UserUpdate(
            tasks=set_task_status(user.tasks, TaskStatus(
                id=id,
                status=Status.waiting_for_confirmation,
                screenshot_path=file_id,
            ))
        ))

    @try_except
    async def get_for_checking(self, user_id: int) -> TaskForUser | None:
        user = self._users_repository.get(user_id)
        if user is None:
            raise NOT_FOUND_ERR
        
        if user.role != Role.admin:
            raise FORBIDDEN_ERR

        user = self._users_repository.get_waiting_for_confirmation()
        if user is None:
            return None
        
        task_status: TaskStatus | None = None
        for i in user.tasks:
            if i.status == Status.waiting_for_confirmation and i.id in tasks:
                task_status = i

        task = tasks.get(task_status.id)

        return TaskForUser(
            id=task_status.id,
            status=task_status.status,
            screenshot_path=task_status.screenshot_path,
            social_network=task.social_network,
            name=task.name,
            description=task.description,
            link=task.link,
            bonuses=task.bonuses,
            user_id=user.id,
        )
    
    @try_except
    async def approve(self, user_id: int, id: str, for_user_id: int, completed: bool) -> tuple[Task, bool]:
        task = tasks.get(id)
        if task is None:
            raise NOT_FOUND_ERR

        user = self._users_repository.get(user_id)
        if user is None:
            raise NOT_FOUND_ERR
        
        if user.role != Role.admin:
            raise FORBIDDEN_ERR
        
        user = self._users_repository.get(for_user_id)
        if user is None:
            raise NOT_FOUND_ERR
        
        task_status = get_task_status(user.tasks, id)
        if task_status.status != Status.waiting_for_confirmation:
            return task, False, False

        status = Status.not_completed
        if completed:
            status = Status.completed
        
        self._users_repository.update(user_id, UserUpdate(
            balance=user.balance + task.bonuses,
            tasks=set_task_status(user.tasks, TaskStatus(
                id=id,
                status=status,
            ))
        ))

        return task, True, status == Status.completed
