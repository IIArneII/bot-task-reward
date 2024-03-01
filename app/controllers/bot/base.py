from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from app.controllers.bot.keyboards.main_menu import menu, exit_kb, iexit_kb


router = Router()


@router.message(Command("start"))
async def start(msg: Message):
    await msg.answer(greet.format(name=msg.from_user.first_name), reply_markup=iexit_kb)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
async def menu_f(msg: Message):
    await msg.answer(menu_t, reply_markup=menu)
