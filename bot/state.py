from aiogram.dispatcher.filters.state import StatesGroup, State


class MyPass(StatesGroup):
    input_msr_key = State()


class CreatePass(StatesGroup):
    create_pass = State()


class SavePass(StatesGroup):
    input_name_pass = State()
    input_login = State()
    choose_pass = State()
    input_pass = State()
    input_description = State()
    input_msr_key = State()
