import sys
import os
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
from dotenv import load_dotenv

from app.core.config import settings
from app.models.file import Base

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


config.set_main_option("sqlalchemy.url", settings.database_url)
target_metadata = Base.metadata


engine = create_async_engine(settings.database_url, future=True)


async def run_migrations_async():

    async with engine.begin() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,  # Используется для поддержки SQLite, можно убрать, если не нужно
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    asyncio.run(run_migrations_async())


def run_migrations_offline():
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
