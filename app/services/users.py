from app.services.models.errors import BadRequestError, NOT_FOUND_ERR
from app.repositories.users import UsersRepository
from app.services.helpers.try_except import try_except
from app.services.models.users import UserEntityCreate, UserRegister, UserEntity, Role, UserFilter
from app.services.models.base import Page


class UsersService:
    def __init__(self, users_repository: UsersRepository) -> None:
        self._users_repository = users_repository
    
    @try_except
    def get(self, id: int):
        user =  self._users_repository.get(id)

        if user is None:
            raise NOT_FOUND_ERR

        return user
    
    @try_except
    def get_list(self, filter: UserFilter) -> Page[UserEntity]:
        return self._users_repository.get_list(filter)
    
    @try_except
    def register(self, model: UserRegister) -> UserEntity:
        if model.password != model.password_repeat:
            raise BadRequestError('Password mismatch')
        
        if self._users_repository.get_by_username(model.username) is not None:
            raise BadRequestError('Username already exists')
        
        if self._users_repository.get_by_email(model.email) is not None:
            raise BadRequestError('Email already exists')

        new_user = UserEntityCreate(model.model_dump() | {
            'password_hash': bcrypt.hash(model.password),
            'role': Role.member,
        })

        new_user = self._users_repository.create(new_user)

        return new_user
