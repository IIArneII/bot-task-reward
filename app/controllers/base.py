from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery

from app.controllers.keyboards.menu import menu_kb, back_to_menu_kb
from app.controllers.messages.menu import menu_msg, info_msg
from app.controllers.messages.error import error_msg
from app.services.users import UsersService
from app.services.models.users import UserCreate
from app.container import get_container


base_router = Router()


@base_router.message(Command("start"))
async def start(msg: Message):
    try:
        users_service: UsersService = get_container().users_service()

        user = users_service.register(UserCreate(id=msg.from_user.id))

        await msg.answer(menu_msg(user, msg.from_user.full_name), reply_markup=menu_kb)

    except Exception as e:
        await msg.answer(error_msg(str(e)))
    

@base_router.callback_query(F.data == 'info')
async def info(clbck: CallbackQuery, state: FSMContext):
    try:
        await state.clear()

        await clbck.message.answer(info_msg(), reply_markup=back_to_menu_kb)
    
    except Exception as e:
        await clbck.message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)


@base_router.callback_query(F.data == 'menu')
async def menu(clbck: CallbackQuery, state: FSMContext):
    try:
        users_service: UsersService = get_container().users_service()
        user = users_service.get(clbck.from_user.id)

        await state.clear()

        await clbck.message.answer(menu_msg(user, clbck.from_user.full_name), reply_markup=menu_kb)
    
    except Exception as e:
        await clbck.message.answer(error_msg(str(e)), reply_markup=back_to_menu_kb)
