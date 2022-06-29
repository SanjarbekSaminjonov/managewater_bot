import logging

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from keyboards.channel_buttons import menu_buttons_callback
from keyboards.default import cancel_button, home_buttons, location_button, yes_no_buttons
from states.add_channel_device import ChannelRegisterState
from data.words import get_word as _
from utils.assistant.make_up_info import make_up_channel_device_info_pre_save


@dp.callback_query_handler(menu_buttons_callback.filter(sep='add_new_channel_device'))
async def add_new_device(call: CallbackQuery):
    await ChannelRegisterState.device_id.set()
    await call.message.edit_text('Yangi qurilma qo\'shish')
    await bot.send_message(
        call.from_user.id,
        'Qurilma "id" sini kiriting (11 xonali)',
        reply_markup=cancel_button
    )


@dp.message_handler(state=ChannelRegisterState.device_id)
async def add_new_device(message: Message, state: FSMContext):
    device_id = message.text
    if len(device_id) == 11:
        device = await db.get_channel_device_info(device_id)
        if device is None:
            base_device = await db.get_base_device_type(device_id)
            if base_device is not None:
                if base_device == 'channel':
                    await ChannelRegisterState.next()
                    await message.answer(
                        'Qurilmadagi sim karta raqamni kiriting.\n'
                        'Mison uchun: <b>+998*****7777</b>'
                    )
                    await state.update_data({'device_id': device_id})
                else:
                    await message.answer('Bu "id" dagi qurilma quduqlar uchun chiqarilgan.\nQayta kiriting')
            else:
                await message.answer('Bunday "id" dagi qurilma topilmadi.\nQayta kiring')
        else:
            user_id = await db.get_user_id(message.from_user.id)
            if user_id == device[5]:
                await state.finish()
                await message.answer(
                    'Siz bu qurilmani avval ro\'yxatdan o\'tkazgansiz',
                    reply_markup=home_buttons
                )
            else:
                await message.answer('Bu qurilma allaqachon ro\'yxatdan o\'tgan')
                # haqiqiy egasiga so'rov yuborish bo'ladi
    else:
        await message.answer('Kiritilgan "id" 11 xonali emas!\nQayta kiriting')


@dp.message_handler(state=ChannelRegisterState.phone)
async def add_new_device(message: Message, state: FSMContext):
    phone_number = message.text
    if len(phone_number) == 13 and phone_number.startswith('+998') and phone_number[1:].isdigit():
        await ChannelRegisterState.next()
        await message.answer('Qurilmaga nom bering.')
        await state.update_data({'phone_number': phone_number})
    else:
        await message.answer(
            'Telefon noto\'g\'ri kiritildi.\nIltimos ko\'rsatilgan tartibda kiriting.\n'
            'Mison uchun: <b>+998911234567</b>'
        )


@dp.message_handler(state=ChannelRegisterState.name)
async def add_new_device(message: Message, state: FSMContext):
    await ChannelRegisterState.next()
    await message.answer('Qurilmaning standart balandligini kiriting (santimetr)')
    await state.update_data({'name': message.text})


@dp.message_handler(state=ChannelRegisterState.height)
async def add_new_device(message: Message, state: FSMContext):
    try:
        _ = float(message.text)
        await message.answer('Qurilmaning joylashuvini kiriting', reply_markup=location_button)
        await ChannelRegisterState.next()
        await state.update_data({'height': message.text})
    except Exception as err:
        logging.error(err)
        await message.reply('Balandlik noto\'g\'ri kiritildi')


@dp.message_handler(state=ChannelRegisterState.location, text_contains=_('ingore_step'))
async def add_new_device(message: Message, state: FSMContext):
    await ChannelRegisterState.next()
    data = await state.get_data()
    await message.answer(
        f'{make_up_channel_device_info_pre_save(data)}\n\n'
        'Qurilma ma\'lumotlar to\'g\'rimi?',
        reply_markup=yes_no_buttons
    )


@dp.message_handler(state=ChannelRegisterState.location, content_types='location')
async def add_new_device(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        f'{make_up_channel_device_info_pre_save(data)}\n\n'
        'Qurilma ma\'lumotlar to\'g\'rimi?',
        reply_markup=yes_no_buttons
    )
    await state.update_data({
        'latitude': message.location.latitude,
        'longitude': message.location.longitude
    })
    await ChannelRegisterState.next()


@dp.message_handler(text_contains=_('yes'), state=ChannelRegisterState.save_basin)
async def add_new_device(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        user_id = await db.get_user_id(message.from_user.id)
        data['user_id'] = user_id
        data['height_conf'] = 0
        await db.add_new_channel_device(data)
        await message.answer('Qurilma muvaffaqiyatli qo\'shildi 👍', reply_markup=home_buttons)
    except Exception as err:
        logging.error(err)
        await message.answer(
            'Ma\'lumotlarni saqlashda xatolik yuz berdi', reply_markup=home_buttons)
    await state.finish()


@dp.message_handler(text_contains=_('no'), state=ChannelRegisterState.save_basin)
async def add_basin(message: Message, state: FSMContext):
    await message.answer(
        'Qurilma qo\'shish bekor qilindi',
        reply_markup=home_buttons
    )
    await state.finish()
