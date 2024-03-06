from aiogram import Dispatcher
from aiogram.filters import Filter
from aiogram.fsm.state import State
from aiogram_dialog import StartMode, ShowMode, DialogManager


class StartDialog:
    def __init__(
        self,
        state: State,
        dp: Dispatcher,
        start_mode: StartMode = StartMode.NORMAL,
        show_mode: ShowMode = ShowMode.AUTO,
    ):
      self.state = state
      self.dp = dp
      self.start_mode = start_mode
      self.show_mode = show_mode

    async def start_dialog(
        self,
        _,
        dialog_manager: DialogManager,
    ) -> None:
        await dialog_manager.start(self.state, mode=self.start_mode, show_mode=self.show_mode)

    def message(self, *filters: Filter):
        self.dp.message.register(
            self.start_dialog,
            *filters,
        )

    def callback_query(self, *filters: Filter):
        self.dp.callback_query.register(
            self.start_dialog,
            *filters,
        )

    def errors(self, *filters: Filter):
        self.dp.errors.register(
            self.start_dialog,
            *filters,
        )