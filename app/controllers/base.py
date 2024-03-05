from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from loguru import logger
from asyncio import sleep

from app.controllers.keyboards.menu import menu_kb, back_to_menu_kb
from app.controllers.keyboards.tasks import tasks_kb, back_to_tasks_kb, check_kb
from app.controllers.messages.menu import menu_msg, info_msg
from app.controllers.messages.tasks import tasks_msg, task_msg, task_user_name_msg
from app.controllers.messages.error import error_msg
from app.services.users import UsersService
from app.services.tasks import TasksService
from app.services.models.users import UserCreate
from app.container import get_container


router = Router()


class CompletingTask(StatesGroup):
    user_name = State()
    execution_process = State()


@router.message(Command("start"))
async def start(msg: Message):
    try:
        users_service: UsersService = get_container().users_service()

        user = users_service.register(UserCreate(id=msg.from_user.id))

        await msg.answer(menu_msg(user, msg.from_user.full_name), reply_markup=menu_kb)

    except Exception as e:
        await msg.answer(error_msg(str(e)))
    

@router.callback_query(F.data == 'info')
async def start(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(info_msg(), reply_markup=back_to_menu_kb)


@router.callback_query(F.data == 'menu')
async def start(clbck: CallbackQuery, state: FSMContext):
    try:
        users_service: UsersService = get_container().users_service()
        user = users_service.get(clbck.from_user.id)

        await clbck.message.answer(menu_msg(user, clbck.from_user.full_name), reply_markup=menu_kb)
    
    except Exception as e:
        await clbck.message.answer(error_msg(str(e)))


@router.callback_query(F.data == 'tasks')
async def start(clbck: CallbackQuery, state: FSMContext):
    try:
        tasks_service: TasksService = get_container().tasks_service()
        tasks = tasks_service.get_list(clbck.from_user.id)

        await clbck.message.answer(tasks_msg(), reply_markup=tasks_kb(tasks))
    
    except Exception as e:
        await clbck.message.answer(error_msg(str(e)))


@router.callback_query(F.data.contains('tasks_'))
async def start(clbck: CallbackQuery, state: FSMContext):
    try:
        tasks_service: TasksService = get_container().tasks_service()
        task = tasks_service.get(clbck.from_user.id, clbck.data[6:])

        await state.update_data(task_id=task.id)
        await state.set_state(CompletingTask.user_name)

        await clbck.message.answer(task_msg(task), reply_markup=back_to_tasks_kb)
    
    except Exception as e:
        await clbck.message.answer(error_msg(str(e)))


@router.message(CompletingTask.user_name)
async def start(message: Message, state: FSMContext):
    try:
        tasks_service: TasksService = get_container().tasks_service()

        data = await state.get_data()
        task = tasks_service.get(message.from_user.id, data['task_id'])

        await state.update_data(user_name=message.text)
        await state.set_state(CompletingTask.execution_process)

        await message.answer(task_user_name_msg(task), reply_markup=check_kb)
    
    except Exception as e:
        await message.answer(error_msg(str(e)))


@router.callback_query(CompletingTask.execution_process, F.data == 'check')
async def start(clbck: CallbackQuery, state: FSMContext):
    try:
        tasks_service: TasksService = get_container().tasks_service()

        data = await state.get_data()
        await state.clear()
        
        logger.info(f'State: {data}')

        await clbck.message.answer('Проверка...')
        await sleep(2)
        await clbck.message.answer('Проверка успешна!')
    
    except Exception as e:
        await clbck.message.answer(error_msg(str(e)))
