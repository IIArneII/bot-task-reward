from app.repositories.users import UsersRepository
from app.services.models.users import User, UserCreate, UserUpdate
from app.services.models.errors import AlreadyExistsError

from pytest import raises


class TestCreate:
    def test_create(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
        )

        user = users_repo.create(new_user)
        assert type(user) is User
        assert user.id == new_user.id
        assert user.balance == 0
        assert user.tasks == []
    
    def test_already_exists_id(self, users_repo: UsersRepository, clean_db):
        new_user_1 = UserCreate(
            id=1,
        )

        new_user_2 = UserCreate(
            id=1,
        )

        users_repo.create(new_user_1)

        with raises(AlreadyExistsError):
            users_repo.create(new_user_2)


class TestGet:
    def test_get_by_id(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
        )

        created_user = users_repo.create(new_user)
        received_user = users_repo.get(created_user.id)
        assert type(received_user) is User
        assert received_user.model_dump() == created_user.model_dump()

    def test_not_found_by_id(self, users_repo: UsersRepository, clean_db):
        received_user = users_repo.get(1)
        assert received_user is None


class TestUpdate:
    def test_update(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
        )

        created_user = users_repo.create(new_user)

        user_update = UserUpdate(
            balance=10,
            tasks=['1'],
        )

        created_user.balance = user_update.balance
        created_user.tasks = user_update.tasks
        
        updated_user = users_repo.update(created_user.id, user_update)
        assert type(updated_user) is User
        assert updated_user.updated_at >= created_user.updated_at
        created_user.updated_at = updated_user.updated_at
        assert updated_user.model_dump() == created_user.model_dump()
    
    def test_update_and_get(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
        )

        created_user = users_repo.create(new_user)

        user_update = UserUpdate(
            balance=10,
            tasks=['1'],
        )

        created_user.balance = user_update.balance
        created_user.tasks = user_update.tasks
        
        users_repo.update(created_user.id, user_update)
        updated_user = users_repo.get(created_user.id)
        assert type(updated_user) is User
        assert updated_user.updated_at >= created_user.updated_at
        created_user.updated_at = updated_user.updated_at
        assert updated_user.model_dump() == created_user.model_dump()

    def test_not_found(self, users_repo: UsersRepository, clean_db):
        updated_user = users_repo.update(1, UserUpdate())
        assert updated_user is None

    def test_empty_update(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
        )

        created_user = users_repo.create(new_user)

        updated_user = users_repo.update(created_user.id, UserUpdate())
        assert type(updated_user) is User
        assert updated_user.updated_at >= created_user.updated_at
        created_user.updated_at = updated_user.updated_at
        assert updated_user.model_dump() == created_user.model_dump()

    def test_empty_same_values(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
        )

        created_user = users_repo.create(new_user)

        user_update = UserUpdate(
            balance=created_user.balance,
            tasks=created_user.tasks,
        )

        updated_user = users_repo.update(created_user.id, user_update)
        assert type(updated_user) is User
        assert updated_user.updated_at >= created_user.updated_at
        created_user.updated_at = updated_user.updated_at
        assert updated_user.model_dump() == created_user.model_dump()
