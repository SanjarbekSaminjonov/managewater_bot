from typing import Union
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.words import get_word as _


def buttons(words: Union[list], row_width: Union[int] = 1) -> ReplyKeyboardMarkup:
    buttons_group = ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=True)
    for word in words:
        if word is not None:
            buttons_group.insert(KeyboardButton(text=word))
    return buttons_group


def contact_button_generate(contact_text: Union[str], cancel_text: Union[str]) -> ReplyKeyboardMarkup:
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


register_button = buttons([_('register')])

contact_button = contact_button_generate(_('request_contact'), _('cancel'))

home_buttons = buttons([_('channel_devices'), _('well_devices'), _('pump_station'), _('settings')], row_width=2)

yes_no_buttons = buttons([_('yes'), _('no'), _('cancel')], row_width=2)

cancel_button = buttons([_('cancel')])
