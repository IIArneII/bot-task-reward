from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from loguru import logger

from app.controllers.keyboards.menu import back_to_menu_kb
from app.controllers.keyboards.tasks import tasks_kb, back_to_tasks_kb, check_kb
from app.controllers.messages.tasks import tasks_msg, task_msg, task_successful_user_name_msg, task_failed_user_name_msg, successful_check_msg, failed_check_msg, screenshot_answer_msg
from app.controllers.messages.error import error_msg
from app.controllers.states.completing_task import CompletingTask
from app.services.tasks import TasksService
from app.services.models.tasks import SocialNetwork, Status
from app.container import get_container


tasks_router = Router()


@tasks_router.callback_query(F.data == 'tasks')
async def task_list(clbck: CallbackQuery, state: FSMContext):
    try:
        tasks_service: TasksService = await get_container().tasks_service()
        tasks = tasks_service.get_list(clbck.from_user.id)

        await state.clear()

        await clbck.message.answer(tasks_msg(), reply_markup=tasks_kb(tasks))
    
    except Exception as e:
        logger.exception(e)
        await clbck.message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)


@tasks_router.callback_query(F.data.contains('tasks_'))
async def task(clbck: CallbackQuery, state: FSMContext):
    try:
        tasks_service: TasksService = await get_container().tasks_service()
        task = tasks_service.get(clbck.from_user.id, clbck.data[6:])

        await state.clear()
        kb = back_to_tasks_kb

        if task.status == Status.not_completed:
            await state.update_data(task_id=task.id)

            if SocialNetwork.is_telegram(task.social_network):
                kb = check_kb
                await state.set_state(CompletingTask.telegram_task)
            
            elif SocialNetwork.for_screenshot(task.social_network):
                await state.set_state(CompletingTask.screenshot_task)
            
            else:
                await state.set_state(CompletingTask.user_name_task)

        await clbck.message.answer(task_msg(task), reply_markup=kb)
    
    except Exception as e:
        logger.exception(e)
        await clbck.message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)


@tasks_router.callback_query(CompletingTask.telegram_task, F.data == 'check')
async def telegram_task(clbck: CallbackQuery, state: FSMContext):
    try:
        tasks_service: TasksService = await get_container().tasks_service()

        data = await state.get_data()

        task_id = data['task_id']
        task = tasks_service.get(clbck.from_user.id, task_id)
        check = await tasks_service.check_execution(clbck.from_user.id, task_id, clbck.from_user.id)

        if check:
            logger.info(f'Successful execution check. User id: {clbck.from_user.id}. Task: {task_id}')
            await clbck.message.answer(successful_check_msg(task), reply_markup=back_to_menu_kb)
        else:
            logger.info(f'Failed execution check. User id: {clbck.from_user.id}. Task: {task_id}')
            await clbck.message.answer(failed_check_msg(), reply_markup=back_to_menu_kb)

    except Exception as e:
        logger.exception(e)
        await clbck.message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)


@tasks_router.message(CompletingTask.screenshot_task, F.photo)
async def save_screenshot(message: Message, state: FSMContext):
    try:
        tasks_service: TasksService = await get_container().tasks_service()

        data = await state.get_data()

        await tasks_service.save_screenshot(message.from_user.id, data['task_id'], message.photo[-1].file_id)

        await message.answer(screenshot_answer_msg(), reply_markup=back_to_menu_kb)

    except Exception as e:
        logger.exception(e)
        await message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)


@tasks_router.message(CompletingTask.user_name_task)
async def user_name(message: Message, state: FSMContext):
    try:
        tasks_service: TasksService = await get_container().tasks_service()

        data = await state.get_data()

        task_id = data['task_id']
        check = await tasks_service.check_user_name(message.from_user.id, task_id, message.text)
        task = tasks_service.get(message.from_user.id, task_id)

        if not check:
            logger.info(f'Failed user name check. User id: {message.from_user.id}. Task: {task_id}. User name: {message.text}')
            await message.answer(task_failed_user_name_msg(task), reply_markup=back_to_tasks_kb)
            return

        logger.info(f'Successful user name check. User id: {message.from_user.id}. Task: {task_id}. User name: {message.text}')
        
        await state.update_data(user_name=message.text)
        await state.set_state(CompletingTask.execution_process)

        await message.answer(task_successful_user_name_msg(task), reply_markup=check_kb)
    
    except Exception as e:
        logger.exception(e)
        await message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)


@tasks_router.callback_query(CompletingTask.execution_process, F.data == 'check')
async def check(clbck: CallbackQuery, state: FSMContext):
    try:
        tasks_service: TasksService = await get_container().tasks_service()

        data = await state.get_data()
        await state.clear()
        
        task_id = data['task_id']
        user_name = data['user_name']
        task = tasks_service.get(clbck.from_user.id, task_id)
        check = await tasks_service.check_execution(clbck.from_user.id, task_id, user_name)
        
        if check:
            logger.info(f'Successful execution check. User id: {clbck.from_user.id}. Task: {task_id}. User name: {user_name}')
            await clbck.message.answer(successful_check_msg(task), reply_markup=back_to_menu_kb)
        else:
            logger.info(f'Failed execution check. User id: {clbck.from_user.id}. Task: {task_id}. User name: {user_name}')
            await clbck.message.answer(failed_check_msg(), reply_markup=back_to_menu_kb)
    
    except Exception as e:
        logger.exception(e)
        await clbck.message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)
