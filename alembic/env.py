from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Импортируйте ваши модели
from db.models import Base

# Это объект конфигурации Alembic, который предоставляет доступ к значениям из .ini файла
config = context.config

# Интерпретируем файл конфигурации для Python логирования.
# Эта строка настраивает логгеры.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Добавьте объект MetaData вашей модели здесь для поддержки 'autogenerate'
target_metadata = Base.metadata

# Другие значения из конфигурации, определенные нуждами env.py,
# можно получить следующим образом:
# my_important_option = config.get_main_option("my_important_option")
# ... и так далее.


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме.

    Настраивает контекст только с URL и без Engine,
    хотя здесь также допустим Engine. Пропуская создание Engine,
    нам даже не нужно, чтобы был доступен DBAPI.

    Вызовы context.execute() здесь исполняют заданную строку в
    вывод скрипта.

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
    """Запуск миграций в 'online' режиме.

    В этом сценарии нам нужно создать Engine
    и ассоциировать соединение с контекстом.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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
