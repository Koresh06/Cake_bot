from aiogram.fsm.state import State, StatesGroup


class Add_categories(StatesGroup):
    name = State()

class Update_product(StatesGroup):
    name = State()
    image = State()
    description = State()
    price =  State()

class Collecting_the_cake(StatesGroup):
    event = State()
    description = State()
    image = State()