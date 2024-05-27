from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.models.user import User
from database.repo.requests import RequestsRepo
from misc.graphic import Graphic
from keyboards.inline import group_buttons, GroupCallbackData
from routers.user import start_message
from states.settings import Settings

settings_router = Router()


@settings_router.callback_query(F.data == "change_group")
async def user_update_group_request(query: CallbackQuery, state: FSMContext, user: User):
    update_message = await query.message.edit_text(f"Ваша поточна група: <b>{user.group}</b>\n\n"
                                                   f"<b>Оберіть нову групу:</b>",
                                                   reply_markup=group_buttons(user.group))

    await state.update_data(message_id=update_message.message_id)
    await state.set_state(Settings.group)


async def edit_group_after_success(state: FSMContext, message: Message, telegram_id: int, new_group: int,
                                   repo: RequestsRepo, bot: Bot):
    data = await state.get_data()
    await bot.delete_message(telegram_id, data['message_id'])
    await repo.users.change_group(telegram_id, new_group)
    await message.answer("⚡️ Група оновлена.")
    await state.clear()


@settings_router.callback_query(GroupCallbackData.filter())
async def user_update_group_confirm_using_button(query: CallbackQuery,
                                                 callback_data: GroupCallbackData,
                                                 state: FSMContext,
                                                 repo: RequestsRepo,
                                                 bot: Bot,
                                                 user: User,
                                                 graphic: Graphic):
    await edit_group_after_success(
        state,
        query.message,
        query.from_user.id,
        callback_data.group_number,
        repo,
        bot
    )
    await start_message(query.message, graphic, user)


@settings_router.message(Settings.group)
async def user_update_group_confirm_using_text(message: Message,
                                               state: FSMContext,
                                               repo: RequestsRepo,
                                               bot: Bot,
                                               user: User,
                                               graphic: Graphic):
    passed_text = message.text

    if not passed_text.isdigit():
        return await message.answer("Ви ввели не число.")

    new_group = int(passed_text)

    if new_group < 1 or new_group > 15:
        return await message.answer("Такої групи не існує.")

    await edit_group_after_success(
        state,
        message,
        message.from_user.id,
        new_group,
        repo,
        bot,
    )
    await start_message(message, graphic, user)


@settings_router.callback_query(F.data == "getting_update")
async def user_update_status(query: CallbackQuery, repo: RequestsRepo, user: User, graphic: Graphic):
    await repo.users.change_getting_update_status(query.from_user.id)
    user = await repo.users.get_user(query.from_user.id)
    await start_message(query, graphic, user, editable=True)
