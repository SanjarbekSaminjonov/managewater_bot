from aiogram.types import CallbackQuery

from loader import dp, db
from data.words import get_word as _
from utils.assistant.make_up_info import make_up_channel_device_info
from keyboards.channel_buttons import channel_devices_list_callback, menu_buttons, manage_channel_device


@dp.callback_query_handler(channel_devices_list_callback.filter(sep='channel_devices_list'))
async def device_detail(call: CallbackQuery):
    device_id = call.data.split(':')[-1]
    if device_id == 'back_to_menu':
        await call.message.edit_text(
            _('channel_devices'),
            reply_markup=menu_buttons
        )
    else:
        device = await db.get_device_info(device_id)
        text = make_up_channel_device_info(device)
        print(text)
        await call.message.edit_text(
            text,
            reply_markup=manage_channel_device(device_id)
        )
