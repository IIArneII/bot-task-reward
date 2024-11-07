from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from app.services.models.users import User, Role


def menu_kb(user: User) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text='💎 Задания', callback_data='tasks')],
        [InlineKeyboardButton(text='ℹ️ Информация', callback_data='info')]
    ]

    if user.role == Role.admin:
        keyboard.append([InlineKeyboardButton(text='📝 Проверка выполнения', callback_data='admin')])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


back_to_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 В меню', callback_data='menu')],
])
