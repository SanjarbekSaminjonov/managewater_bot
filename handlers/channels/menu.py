from aiogram.types import Message

from loader import dp
from data.words import get_word as _
from keyboards.channel_buttons import menu_buttons


@dp.message_handler(text_contains=_('channel_devices'))
async def register_user(message: Message):
    await message.answer(
        _('channel_devices'),
        reply_markup=menu_buttons
    )
