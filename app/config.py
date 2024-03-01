from enum import Enum
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    TOKEN: str = 'bot_token'

    class Config:
        env_prefix = 'BOT_'
        env_file = '.env'
        extra = 'allow'


class APIConfig(BaseSettings):
    VERSION: str = '1.0.0'
    TITLE: str = 'Bot Task Reward API'
    SUMMARY: str | None = None
    DESCRIPTION: str = 'API for telegram bot for completing various tasks and getting points'
    PREFIX: str = '/api'
    IS_VISIBLE: bool = True

    class Config:
        env_prefix = 'API_'
        env_file = '.env'
        extra = 'allow'


class AppConfig(BaseSettings):
    PORT: int = 80
    HOST: str = '0.0.0.0'
    DEBUG: bool = False

    class Config:
        env_prefix = 'APP_'
        env_file = '.env'
        extra = 'allow'


class DBConfig(BaseSettings):
    ALEMBIC_INI_PATH: str = 'alembic.ini'
    PORT: int = 5432
    HOST: str = 'bot_task_reward_postgres'
    NAME: str = 'bot_task_reward'
    USER: str = 'admin'
    PASSWORD: str = 'password'
    APPLY_MIGRATIONS: bool = True

    def dsn(self):
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

    class Config:
        env_prefix = 'DB_'
        env_file = '.env'
        extra = 'allow'


class LogConfig(BaseSettings):
    class LogLevel(str, Enum):
        debug = 'debug'
        info = 'info'
        error = 'error'

    LEVEL: LogLevel = LogLevel.info
    DIR: str = ''
    RETENTION: int = 5
    ROTATION: int = 100

    class Config:
        env_prefix = 'LOG_'
        use_enum_values = True
        env_file = '.env'
        extra = 'allow'


class Config(BaseSettings):
    api: APIConfig = APIConfig()
    app: AppConfig = AppConfig()
    bot: BotConfig = BotConfig()
    db:  DBConfig  = DBConfig()
    log: LogConfig = LogConfig()
