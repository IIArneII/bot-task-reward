from app.services.models.tasks import TaskForUser, Task


def not_found_msg() -> str:
    return f'''
Не найдены задания, ожидающий подтверждения
'''

def approve_task_msg(success: bool) -> str:
    if not success:
        return f'Уже проверено другим администратором'
    
    return f'Проверено'

def notification_msg(task: Task, success: bool) -> str:
    end_text = f'Задание выполнено. Зачислено {task.bonuses} бонусов' if success else 'Задание не выполнено'

    return f'''
Задание проверено!

{task.name}

{end_text}
'''

def confirmation_task_msg(task: TaskForUser):
    return f'''
- Идентификатор задачи: {task.id}
- Социальная сеть: {task.social_network}
- Имя задачи: {task.name}
- Описание задачи: {task.description}
- Ссылка на выполнение: {task.link}
- Количествов бонусов: {task.bonuses}
- Статус выполнения: {task.status}
- Идентификатор пользователя: {task.user_id}
'''
