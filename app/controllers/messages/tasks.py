from app.services.models.tasks import TaskForUser
from app.services.models.tasks import SocialNetwork, Status


def tasks_msg() -> str:
    return f'''
💎Список заданий💎
Выполняй эти задания и получай бонусы!
    '''


def task_msg(task: TaskForUser) -> str:
    end_text = 'Ты уже выполнил это задание!'
    
    if task.status == Status.not_completed:
        if SocialNetwork.is_telegram(task.social_network):
            end_text = f'Ссылка на выполнение: {task.link}'
        elif SocialNetwork.for_screenshot(task.social_network):
            end_text = f'Ссылка на выполнение: {task.link}. Отправь скриншот, подтверждающий выполнение'
        else:    
            end_text = 'Отправь свое имя пользователя в этой социальной сети и мы вышлем ссылку на выполнение'
    
    elif task.status == Status.waiting_for_confirmation:
        end_text = 'Ожидай подтверждения'

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

def screenshot_answer_msg() -> str:
    return f'''
Отлично! Потребуется некоторое время, чтобы мы проверили выполнение
'''
