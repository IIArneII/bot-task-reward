from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.services.models.tasks import TaskForUser


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
        is_done = '✅' if i.is_done else '❗'
        keyboard.append([InlineKeyboardButton(text=f'{is_done}{i.name}', callback_data=f'tasks_{i.id}')])
    
    keyboard.append([InlineKeyboardButton(text='🔙В меню', callback_data='menu')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
