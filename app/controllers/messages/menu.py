from app.services.models.users import User


def menu_msg(user: User, user_name: str) -> str:
    return f'''
Привет, {user_name}!
💎Баланс бонусов: {user.balance}.
❗Выполняй задания, чтобы получать бонусы.
    '''

def info_msg() -> str:
    return f'''
Тут очень важная информация.
Много важной информации.
И можно вернуться в меню.
'''
