from aiogram.dispatcher.filters.state import State, StatesGroup


class UserRegisterState(StatesGroup):
    start_register = State()
    username = State()
    first_name = State()
    last_name = State()
    region = State()
    city = State()
    org_name = State()
    password = State()
    save_user = State()
