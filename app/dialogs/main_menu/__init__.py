from aiogram import Dispatcher

from .dialogs import main_menu


def setup(dp: Dispatcher):
    dp.include_router(main_menu)