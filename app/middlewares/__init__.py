from aiogram import Dispatcher
from sqlalchemy.orm import Session, sessionmaker

from app.middlewares.middleware import InitMiddleware


def setup_middlewares(
    dp: Dispatcher,
    pool: sessionmaker[Session],
):
    dp.update.middleware(InitMiddleware(pool=pool))