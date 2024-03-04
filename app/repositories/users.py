from app.db.models.user import User as UserDB
from app.services.models.users import User, UserCreate, UserUpdate, UserFilter
from app.services.enums.users import Role
from app.services.models.base import Page
from app.services.models.errors import ALREADY_EXISTS
from app.repositories.helpers.page import build_page


from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from typing import Callable
from datetime import datetime, timezone


class UsersRepository:
    def __init__(self, get_session: Callable[..., Session]) -> None:
        self._get_session = get_session


    def get_list(self, filter: UserFilter) -> Page[User]:
        with self._get_session() as session:
            q = session.query(UserDB).where(UserDB.deleted_at == None)
            
            if filter.email:
                q = q.where(UserDB.email.ilike(f'%{filter.email}%'))
            
            q = q.order_by(UserDB.id.asc())

            return build_page(User, q, filter)


    def get(self, id: int) -> User | None:
        with self._get_session() as session:
            user = session.query(UserDB).where(
                (UserDB.id == id) &
                (UserDB.deleted_at == None)
            ).first()

            return User.model_validate(user) if user else None


    def get_by_email(self, email: str) -> User | None:
        with self._get_session() as session:
            user = session.query(UserDB).where(
                (UserDB.email == email) &
                (UserDB.deleted_at == None)
            ).first()

            return User.model_validate(user) if user else None


    def create(self, model: UserCreate) -> User:
        try:
            with self._get_session() as session:
                user = UserDB(**model.model_dump())
                session.add(user)
                session.commit()
                session.refresh(user)
                
                return User.model_validate(user)
        except IntegrityError:
            raise ALREADY_EXISTS


    def update(self, id: int, model: UserUpdate) -> User | None:
        try:
            with self._get_session() as session:
                user = session.query(UserDB).where(
                    (UserDB.id == id) &
                    (UserDB.deleted_at == None)
                ).first()

                if user is None:
                    return None
            
                if type(model.email) is str:
                    user.email = model.email
                
                if type(model.role) is str:
                    user.role = model.role
                
                if type(model.balance) is int:
                    user.balance = model.balance

                user.updated_at = datetime.now(timezone.utc)

                session.commit()

                return User.model_validate(user)

        except IntegrityError:
            raise ALREADY_EXISTS


    def delete(self, id: int) -> bool:
        with self._get_session() as session:
            user = session.query(UserDB).where(
                (UserDB.id == id) &
                (UserDB.deleted_at == None)
            ).first()

            if not user:
                return False
            
            time = datetime.now(timezone.utc)
            user.deleted_at = time
            user.updated_at = time
            session.commit()

            return True
