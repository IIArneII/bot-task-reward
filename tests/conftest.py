from pytest import fixture
from os.path import join

from app.db.db import DataBase
from app.config import DBConfig


def _ping_db(db: DataBase):
    try:
        db.ping()
        return True
    except Exception as e:
        print(e)
        return False


@fixture(scope='session')
def docker_compose_file(pytestconfig):
    return join(str(pytestconfig.rootdir), "tests", "docker-compose-test.yml")


@fixture(scope='session')
def db(docker_ip, docker_services) -> DataBase:
    config = DBConfig(
        PORT=docker_services.port_for("bot_task_reward_postgres_test", 5432),
        HOST=docker_ip,
        USER='admin',
        NAME='bot_task_reward_test',
        PASSWORD='',
        APPLY_MIGRATIONS=False,
    )

    db = DataBase(config, ping=False)

    docker_services.wait_until_responsive(timeout=30.0, pause=0.1, check=lambda: _ping_db(db))
    
    db.apply_migrations()

    return db
