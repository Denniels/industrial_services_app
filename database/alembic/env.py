# Se ejecutará cuando se cree una nueva migración
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

# Agregar el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar modelos y configuración
from database.models import Base
from database.config import POSTGRES_OPTIONS

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de la base de datos
config = context.config
db_url = os.getenv("DATABASE_URL")
config.set_main_option("sqlalchemy.url", db_url)

# Interpretar el archivo de configuración para Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Agregar el modelo MetaData para autogeneración
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'
    
    Útil para generar SQL que se puede ejecutar más tarde.
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
    """Ejecutar migraciones en modo 'online'
    
    Crea una conexión a la base de datos y ejecuta las migraciones.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration.update(POSTGRES_OPTIONS)
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Compara tipos de columnas
            compare_server_default=True,  # Compara valores por defecto
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
