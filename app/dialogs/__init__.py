from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs as set_dialogs

from app.dialogs import (
    main_menu,
)


def setup_dialogs(dp: Dispatcher):
    main_menu.setup(dp)
    set_dialogs(dp)