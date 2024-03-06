from datetime import datetime
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from sqlalchemy.orm import sessionmaker, Session

import config

# Это будет inner-мидлварь на сообщения
class Is_Admin(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id == config.ADMIN_ID:
            return await handler(event, data)
        await event.answer('Данная команда доступна только для администатора')
        return


class InitMiddleware(BaseMiddleware):
    def __init__(self,pool: sessionmaker[Session]) -> None:
        self.pool = pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        with self.pool() as session:
            data["session"] = session
            result = await handler(event, data)
        return result