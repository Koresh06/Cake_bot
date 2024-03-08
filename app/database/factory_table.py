from sqlalchemy import Engine

from app.database.base import Base


async def create_all_tables(engine: Engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
