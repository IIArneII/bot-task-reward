from abc import ABC, abstractmethod

class ISocialNetwork(ABC):
    def check_user(self, user_name: str) -> bool:
        '''
        Checks whether the specified user is subscribed to an account on a social network.
        If the user is subscribed, then returns True, otherwise False.
        '''
