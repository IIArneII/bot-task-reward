from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💎 Задания', callback_data='tasks')],
    [InlineKeyboardButton(text='ℹ️ Информация', callback_data='info')],
])

back_to_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙В меню', callback_data='menu')],
])
