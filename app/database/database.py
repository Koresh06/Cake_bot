from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.engine import make_url
from app.config import DbConfig



def create_pool(db_config: DbConfig) -> async_sessionmaker[AsyncSession]:
    engine = create_engine(db_config)
    return create_sessionmaker(engine)

def create_engine_db(db_config: DbConfig) -> AsyncEngine:
    return create_async_engine(url=make_url(db_config.uri), echo=db_config.echo)

def create_sessionmaker(engine) -> async_sessionmaker[AsyncSession]:
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )
    return pool