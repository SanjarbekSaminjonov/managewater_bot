from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp
from data.words import get_word as _
from data.regions import regions_list, districts_list
from states.auth import UserRegisterState
from keyboards.default import contact_button, buttons
from keyboards.inline import numbers_buttons


@dp.message_handler(text_contains=_('register'), state=UserRegisterState.start_register)
async def register_user(message: Message):
    await UserRegisterState.next()
    await message.answer(
        text=_('request_phone_number'),
        reply_markup=contact_button(_('request_contact'), _('cancel'))
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
async def register(message: Message, state: FSMContext):
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
async def register(message: Message, state: FSMContext):
    await UserRegisterState.next()
    await message.answer(
        _('request_org_name'),
        reply_markup=buttons([_('cancel')])
    )
    await state.update_data({'city': message.text})


@dp.message_handler(state=UserRegisterState.org_name)
async def register(message: Message, state: FSMContext):
    await UserRegisterState.next()
    password_text = "Barcha ma'lumotlaringiz xavfsizligi uchun parol kiriting.\n"
    password_text += "<i>Parol uzunligi 4 - 6 xonali bo'lishi lozim</i>\n\n"
    password_text += "Parol:"
    await message.answer(
        text=password_text,
        reply_markup=numbers_buttons
    )
    await state.update_data({'org_name': message.text})
    data = await state.get_data()
    print(data)


@dp.callback_query_handler(state=UserRegisterState.password)
async def register(call: CallbackQuery, state: FSMContext):
    call_data = call.data
    data = await state.get_data()
    show_password = data.get('show_password', False)
    password = data.get('password', '')
    password_text = _('password_text')

    if call_data.isdigit():
        if len(password) <= 6:
            password += call_data
            password_text += f"<b>{password if show_password else '*' * len(password)}</b>"
            await call.message.edit_text(text=password_text, reply_markup=numbers_buttons)
            await state.update_data({"password": password})
        else:
            await call.answer("Parol uzunligi 6 xonadan ko\'p bo'la olmadi!", show_alert=True)

    elif call_data == "show":
        show_password = not show_password
        if password:
            password_text += f"<b>{password if show_password else '*' * len(password)}</b>"
            await call.message.edit_text(text=password_text, reply_markup=numbers_buttons)
        await state.update_data({"show_password": show_password})

    elif call_data == "clear":
        if len(password) > 0:
            password = password[:-1]
            password_text += f"<b>{password if show_password else '*' * len(password)}</b>"
            await call.message.edit_text(text=password_text, reply_markup=numbers_buttons)
            await state.update_data({"password": password})

    elif call_data == "submit":
        if len(password) < 4:
            await call.answer("Parol kamida 4 xonadan iborat bo'lishi kerak!", show_alert=True)
    #     else:
    #         await UserRegisterState.next()
    #         await call.message.delete()
    #         await call.message.answer(
    #             text=local_services.users.makeup_user_info(data=data) + "\n\nBarcha ma'lumotlar to'g'rimi?",
    #             reply_markup=default.yes_no_buttons
    #         )

    await call.answer(cache_time=0)
