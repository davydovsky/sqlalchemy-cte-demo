from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


def create_engine() -> AsyncEngine:
    """Create Sqlalchemy engine."""
    config = dotenv_values(".env")

    driver = 'postgresql+asyncpg'
    user = config['POSTGRES_USER']
    password = config['POSTGRES_PASSWORD']
    host = config['POSTGRES_HOST']
    db_name = config['POSTGRES_DB']

    return create_async_engine(f"{driver}://{user}:{password}@{host}/{db_name}")
