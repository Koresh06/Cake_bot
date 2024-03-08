from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy.orm import Session, sessionmaker

from app.config import Config
from app.dialogs import setup_dialogs
from app.handlers.base import setup_handlers
from app.middlewares import setup_middlewares


def create_bot(config: Config) -> Bot:
    return Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

def create_dispather(pool: sessionmaker[Session]) -> Dispatcher:
    dp = Dispatcher()
    setup_middlewares(dp=dp, pool=pool)
    setup_handlers(dp)
    setup_dialogs(dp)
    return dp