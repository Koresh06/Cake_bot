from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Engine

from app.database.base import Base

def create_all_table(engine: Engine):
    Base.metadata.create_all(engine)