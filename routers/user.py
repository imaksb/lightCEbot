from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from database.models.user import User
from misc.graphic import Graphic
from keyboards.inline import main_menu_keyboard
from misc.shutdown_info import get_information_about_graphic

user_router = Router()


async def start_message(
        controller: Message | CallbackQuery,
        graphic: Graphic,
        user: User,
        editable=False
):
    graphic_for_user = "\n\n" + graphic.pprint_row(user.group)

    text_to_send = get_information_about_graphic(user.group, graphic) + graphic_for_user
    markup = main_menu_keyboard(user.group, user.get_update)

    if editable:
        return await controller.message.edit_text(text_to_send, reply_markup=markup)

    await controller.answer(text_to_send, reply_markup=markup)


@user_router.message(CommandStart())
async def start(message: Message, graphic: Graphic, user: User):
    await start_message(message, graphic, user)
