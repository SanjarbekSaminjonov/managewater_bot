from aiogram.dispatcher.filters.state import StatesGroup, State


class ChannelRegisterState(StatesGroup):
    device_id = State()
    phone = State()
    name = State()
    height = State()
    location = State()
    save_basin = State()
