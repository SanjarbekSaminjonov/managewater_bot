from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, db
from states.auth import UserRegisterState
from data.words import get_word as _
from keyboards.default import buttons


@dp.message_handler(text_contains="Bekor qilish", state=UserRegisterState.all_states)
async def cancel_login_register(message: Message, state: FSMContext):
    await state.reset_data()
    user_id = await db.get_user_id(message.from_user.id)
    if user_id is not None:
        buttons_group = [_('add_device'), _('my_devices')]
        await state.finish()
    else:
        buttons_group = [_('register')]
        await UserRegisterState.start_register.set()
    await message.answer(
        _('cancelled'),
        reply_markup=buttons(buttons_group)
    )
