from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db

from keyboards.default import home_buttons, register_button
from states.auth import UserRegisterState


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: Message, state: FSMContext):
    await state.finish()
    full_name = await db.get_user_full_name(message.from_user.id)
    if full_name is not None:
        await message.answer(
            f'🙋‍♂ Salom {full_name} yana ko\'rishganimizdan xursandman !',
            reply_markup=home_buttons
        )
    else:
        await UserRegisterState.start_register.set()
        await message.answer(
            f'Salom, {message.from_user.full_name} !\nBotdan foydalanish uchun ro\'yxatdan o\'ting.',
            reply_markup=register_button
        )
