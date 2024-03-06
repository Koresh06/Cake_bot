from datetime import datetime

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import (
    Const,
)

from app.FSM import states


main_menu = Dialog(
    Window(
        Const("<b>Главное меню</b>"),
        state=states.MainMenuSG.main,
    )
)