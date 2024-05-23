# states.py
from aiogram.filters.state import State, StatesGroup

class Form(StatesGroup):
    username = State()
    email = State()
    password = State()
    username_auth = State()
    password_auth = State()
