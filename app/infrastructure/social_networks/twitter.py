from loguru import logger

from app.infrastructure.social_network import ISocialNetwork


class Twitter(ISocialNetwork):
    def __init__(self) -> None:
        logger.info('Twitter initialization...')

        self.subscribers: list[str] = []
    
    async def check_user(self, user_name: str) -> bool:
        if user_name in self.subscribers:
            return True
        
        # Убрать
        self.subscribers.append(user_name)
        
        return False
