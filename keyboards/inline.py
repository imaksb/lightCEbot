from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

status_emoji = ["🟥", "🟩️"]


def main_menu_keyboard(group: int, getting_update: bool):
    buttons = [
        [
            InlineKeyboardButton(text=f"Змінити групу ({group})",
                                 callback_data="change_group")
        ],
        [

            InlineKeyboardButton(text=f"{status_emoji[getting_update]} Отримувати оновлення",
                                 callback_data="getting_update"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )

    return keyboard


class GroupCallbackData(CallbackData, prefix="group"):
    group_number: int


def group_buttons(except_group: int):
    builder = InlineKeyboardBuilder()

    for group in range(1, 16):
        if except_group == group:
            continue
        builder.button(text=f"{group}", callback_data=GroupCallbackData(group_number=group))

    # builder.button(text="Повернутись на головну", callback_data="go_menu")

    return builder.as_markup()
