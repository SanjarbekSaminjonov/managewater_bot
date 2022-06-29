from aiogram.types import CallbackQuery

from loader import dp, db
from data.words import get_word as _
from keyboards.channel_buttons import channel_devices_list, menu_buttons_callback


@dp.callback_query_handler(menu_buttons_callback.filter(sep='channel_devices_list'))
async def devices_list(call: CallbackQuery):
    devices = await db.get_user_channel_devices(call.from_user.id)
    if len(devices):
        await call.message.edit_text(
            _('channel_devices_list'),
            reply_markup=channel_devices_list(devices)
        )
    else:
        await call.answer('Sizda ro\'yxatdan o\'tgan qurilmalar yo\'q', show_alert=True)
