from logging.config import fileConfig
import os # <-- IMPORT OS MODULE HERE FOR ENVIRONMENT VARIABLES

from sqlalchemy import engine_from_config
from sqlalchemy import pool


from alembic import context


from app.database.base import Base


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


# Ensure all your models are imported here so Alembic can discover them.
# This is crucial for 'autogenerate' to work correctly.
from app.models import user
# from app.models import other_model_if_you_have_any # Example for future models


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an actual Python connection.
    """
    # In offline mode, we still need to get the URL
    # We will get it directly from the DATABASE_URL environment variable
    url = os.environ.get("DATABASE_URL")
    if url is None:
        raise Exception("DATABASE_URL environment variable is not set!")

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
    # In online mode, we also get the URL from the environment variable
    db_url = os.environ.get("DATABASE_URL")
    if db_url is None:
        raise Exception("DATABASE_URL environment variable is not set!")

    # Pass the URL to engine_from_config
    connectable = engine_from_config(
        {'sqlalchemy.url': db_url}, # <-- Pass the URL directly here
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

