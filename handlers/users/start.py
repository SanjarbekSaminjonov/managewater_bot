from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db

from data.words import get_words
from keyboards.default import buttons
from states.auth import UserRegisterState


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = await db.get_user_id(message.from_user.id)
    if user_id is not None:
        full_name = await db.get_user_full_name(message.from_user.id)
        buttons_group = ['add_device', 'my_devices']
    else:
        full_name = message.from_user.full_name
        buttons_group = ['register']
        await UserRegisterState.start_register.set()
    await message.answer(
        f"Salom, {full_name}!",
        reply_markup=buttons(get_words(buttons_group))
    )
