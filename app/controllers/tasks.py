from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from loguru import logger
from asyncio import sleep

from app.controllers.keyboards.menu import menu_kb, back_to_menu_kb
from app.controllers.keyboards.tasks import tasks_kb, back_to_tasks_kb, check_kb
from app.controllers.messages.menu import menu_msg, info_msg
from app.controllers.messages.tasks import tasks_msg, task_msg, task_successful_user_name_msg, task_failed_user_name_msg, successful_check_msg, failed_check_msg
from app.controllers.messages.error import error_msg
from app.controllers.states.completing_task import CompletingTask
from app.services.users import UsersService
from app.services.tasks import TasksService
from app.services.models.users import UserCreate
from app.container import get_container


tasks_router = Router()


@tasks_router.callback_query(F.data == 'tasks')
async def task_list(clbck: CallbackQuery, state: FSMContext):
    try:
        tasks_service: TasksService = get_container().tasks_service()
        tasks = tasks_service.get_list(clbck.from_user.id)

        await state.clear()

        await clbck.message.answer(tasks_msg(), reply_markup=tasks_kb(tasks))
    
    except Exception as e:
        await clbck.message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)


@tasks_router.callback_query(F.data.contains('tasks_'))
async def task(clbck: CallbackQuery, state: FSMContext):
    try:
        tasks_service: TasksService = get_container().tasks_service()
        task = tasks_service.get(clbck.from_user.id, clbck.data[6:])

        await state.clear()

        if not task.is_done:
            await state.update_data(task_id=task.id)
            await state.set_state(CompletingTask.user_name)

        await clbck.message.answer(task_msg(task), reply_markup=back_to_tasks_kb)
    
    except Exception as e:
        await clbck.message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)


@tasks_router.message(CompletingTask.user_name)
async def user_name(message: Message, state: FSMContext):
    try:
        tasks_service: TasksService = get_container().tasks_service()

        data = await state.get_data()

        check = tasks_service.check_user_name(message.from_user.id, data['task_id'], message.text)
        if not check:
            await message.answer(task_failed_user_name_msg(task), reply_markup=back_to_tasks_kb)

        await state.update_data(user_name=message.text)
        await state.set_state(CompletingTask.execution_process)

        task = tasks_service.get(message.from_user.id, data['task_id'])

        await message.answer(task_successful_user_name_msg(task), reply_markup=check_kb)
    
    except Exception as e:
        await message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)


@tasks_router.callback_query(CompletingTask.execution_process, F.data == 'check')
async def check(clbck: CallbackQuery, state: FSMContext):
    try:
        tasks_service: TasksService = get_container().tasks_service()

        data = await state.get_data()
        await state.clear()
        
        task = tasks_service.get(clbck.from_user.id, data['task_id'])
        check = tasks_service.check_execution(clbck.from_user.id, data['task_id'], data['user_name'])
        
        if check:
            await clbck.message.answer(successful_check_msg(task), reply_markup=back_to_menu_kb)
        else:
            await clbck.message.answer(failed_check_msg(), reply_markup=back_to_menu_kb)
    
    except Exception as e:
        await clbck.message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)
