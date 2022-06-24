from typing import Union
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def buttons(words: Union[list], row_width: Union[int] = 1) -> ReplyKeyboardMarkup:
    buttons_group = ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=True)
    for word in words:
        if word is not None:
            buttons_group.insert(KeyboardButton(text=word))
    return buttons_group


def contact_button(contact_text: Union[str], cancel_text: Union[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(
                    text=contact_text,
                    request_contact=True)
            ],
            [KeyboardButton(cancel_text)]
        ]
    )
