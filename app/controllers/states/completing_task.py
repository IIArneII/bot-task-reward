from aiogram.filters.state import State, StatesGroup


class CompletingTask(StatesGroup):
    telegram_task = State()
    screenshot_task = State()
    user_name_task = State()
    execution_process = State()
