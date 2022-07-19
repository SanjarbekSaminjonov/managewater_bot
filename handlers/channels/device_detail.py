import logging

from aiogram.types import CallbackQuery

from loader import dp, db
from data.words import get_word as _
from utils.assistant.make_up_info import make_up_channel_device_info, makeup_channel_device_message_info
from keyboards.channel_buttons import channel_devices_list_callback, menu_buttons, manage_channel_device, \
    manage_channel_device_callback, channel_devices_list


@dp.callback_query_handler(channel_devices_list_callback.filter(sep='channel_devices_list'))
async def device_detail(call: CallbackQuery):
    device_id = call.data.split(':')[-1]
    if device_id == 'back_to_menu':
        await call.message.edit_text(
            _('channel_devices'),
            reply_markup=menu_buttons
        )
    else:
        device = await db.get_channel_device_info(device_id)
        text = make_up_channel_device_info(device)
        await call.message.edit_text(
            text,
            reply_markup=manage_channel_device(device_id)
        )


@dp.callback_query_handler(manage_channel_device_callback.filter(sep='see_last_message'))
async def device_detail(call: CallbackQuery):
    device_id = call.data.split(':')[-1]
    device = await db.get_channel_device_info(device_id)
    device_message = await db.get_last_channel_device_message(device_id)
    if device_message is not None:
        await call.message.answer(text=makeup_channel_device_message_info(device, device_message))
    else:
        await call.answer('Ma\'lumot topilmadi !', show_alert=True)


@dp.callback_query_handler(manage_channel_device_callback.filter(sep='see_location'))
async def device_detail(call: CallbackQuery):
    device_id = call.data.split(':')[-1]
    device = await db.get_channel_device_location(device_id)
    try:
        await call.message.answer_location(
            latitude=device[0],
            longitude=device[1]
        )
    except Exception as err:
        logging.error(err)
        await call.answer('Joylashuv ma\'lumoti topilmadi !', show_alert=True)
    await call.answer(cache_time=30)


@dp.callback_query_handler(manage_channel_device_callback.filter(sep='back_to_devices_list'))
async def device_detail(call: CallbackQuery):
    devices = await db.get_user_channel_devices(call.from_user.id)
    await call.message.edit_text(
        _('channel_devices_list'),
        reply_markup=channel_devices_list(devices)
    )
