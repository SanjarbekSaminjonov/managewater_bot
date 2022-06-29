from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp
from data.words import get_word as _
from data.regions import regions_list, districts_list
from states.auth import UserRegisterState
from keyboards.default import contact_button, buttons, home_buttons, register_button, yes_no_buttons, cancel_button
from keyboards.inline import numbers_buttons
from utils.assistant.user_info import makeup_user_info, hash_password
from utils.backend_connection.register_api import create_user


@dp.message_handler(text_contains=_('register'), state=UserRegisterState.start_register)
async def register_user(message: Message):
    await UserRegisterState.next()
    await message.answer(
        _('request_phone_number'),
        reply_markup=contact_button
    )


@dp.message_handler(state=UserRegisterState.username, content_types='contact')
async def register_user(message: Message, state: FSMContext):
    await UserRegisterState.next()
    await message.answer(
        _('request_first_name'),
        reply_markup=buttons([message.from_user.first_name, _('cancel')])
    )
    phone = message.contact.phone_number
    phone = phone if phone.startswith('+') else f'+{phone}'
    await state.update_data({'username': phone})


@dp.message_handler(state=UserRegisterState.first_name)
async def register_user(message: Message, state: FSMContext):
    await UserRegisterState.next()
    await message.answer(
        _('request_last_name'),
        reply_markup=buttons([message.from_user.last_name, _('cancel')])
    )
    await state.update_data({'first_name': message.text})


@dp.message_handler(state=UserRegisterState.last_name)
async def register_user(message: Message, state: FSMContext):
    buttons_group = regions_list()
    buttons_group.append(_('cancel'))
    await UserRegisterState.next()
    await message.answer(
        _('request_region'),
        reply_markup=buttons(buttons_group, row_width=2)
    )
    await state.update_data({'last_name': message.text})


@dp.message_handler(state=UserRegisterState.region)
async def register_user(message: Message, state: FSMContext):
    region = message.text
    buttons_group = districts_list(region)
    buttons_group.append(_('cancel'))
    await UserRegisterState.next()
    await message.answer(
        _('request_city'),
        reply_markup=buttons(buttons_group, row_width=2)
    )
    await state.update_data({'region': region})


@dp.message_handler(state=UserRegisterState.city)
async def register_user(message: Message, state: FSMContext):
    await UserRegisterState.next()
    await message.answer(
        _('request_org_name'),
        reply_markup=cancel_button
    )
    await state.update_data({'city': message.text})


@dp.message_handler(state=UserRegisterState.org_name)
async def register_user(message: Message, state: FSMContext):
    await UserRegisterState.next()
    password_text = _('password_text')
    await message.answer(
        text=password_text,
        reply_markup=numbers_buttons
    )
    await state.update_data({'org_name': message.text})


@dp.callback_query_handler(state=UserRegisterState.password)
async def register_user(call: CallbackQuery, state: FSMContext):
    call_data = call.data
    data = await state.get_data()
    show_password = data.get('show_password', False)
    password = data.get('password', '')
    password_text = _('password_text')

    if call_data.isdigit():
        if len(password) < 6:
            password += call_data
            password_text += hash_password(password, show_password)
            await call.message.edit_text(text=password_text, reply_markup=numbers_buttons)
            await state.update_data({'password': password})
        else:
            await call.answer('Parol uzunligi 6 xonadan ko\'p bo\'la olmaydi!', show_alert=True)

    elif call_data == 'show':
        show_password = not show_password
        if password:
            password_text += hash_password(password, show_password)
            await call.message.edit_text(text=password_text, reply_markup=numbers_buttons)
        await state.update_data({'show_password': show_password})

    elif call_data == 'clear':
        if len(password) > 0:
            password = password[:-1]
            password_text += hash_password(password, show_password)
            await call.message.edit_text(text=password_text, reply_markup=numbers_buttons)
            await state.update_data({'password': password})

    elif call_data == 'submit':
        if len(password) < 4:
            await call.answer('Parol uzunligi 4 xonadan kam bo\'la olmaydi!', show_alert=True)
        else:
            await UserRegisterState.next()
            await call.message.delete()
            await call.message.answer(
                text=makeup_user_info(data=data) + '\n\nBarcha ma\'lumotlar to\'g\'rimi?',
                reply_markup=yes_no_buttons
            )

    await call.answer(cache_time=0)


@dp.message_handler(state=UserRegisterState.save_user, text_contains=_('yes'))
async def register_user(message: Message, state: FSMContext):
    await message.answer(_('saving_process'))
    data = await state.get_data()
    telegram_id = message.from_user.id
    data['telegram_id'] = str(telegram_id)
    resp = await create_user(data)
    await state.reset_data()
    if resp:
        await message.answer(
            'Jarayon yakunlandi, Sabr bilan ma\'lumotlarni kiritganingiz uchun tashakkur. 😊',
            reply_markup=home_buttons
        )
        await state.finish()
    else:
        await UserRegisterState.start_register.set()
        await message.answer(
            "Ro'yxatdan o'tishda xatolik bor. Qayta harakat qiling.",
            reply_markup=register_button
        )


@dp.message_handler(state=UserRegisterState.save_user, text_contains=_('no'))
async def register_user(message: Message, state: FSMContext):
    await UserRegisterState.start_register.set()
    await message.answer(
        'Ro\'yxatdan o\'tish yakunlanmadi. Qayta harakat qiling.',
        reply_markup=register_button
    )
    await state.reset_data()
