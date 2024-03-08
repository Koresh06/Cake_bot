from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram_dialog import ShowMode

from app.FSM import states
from app.utils.router import StartDialog


def setup(dp: Dispatcher):
    main_menu = StartDialog(
        dp=dp,
        state=states.MainMenuSG.main1,
        show_mode=ShowMode.SEND,
    )
    main_menu.message(Command("start"))