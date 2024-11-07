from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='BOT_',
        env_file='.env',
        extra='ignore',
    )

    TOKEN: str = '0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='APP_',
        env_file='.env',
        extra='ignore',
    )

    DEBUG: bool = False


class DBConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='DB_',
        env_file='.env',
        extra='ignore',
    )

    ALEMBIC_INI_PATH: str = 'alembic.ini'
    PORT: int = 5432
    HOST: str = 'bot_task_reward_postgres'
    NAME: str = 'bot_task_reward'
    USER: str = 'admin'
    PASSWORD: str = 'password'
    APPLY_MIGRATIONS: bool = True

    def dsn(self):
        if self.PASSWORD:
            return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"
        return f"postgresql://{self.USER}@{self.HOST}:{self.PORT}/{self.NAME}"


class FMConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='FM_',
        env_file='.env',
        extra='ignore',
    )

    DIR: str = './files'


class LogConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='LOG_',
        env_file='.env',
        extra='ignore',
        use_enum_values=True,
    )

    class LogLevel(str, Enum):
        debug = 'debug'
        info = 'info'
        error = 'error'

    LEVEL: LogLevel = LogLevel.info
    DIR: str = ''
    RETENTION: int = 5
    ROTATION: int = 100


class InstagramConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='SN_INST_',
        env_file='.env',
        extra='ignore',
        use_enum_values=True,
    )

    USERNAME: str = 'username'
    PASSWORD: str = 'password'
    SETTINGS_PATH: str = './social_networks_temp/instagram_settings.json'


class TelegramConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='SN_TELEGRAM_',
        env_file='.env',
        extra='ignore',
        use_enum_values=True,
    )

    CHANNEL: str = '@channel_name'


class DiscordConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='SN_DISCORD_',
        env_file='.env',
        extra='ignore',
        use_enum_values=True,
    )

    TOKEN: str = 'AAAAAAAAAAAAAAAAAAAAAAAA.AAAAAA.AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    GUILD: int = 1


class SNConfig(BaseSettings):
    discord: DiscordConfig = DiscordConfig()
    telegram: TelegramConfig = TelegramConfig()
    instagram: InstagramConfig = InstagramConfig()


class Config(BaseSettings):
    app: AppConfig = AppConfig()
    bot: BotConfig = BotConfig()
    db:  DBConfig  = DBConfig()
    log: LogConfig = LogConfig()
    sn: SNConfig = SNConfig()
    fm: FMConfig = FMConfig()
