from aiogram.filters.state import State, StatesGroup


class CompletingTask(StatesGroup):
    user_name = State()
    execution_process = State()
