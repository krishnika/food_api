from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from api import db, app
from sqlalchemy.dialects import mysql
from sqlalchemy.sql.expression import true, false

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
config.set_main_option(
    'sqlalchemy.url', app.config.get('SQLALCHEMY_DATABASE_URI')
)
target_metadata = db.metadata


def compare_type(context, inspected_column, metadata_column, inspected_type,
                 metadata_type):
    if type(metadata_type) == db.Boolean:
        if type(inspected_type) == mysql.base.TINYINT:
            return False


def compare_server_default(context, inspected_column, metadata_column,
                           inspected_default, metadata_default,
                           rendered_metadata_default):
    if type(metadata_column.type) == db.Boolean:
        if type(inspected_column['type']) == mysql.base.TINYINT:
            if inspected_default == "'1'":
                return metadata_default == true
            elif inspected_default == "'0'":
                return metadata_default == false


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
