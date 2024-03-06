from app.infrastructure.social_network import ISocialNetwork


class Twitter(ISocialNetwork):
    def __init__(self) -> None:
        self.subscribers: list[str] = []
    
    def check_user(self, user_name: str) -> bool:
        if user_name in self.subscribers:
            return True
        
        # Убрать
        self.subscribers.append(user_name)
        
        return False
