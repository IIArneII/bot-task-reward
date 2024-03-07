from instagrapi import Client
from os.path import dirname, isdir, isfile
from os import mkdir
from loguru import logger

from app.infrastructure.social_network import ISocialNetwork
from app.services.models.errors import AUTHORIZATION_FAILURE
from app.config import InstagramConfig


class Instagram(ISocialNetwork):
    def __init__(self, config: dict | InstagramConfig) -> None:
        self._config: InstagramConfig = config if type(config) is InstagramConfig else InstagramConfig(config)
        self._client = Client(logger=logger)
        
        if isfile(self._config.SETTINGS_PATH):
            self._client.load_settings(self._config.SETTINGS_PATH)
        elif not isdir(dir_name := dirname(self._config.SETTINGS_PATH)):
            mkdir(dir_name)

        if not self._client.login(self._config.USERNAME, self._config.PASSWORD):
            raise AUTHORIZATION_FAILURE
        
        self._client.dump_settings(self._config.SETTINGS_PATH)
        
        self._check_user_id = self._client.user_id_from_username(self._config.CHECK_USERNAME if self._config.CHECK_USERNAME else self._config.USERNAME)


    def check_user(self, user_name: str) -> bool:
        users = self._client.user_followers(self._check_user_id, use_cache=False)
        return any(map(lambda x: x.username == user_name, users.values()))
