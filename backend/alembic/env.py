import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


# --- 1. Path Configuration: Make the 'app' module importable ---
# Get the directory of the current file (env.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the 'backend' directory (one level up from 'alembic')
backend_dir = os.path.join(current_dir, '..')
# Add the 'backend' directory to the Python path
sys.path.insert(0, backend_dir)


# --- 2. Load the application's models and Base ---
# Now that the path is set, we can import from 'app'
from app.db import Base
from app import models  # This ensures Alembic sees all your models


# --- 3. Load Environment Variables from .env file ---
from dotenv import load_dotenv

# Construct the path to the .env file at the project root
project_root = os.path.join(backend_dir, '..')
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set or .env file is not found.")


# --- 4. Alembic Configuration ---
config = context.config

# Set the database URL for Alembic from our loaded environment variable
config.set_main_option('sqlalchemy.url', DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()