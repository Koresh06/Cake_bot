from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import (
    Const, Format
)
from aiogram_dialog.widgets.kbd import Button, Back

from app.FSM import states


async def window1_get_data(**kwargs):
    return {
        "something": "data from Window1 getter",
    }

async def window2_get_data(**kwargs):
    return {
        "something": "data from Window2 getter",
        }

async def dialog_get_data(**kwargs):
    return {
        "name": "Tishka17",
    }

async def button1_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    dialog_data = manager.dialog_data
    event = manager.event
    middleware_data = manager.middleware_data
    start_data = manager.start_data

main_menu = Dialog(
    Window(
        Format("Hello, {name}"),
        Format("Something: {something}"),
        Button(Const("Next window "), id="button1", on_click=button1_clicked),
        state=states.MainMenuSG.main1,
        getter=window1_get_data
    ),
    Window(
        Format("hello, {name}"), 
        Format("Something: {something}"),
        Format("user input: {dialog_data[user_input]}"),
        Back(text=Const("Back")),
        state=states.MainMenuSG.main2,
        getter=window2_get_data
    ),
    getter=dialog_get_data
)