from aiogram import Dispatcher

from . import base


def setup_handlers(dp: Dispatcher):
    base.setup(dp)
    return