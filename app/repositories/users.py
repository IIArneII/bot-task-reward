from app.db.models.user import User as UserDB
from app.services.models.users import User, UserCreate, UserUpdate
from app.services.models.tasks import Status
from app.services.models.errors import ALREADY_EXISTS


from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import cast, String
from typing import Callable
from datetime import datetime, timezone


class UsersRepository:
    def __init__(self, get_session: Callable[..., Session]) -> None:
        self._get_session = get_session


    def get(self, id: int) -> User | None:
        with self._get_session() as session:
            user = session.query(UserDB).where(UserDB.id == id).first()

            return User.model_validate(user) if user else None

    def get_waiting_for_confirmation(self) -> User:
        with self._get_session() as session:

            user = session.query(UserDB).where(cast(UserDB.tasks, String).ilike(f'%{Status.waiting_for_confirmation}%')).order_by(UserDB.updated_at.desc()).first()

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
                user = session.query(UserDB).where(UserDB.id == id).first()

                if user is None:
                    return None
                
                if type(model.balance) is int:
                    user.balance = model.balance
                
                if type(model.tasks) is list:
                    user.tasks = [s.model_dump() for s in model.tasks]

                user.updated_at = datetime.now(timezone.utc)

                session.commit()

                return User.model_validate(user)

        except IntegrityError:
            raise ALREADY_EXISTS
