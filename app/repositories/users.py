from app.db.models.user import User
from app.services.models.users import UserEntity, UserEntityCreate, UserEntityWithPassword, UserFilter
from app.services.models.base import Page
from app.repositories.helpers.page import build_page


from sqlalchemy.orm.session import Session
from typing import Callable


class UsersRepository:
    def __init__(self, get_session: Callable[..., Session]) -> None:
        self._get_session = get_session

    
    def get_list(self, filter: UserFilter) -> Page[UserEntity]:
        with self._get_session() as session:
            q = session.query(User).filter(User.deleted_at == None)

            if filter.username:
                q = q.filter(User.username.ilike(f'%{filter.username}%'))
            
            if filter.email:
                q = q.filter(User.email.ilike(f'%{filter.email}%'))
            
            q = q.order_by(User.id.asc())

            return build_page(UserEntity, q, filter)

    
    def get(self, id: int) -> UserEntity | None:
        with self._get_session() as session:
            user = session.query(User).filter(
                User.id == id and
                User.deleted_at == None
            ).first()

            return UserEntity.model_validate(user) if user else None
    

    def get_by_username_with_password(self, username: str) -> UserEntityWithPassword | None:
        with self._get_session() as session:
            user = session.query(User).filter(
                User.username == username and
                User.deleted_at == None
            ).first()
        
            return UserEntityWithPassword.model_validate(user) if user else None


    def get_by_username(self, username: str) -> UserEntity | None:
        with self._get_session() as session:
            user = session.query(User).filter(
                User.username == username and
                User.deleted_at == None
            ).first()
        
            return UserEntity.model_validate(user) if user else None
    

    def get_by_email(self, email: str) -> UserEntity | None:
        with self._get_session() as session:
            user = session.query(User).filter(
                User.email == email and
                User.deleted_at == None
            ).first()

            return UserEntity.model_validate(user) if user else None
    

    def create(self, model: UserEntityCreate) -> UserEntity:
        with self._get_session() as session:
            user = User(**model.model_dump())
            session.add(user)
            session.commit()
            session.refresh(user)
            
            return UserEntity.model_validate(user)
