from app.services.models.tasks import TaskForUser
from app.services.models.tasks import SocialNetwork


def tasks_msg() -> str:
    return f'''
💎Список заданий💎
Выполняй эти задания и получай бонусы!
    '''


def task_msg(task: TaskForUser) -> str:
    end_text = 'Ты уже выполнил это задание!'
    
    if not task.is_done:
        if task.social_network == SocialNetwork.telegram:
            end_text = f'Ссылка на выполнение: {task.link}'
        else:    
            end_text = 'Отправь свое имя пользователя в этой социальной сети и мы вышлем ссылку на выполнение'

    return f'''
{task.name}

❗{task.description}

💎Будет получено {task.bonuses} бонусов

{end_text}
    '''


def task_successful_user_name_msg(task: TaskForUser) -> str:
    return f'''
Отлично!
Ссылка на выполнение: {task.link}
Когда подпишешься, нажми на кнопку "проверить".
'''

def task_failed_user_name_msg(task: TaskForUser) -> str:
    return f'''
Ой, кажется, такой пользователь уже подписан на эту соц сеть. Попробуй ввести другого пользователя.
'''


def successful_check_msg(task: TaskForUser) -> str:
    return f'''
Проверка успешна!
Вы получили {task.bonuses} бонусов!
'''


def failed_check_msg() -> str:
    return f'''
Кажется, вы не выполнили задание😞
'''
