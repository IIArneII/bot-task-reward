import tweepy
from loguru import logger

from app.infrastructure.social_network import ISocialNetwork
from app.config import TwitterConfig


class Twitter(ISocialNetwork):
    def __init__(self, config: dict | TwitterConfig) -> None:
        self._config: TwitterConfig = config if type(config) is TwitterConfig else TwitterConfig(config)

        auth = tweepy.OAuthHandler(
            consumer_key=self._config.CONSUMER_KEY,
            consumer_secret=self._config.CONSUMER_SECRET,
            access_token=self._config.ACCESS_TOKEN,
            access_token_secret=self._config.ACCESS_TOKEN_SECRET,
        )

        self._client = tweepy.API(auth)

        relationship = self._client.get_friendship(source_screen_name='Arne73170969672', target_screen_name='Strapongo')


        # self._client = tweepy.Client(
        #     bearer_token=''
        #     consumer_key=self._config.CONSUMER_KEY,
        #     consumer_secret=self._config.CONSUMER_SECRET,
        #     access_token=self._config.ACCESS_TOKEN,
        #     access_token_secret=self._config.ACCESS_TOKEN_SECRET,
        # )

        # user = self._client.get_user(username=self._config.CHECK_USERNAME, user_auth=True) if self._config.CHECK_USERNAME else self._client.get_me()

        user = self._client.get_user(username='Arne73170969672')
        self._check_user_id = user.data.id

        users = self._client.get_users_followers(self._check_user_id, user_auth=True)
        logger.info(users)


    def check_user(self, user_name: str) -> bool:
        self._client.get_user
        return True
