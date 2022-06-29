from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, db

from keyboards.default import home_buttons, register_button
from states.auth import UserRegisterState


@dp.message_handler(state=None)
async def bot_echo(message: Message, state: FSMContext):
    user_id = await db.get_user_id(message.from_user.id)
    if user_id is not None:
        await state.finish()
        await message.answer(
            f'Aniqlanmagan buyruq !',
            reply_markup=home_buttons
        )
    else:
        await UserRegisterState.start_register.set()
        await message.answer(
            f'Xurmatli {message.from_user.full_name} siz ro\'yxatdan o\'tmagansiz !\n'
            f'Botdan foydalanish uchun ro\'yxatdan o\'ting.',
            reply_markup=register_button
        )
