from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.models.base import Base

meta = Base.metadata
async def create_engine(echo=False):
    engine = create_async_engine(
        "sqlite+aiosqlite:///database.db", 
        future=True,
        echo=echo,
    )

    async with engine.begin() as conn: 
        # await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)
                            
    return engine


def create_session_pool(engine):
    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool