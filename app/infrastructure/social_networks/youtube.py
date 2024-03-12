from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from loguru import logger

from app.infrastructure.social_network import ISocialNetwork
from app.services.models.errors import AUTHORIZATION_FAILURE
from app.config import YouTubeConfig


class YouTube(ISocialNetwork):
    def __init__(self, config: dict | YouTubeConfig) -> None:
        self._config: YouTubeConfig = config if type(config) is YouTubeConfig else YouTubeConfig(config)
        self._client = build('youtube', 'v3', developerKey='')


    def check_user(self, user_name: str) -> bool:
        channel = self._client.channels().list(
            forHandle=user_name,
            part='id'
        ).execute()

        if not channel.get('items'):
            return False

        channel_id = channel['items'][0]['id']

        while True:
            subscribers = self._client.subscriptions().list(
                part='subscriberSnippet',
                mySubscribers=True,
                maxResults=50,
                order='unread',
            ).execute()
            
            if channel_id in map(lambda x: x['subscriberSnippet']['channelId'], subscribers.get('items', [])):
                return True
            
            if len(subscribers.get('items', [])) < 50:
                return False

        return True
