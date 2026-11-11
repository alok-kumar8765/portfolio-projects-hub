
from logging.config import fileConfig

from alembic import context

from database.connection import Base, engine
from database import models


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Load all SQLAlchemy models.
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations without a database connection."""

    context.configure(
        url=engine.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations using the application's database engine."""

    with engine.connect() as connection:

        print("\n========== ALEMBIC DATABASE ==========")
        print("Using database:", engine.url.database)
        print("Existing tables:", connection.dialect.get_table_names(connection))
        print("======================================\n")

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
