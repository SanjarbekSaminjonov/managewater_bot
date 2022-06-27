from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, db
from states.auth import UserRegisterState
from data.words import get_word as _
from keyboards.default import home_buttons, register_button


@dp.message_handler(text_contains=_('cancel'), state=UserRegisterState.all_states)
async def cancel_login_register(message: Message, state: FSMContext):
    await state.reset_data()
    user_id = await db.get_user_id(message.from_user.id)
    if user_id is not None:
        buttons_group = home_buttons
        await state.finish()
    else:
        buttons_group = register_button
        await UserRegisterState.start_register.set()
    await message.answer(
        _('cancelled'),
        reply_markup=buttons_group
    )
