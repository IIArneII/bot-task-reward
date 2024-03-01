from fastapi import APIRouter, Depends, Query

from app.controllers.api.helpers.responses import OK, NOT_FOUND, BAD_REQUEST, FORBIDDEN
from app.controllers.api.helpers.services_providers import users_service
from app.controllers.api.helpers.profile import Profile
from app.controllers.api.helpers.filters import user_filter
from app.services.users import UsersService
from app.services.models.users import UserRegister, UserEntity, UserFilter
from app.services.models.base import Page, BaseFilter


users_api = APIRouter(
    prefix='/users',
    tags=['users']
)


@users_api.post('/register', responses= OK | BAD_REQUEST)
def register(model: UserRegister, users_service: UsersService = Depends(users_service)) -> UserEntity:
    '''
    Register of a new client
    '''
    return users_service.register(model)


@users_api.get('/me', responses= OK | FORBIDDEN)
def get_me(profile: UserEntity = Depends(Profile()), users_service: UsersService = Depends(users_service)) -> UserEntity:
    '''
    Get yourself
    '''
    return users_service.get(profile.id)


@users_api.get("", responses= OK)
def get_list(filter: UserFilter = Depends(user_filter), users_service: UsersService = Depends(users_service)) -> Page[UserEntity]:
    '''
    Get users list
    '''    
    return users_service.get_list(filter)


@users_api.get('/{id}', responses= OK | NOT_FOUND)
def get(id: int, users_service: UsersService = Depends(users_service)) -> UserEntity:
    '''
    Get user by ID
    '''
    return users_service.get(id)
