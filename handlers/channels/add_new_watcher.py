import logging

from aiogram.types import CallbackQuery

from loader import dp, db, bot
from keyboards.channel_buttons import additional_watcher_callback, accept_watch_request_button
from utils.assistant.user_info import makeup_user_info


@dp.callback_query_handler(additional_watcher_callback.filter(sep='send_request_to_watch'))
async def add_new_watcher(call: CallbackQuery):
    *other, device_id, owner_telegram_id = call.data.split(':')
    watcher_telegram_id = call.from_user.id
    watcher_id = await db.get_user_id(call.from_user.id)
    watching_device = await db.check_user_and_device(watcher_id, device_id)
    if watching_device is None:
        try:
            watcher_data = await db.get_user_info(watcher_telegram_id)
            device = await db.get_channel_device_info(device_id)
            text = makeup_user_info(watcher_data)
            text += f'\n\nUshbu foydalanuvchi sizning qurilmangizni ' \
                    f'kuzatishga ruxsat so\'ramoqda\n' \
                    f'Qurilma nomi: {device[1]}\n' \
                    f'Qurilma IDsi: {device_id}'
            await bot.send_message(
                chat_id=owner_telegram_id,
                text=text,
                reply_markup=accept_watch_request_button(device_id, watcher_telegram_id)
            )
            await call.answer('So\'rov yuborildi', show_alert=True)
        except Exception as err:
            logging.error(err)
            await call.answer('So\'rov yuborishda xatolik yuzaga keldi', show_alert=True)
    else:
        await call.answer('Ushbu so\'rov qabul qilingan', show_alert=True)
    await call.message.edit_text('Qurilma egasiga so\'rov yuborilgan')


@dp.callback_query_handler(additional_watcher_callback.filter(sep='accept'))
async def owner_answer(call: CallbackQuery):
    *other, device_id, watcher_telegram_id = call.data.split(':')
    watcher_id = await db.get_user_id(watcher_telegram_id)
    await db.add_new_channel_watcher(device_id, watcher_id)
    text = call.message.text
    text += '\n\n<b>Ruxsat berildi</b>'
    await call.message.edit_text(text=text)
    await bot.send_message(watcher_telegram_id, f'{device_id} qurilma uchun ruxsat berildi')


@dp.callback_query_handler(additional_watcher_callback.filter(sep='ignore'))
async def owner_answer(call: CallbackQuery):
    *other, device_id, watcher_telegram_id = call.data.split(':')
    text = call.message.text
    text += '\n\n<b>Ruxsat berilmadi</b>'
    await call.message.edit_text(text=text)
    await bot.send_message(watcher_telegram_id, f'{device_id} qurilma uchun ruxsat berilmadi')
