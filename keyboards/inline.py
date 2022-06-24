from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


numbers_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="1️⃣", callback_data="1"),
            InlineKeyboardButton(
                text="2️⃣", callback_data="2"),
            InlineKeyboardButton(
                text="3️⃣", callback_data="3"),
        ],
        [
            InlineKeyboardButton(
                text="4️⃣", callback_data="4"),
            InlineKeyboardButton(
                text="5️⃣", callback_data="5"),
            InlineKeyboardButton(
                text="6️⃣", callback_data="6"),
        ],
        [
            InlineKeyboardButton(
                text="7️⃣", callback_data="7"),
            InlineKeyboardButton(
                text="8️⃣", callback_data="8"),
            InlineKeyboardButton(
                text="9️⃣", callback_data="9"),
        ],
        [
            InlineKeyboardButton(
                text="❌", callback_data="clear"),
            InlineKeyboardButton(
                text="0️⃣", callback_data="0"),
            InlineKeyboardButton(
                text="👁", callback_data="show"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Tasdiqlash", callback_data="submit"),
        ]
    ]
)
