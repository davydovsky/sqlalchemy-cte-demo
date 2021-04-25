import pytest
from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import AsyncSession

from models import Base
from tree import traverse_tree, build_tree
from utils import create_engine

config = dotenv_values(".env")


@pytest.fixture(scope="session")
def engine():
    engine = create_engine()
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture()
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def session(engine, create):
    async with AsyncSession(engine) as session:
        yield session


@pytest.fixture(autouse=True)
async def build_tree_fixture(session):
    await build_tree(session, 0, 0)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "depth,expected_len",
    [(0, 1), (1, 6), (2, 31), (3, 156), (4, 781)], indirect=True)
async def test_one(session, depth, expected_len):
    assert len(await traverse_tree(session, depth=depth)) == expected_len
