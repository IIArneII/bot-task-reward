from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


confirmation_task_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Выполнено', callback_data='completed')],
    [InlineKeyboardButton(text='❌ Не выполнено', callback_data='not_completed')],
    [InlineKeyboardButton(text='🔙 В меню', callback_data='menu')],
])
