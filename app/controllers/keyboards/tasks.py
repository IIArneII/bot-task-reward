from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.services.models.tasks import TaskForUser, Status


back_to_tasks_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙В список заданий', callback_data='tasks')],
])


check_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💎Проверить', callback_data='check')],
    [InlineKeyboardButton(text='🔙В список заданий', callback_data='tasks')],
])


def tasks_kb(tasks: list[TaskForUser]) -> InlineKeyboardMarkup:
    keyboard = []
    for i in tasks:
        status = '❗'
        if i.status == Status.completed:
            status = '✅'
        elif i.status == Status.waiting_for_confirmation:
            status = '⌛'

        keyboard.append([InlineKeyboardButton(text=f'{status}{i.name}', callback_data=f'tasks_{i.id}')])
    
    keyboard.append([InlineKeyboardButton(text='🔙В меню', callback_data='menu')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
