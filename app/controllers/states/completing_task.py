from aiogram.filters.state import State, StatesGroup


class CompletingTask(StatesGroup):
    telegram_task = State()
    user_name = State()
    execution_process = State()
