import asyncio

from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models import Base
from tree import build_tree, traverse_tree
from utils import create_engine


async def async_main():
    engine = create_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        async with session.begin():
            await build_tree(session, 0, 0)

        result_nodes = await traverse_tree(session, 'title', 'desc', 0)
        for node in result_nodes:
            print(node)
        await session.commit()


if __name__ == '__main__':
    asyncio.run(async_main())
