from app.services.models.tasks import TaskForUser


def tasks_msg() -> str:
    return f'''
💎Список заданий💎
Выполняй эти задания и получай бонусы!
    '''


def task_msg(task: TaskForUser) -> str:
    return f'''
{task.name}

❗{task.description}

💎Будет получено {task.bonuses} бонусов

{'Ты уже выполнил это задание!' if task.is_done else 'Отправь свое имя пользователя в этой социальной сети и мы вышлем ссылку на выполнение'}
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
'Кажется, вы не выполнили задание😞'
'''
