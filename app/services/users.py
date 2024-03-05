from app.services.models.errors import NOT_FOUND_ERR
from app.repositories.users import UsersRepository
from app.services.helpers.try_except import try_except
from app.services.models.users import UserCreate, User


class UsersService:
    def __init__(self, users_repository: UsersRepository) -> None:
        self._users_repository = users_repository
    
    @try_except
    def get(self, id: int) -> User:
        user =  self._users_repository.get(id)

        if user is None:
            raise NOT_FOUND_ERR

        return user
    
    @try_except
    def register(self, model: UserCreate) -> User:
        user = self._users_repository.get(model.id)
        if user:
            return user

        return self._users_repository.create(model)
