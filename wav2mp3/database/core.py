from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from wav2mp3 import config


engine = create_async_engine(url=config.SQLALCHEMY_DB_CONN_STRING)

async_session = async_sessionmaker(bind=engine)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
