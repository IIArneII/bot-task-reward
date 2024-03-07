from app.repositories.users import UsersRepository
from app.infrastructure.social_network import ISocialNetwork
from app.services.models.errors import NOT_FOUND_ERR, ALREADY_DONE, UNKNOWN_SOCIAL_NETWORK
from app.services.helpers.try_except import try_except
from app.services.models.tasks import Task, TaskForUser, SocialNetwork
from app.services.models.users import UserUpdate


tasks = {
    'twitter.subscribe': Task(
        social_network=SocialNetwork.twitter,
        name='Подписаться на твиттер',
        description='Вам необходимо подписаться на твиттер',
        link='https://twitter.com/DiscoverMag',
        bonuses=20,
    ),
    'instagram.subscribe': Task(
        social_network=SocialNetwork.instagram,
        name='Подписаться на инстаграм',
        description='Вам необходимо подписаться на инстаграм',
        link='https://www.instagram.com/gzed_2001',
        bonuses=10,
    ),
}


class TasksService:
    def __init__(self, users_repository: UsersRepository, twitter: ISocialNetwork, instagram: ISocialNetwork) -> None:
        self._users_repository = users_repository
        self._twitter = twitter
        self._instagram = instagram
    
    def _get_social_network(self, name: SocialNetwork) -> ISocialNetwork:
        if name == SocialNetwork.twitter:
            return self._twitter
        if name == SocialNetwork.instagram:
            return self._instagram
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
            is_done=id in user.tasks,
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
            is_done=i in user.tasks,
        ) for i, v in tasks.items()]

        return tasks_for_user


    @try_except
    def check_user_name(self, user_id: int, id: str, user_name: str) -> bool:
        task = tasks.get(id)
        if task is None:
            raise NOT_FOUND_ERR

        user =  self._users_repository.get(user_id)
        if user is None:
            raise NOT_FOUND_ERR

        if id in user.tasks:
            raise ALREADY_DONE

        social_network = self._get_social_network(task.social_network)
        
        return not social_network.check_user(user_name)


    @try_except
    def check_execution(self, user_id: int, id: str, user_name: str) -> bool:
        task = tasks.get(id)
        if task is None:
            raise NOT_FOUND_ERR

        user = self._users_repository.get(user_id)
        if user is None:
            raise NOT_FOUND_ERR
        
        if id in user.tasks:
            raise ALREADY_DONE

        social_network = self._get_social_network(task.social_network)
        if not social_network.check_user(user_name):
            return False

        user = self._users_repository.update(user.id, UserUpdate(
            balance=user.balance+task.bonuses,
            tasks=user.tasks+[id]
        ))

        if user is None:
            raise NOT_FOUND_ERR

        return True
