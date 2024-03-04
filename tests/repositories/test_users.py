from app.repositories.users import UsersRepository
from app.services.models.users import User, UserCreate, UserUpdate, UserFilter
from app.services.models.errors import AlreadyExistsError
from app.services.enums.users import Role

from pytest import raises


class TestCreate:
    def test_create(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
            email='email@email.com',
        )

        user = users_repo.create(new_user)
        assert type(user) is User
        assert user.id == new_user.id
        assert user.email == new_user.email
        assert user.balance == 0
        assert user.role == Role.member
    
    def test_already_exists_id(self, users_repo: UsersRepository, clean_db):
        new_user_1 = UserCreate(
            id=1,
            email='email1@email.com',
        )

        new_user_2 = UserCreate(
            id=1,
            email='email2@email.com',
        )

        users_repo.create(new_user_1)

        with raises(AlreadyExistsError):
            users_repo.create(new_user_2)
    
    def test_already_exists_email(self, users_repo: UsersRepository, clean_db):
        new_user_1 = UserCreate(
            id=1,
            email='email@email.com',
        )

        new_user_2 = UserCreate(
            id=2,
            email='email@email.com',
        )

        users_repo.create(new_user_1)

        with raises(AlreadyExistsError):
            users_repo.create(new_user_2)


class TestGet:
    def test_get_by_id(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
            email='email@email.com',
        )

        created_user = users_repo.create(new_user)
        received_user = users_repo.get(created_user.id)
        assert type(received_user) is User
        assert received_user.model_dump() == created_user.model_dump()
    
    def test_get_by_email(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
            email='email@email.com',
        )

        created_user = users_repo.create(new_user)
        received_user = users_repo.get_by_email(created_user.email)
        assert type(received_user) is User
        assert received_user.model_dump() == created_user.model_dump()

    def test_not_found_by_id(self, users_repo: UsersRepository, clean_db):
        received_user = users_repo.get(1)
        assert received_user is None
    
    def test_not_found_by_email(self, users_repo: UsersRepository, clean_db):
        received_user = users_repo.get_by_email('email@email.com')
        assert received_user is None


class TestDelete:
    def test_delete(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
            email='email@email.com',
        )

        users_repo.create(new_user)
        res = users_repo.delete(new_user.id)
        assert res == True
    
    def test_delete_and_get(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
            email='email@email.com',
        )

        users_repo.create(new_user)
        users_repo.delete(new_user.id)
        received_user = users_repo.get(new_user.id)
        assert received_user is None

    def test_not_found(self, users_repo: UsersRepository, clean_db):
        res = users_repo.delete(1)
        assert res == False


class TestUpdate:
    def test_update(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
            email='email@email.com',
        )

        created_user = users_repo.create(new_user)

        user_update = UserUpdate(
            email='email1@email.com',
            role=Role.admin,
            balance=10,
        )

        created_user.email = user_update.email
        created_user.role = user_update.role
        created_user.balance = user_update.balance
        
        updated_user = users_repo.update(created_user.id, user_update)
        assert type(updated_user) is User
        assert updated_user.updated_at >= created_user.updated_at
        created_user.updated_at = updated_user.updated_at
        assert updated_user.model_dump() == created_user.model_dump()
    
    def test_update_and_get(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
            email='email@email.com',
        )

        created_user = users_repo.create(new_user)

        user_update = UserUpdate(
            email='email1@email.com',
            role=Role.admin,
            balance=10,
        )

        created_user.email = user_update.email
        created_user.role = user_update.role
        created_user.balance = user_update.balance
        
        users_repo.update(created_user.id, user_update)
        updated_user = users_repo.get(created_user.id)
        assert type(updated_user) is User
        assert updated_user.updated_at >= created_user.updated_at
        created_user.updated_at = updated_user.updated_at
        assert updated_user.model_dump() == created_user.model_dump()

    def test_not_found(self, users_repo: UsersRepository, clean_db):
        user_update = UserUpdate()

        updated_user = users_repo.update(1, user_update)
        assert updated_user is None

    def test_empty_update(self, users_repo: UsersRepository, clean_db):
        new_user = UserCreate(
            id=1,
            email='email@email.com',
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
            email='email@email.com',
        )

        created_user = users_repo.create(new_user)

        user_update = UserUpdate(
            email=created_user.email,
            role=created_user.role,
            balance=created_user.balance,
        )

        updated_user = users_repo.update(created_user.id, user_update)
        assert type(updated_user) is User
        assert updated_user.updated_at >= created_user.updated_at
        created_user.updated_at = updated_user.updated_at
        assert updated_user.model_dump() == created_user.model_dump()

    def test_already_exists_email(self, users_repo: UsersRepository, clean_db):
        new_user_1 = UserCreate(
            id=1,
            email='email1@email.com',
        )

        new_user_2 = UserCreate(
            id=2,
            email='email2@email.com',
        )

        users_repo.create(new_user_1)
        users_repo.create(new_user_2)

        with raises(AlreadyExistsError):
            users_repo.update(new_user_2.id, UserUpdate(email=new_user_1.email))
