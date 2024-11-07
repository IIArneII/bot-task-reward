from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from loguru import logger

from app.controllers.keyboards.menu import back_to_menu_kb
from app.controllers.keyboards.admin import confirmation_task_kb
from app.controllers.messages.admin import not_found_msg, confirmation_task_msg, approve_task_msg, notification_msg
from app.controllers.messages.error import error_msg
from app.controllers.states.admin import Admin
from app.services.tasks import TasksService
from app.container import get_container


admin_router = Router()


@admin_router.callback_query(F.data == 'admin')
async def confirmation_task(clbck: CallbackQuery, state: FSMContext):
    try:
        tasks_service: TasksService = await get_container().tasks_service()
        task = await tasks_service.get_for_checking(clbck.from_user.id)
        
        await state.clear()

        if task is None:
            await clbck.message.answer(not_found_msg(), reply_markup=back_to_menu_kb)
            return

        await state.set_state(Admin.admin)
        await state.update_data(task_id=task.id, user_id=task.user_id)

        await clbck.message.answer_photo(task.screenshot_path)
        await clbck.message.answer(confirmation_task_msg(task), reply_markup=confirmation_task_kb)
    
    except Exception as e:
        logger.exception(e)
        await clbck.message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)


@admin_router.callback_query(Admin.admin, F.data.in_({'completed', 'not_completed'}))
async def approve_task(clbck: CallbackQuery, state: FSMContext):
    try:
        tasks_service: TasksService = await get_container().tasks_service()

        data = await state.get_data()
        await state.clear()

        task, success, success_for_user = await tasks_service.approve(clbck.from_user.id, data['task_id'], data['user_id'], True if clbck.data == 'completed' else False)
        
        await clbck.message.answer(approve_task_msg(success), reply_markup=back_to_menu_kb)

        await clbck.bot.send_message(data['user_id'], notification_msg(task, success_for_user))

    except Exception as e:
        logger.exception(e)
        await clbck.message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)
