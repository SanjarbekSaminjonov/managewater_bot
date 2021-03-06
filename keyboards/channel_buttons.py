from typing import Union

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data.words import get_word as _


menu_buttons_callback = CallbackData('callback', 'sep')
channel_devices_list_callback = CallbackData('callback', 'sep', 'device_id')
manage_channel_device_callback = CallbackData('callback', 'sep', 'device_id')
additional_watcher_callback = CallbackData('callback', 'sep', 'device_id', 'user_id')


menu_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=_('channel_devices_list'),
                callback_data=menu_buttons_callback.new(
                    sep='channel_devices_list'
                )
            )
        ],
        # [
        #     InlineKeyboardButton(
        #         text=_('add_new_channel_device'),
        #         callback_data=menu_buttons_callback.new(
        #             sep='add_new_channel_device'
        #         )
        #     )
        # ],
        # [
        #     InlineKeyboardButton(
        #         text=_('channel_devices_all_statistics'),
        #         callback_data=menu_buttons_callback.new(
        #             sep='channel_devices_all_statistics'
        #         )
        #     )
        # ]
    ]
)


def channel_devices_list(devices: Union[list]):
    buttons = InlineKeyboardMarkup(row_width=1)
    for device in devices:
        button = InlineKeyboardButton(
            text=device[1],
            callback_data=channel_devices_list_callback.new(
                sep='channel_devices_list',
                device_id=device[0]
            )
        )
        buttons.insert(button)
    back_button = InlineKeyboardButton(
        text=_('back'),
        callback_data=channel_devices_list_callback.new(
            sep='channel_devices_list',
            device_id='back_to_menu'
        )
    )
    buttons.insert(back_button)
    return buttons


def manage_channel_device(device_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # [
            #     InlineKeyboardButton(
            #         text=_('edit_device_data'),
            #         callback_data=manage_channel_device_callback.new(
            #             sep='edit_device_data',
            #             device_id=device_id
            #         )
            #     )
            # ],
            [
                InlineKeyboardButton(
                    text=_('see_last_message'),
                    callback_data=manage_channel_device_callback.new(
                        sep='see_last_message',
                        device_id=device_id
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text=_('see_location'),
                    callback_data=manage_channel_device_callback.new(
                        sep='see_location',
                        device_id=device_id
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text=_('back_to_devices_list'),
                    callback_data=manage_channel_device_callback.new(
                        sep='back_to_devices_list',
                        device_id=device_id
                    )
                )
            ]
        ]
    )


def send_request_to_be_channel_device_watcher(device_id, user_telegram_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='So\'rov yuborish',
                    callback_data=additional_watcher_callback.new(
                        sep='send_request_to_watch',
                        device_id=device_id,
                        user_id=user_telegram_id
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text=_('add_new_channel_device'),
                    callback_data=menu_buttons_callback.new(
                        sep='add_new_channel_device'
                    )
                )
            ]
        ]
    )


def accept_watch_request_button(device_id, watcher_telegram_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Ruxsat berish',
                    callback_data=additional_watcher_callback.new(
                        sep='accept',
                        device_id=device_id,
                        user_id=watcher_telegram_id
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text='Bekor qilish',
                    callback_data=additional_watcher_callback.new(
                        sep='ignore',
                        device_id=device_id,
                        user_id=watcher_telegram_id
                    )
                )
            ]
        ]
    )
