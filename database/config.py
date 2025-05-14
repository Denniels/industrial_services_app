# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
import os
import logging
import sys

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv(encoding='utf-8')

# Configuración forzada de encoding para Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Configuración de la base de datos
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'integral_service_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'DAms15820'),
    'port': os.getenv('DB_PORT', '5432'),
    'options': '-c client_encoding=utf8'
}

# Configuración de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost:5432/integral_service_db')

# Opciones específicas de PostgreSQL
POSTGRES_OPTIONS = {
    'pool_size': 20,
    'max_overflow': 10,
    'pool_timeout': 30,
    'pool_recycle': 1800,
    'pool_pre_ping': True,
    'echo': True,
    'isolation_level': 'READ COMMITTED',
    'connect_args': {
        'client_encoding': 'utf8',
        'application_name': 'integral_service_app',
        'options': '-c search_path=public -c client_encoding=utf8 -c timezone=UTC'
    }
}

# Crear el motor de SQLAlchemy con opciones optimizadas
try:
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        **POSTGRES_OPTIONS
    )
    logger.info("Motor de base de datos creado exitosamente")
except Exception as e:
    logger.error(f"Error al crear el motor de base de datos: {str(e)}")
    raise

# Crear clase de sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# Función para obtener la base de datos con manejo de errores
def get_db():
    db = SessionLocal()
    try:
        yield db
        logger.debug("Sesión de base de datos creada")
    except Exception as e:
        logger.error(f"Error en la sesión de base de datos: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()
        logger.debug("Sesión de base de datos cerrada")

# Event listeners para debugging y monitoreo
@event.listens_for(engine, 'connect')
def receive_connect(dbapi_connection, connection_record):
    logger.info("Nueva conexión establecida a la base de datos")

@event.listens_for(engine, 'checkout')
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    logger.debug("Conexión retirada del pool")

@event.listens_for(engine, 'checkin')
def receive_checkin(dbapi_connection, connection_record):
    logger.debug("Conexión devuelta al pool")

# Base declarativa para los modelos
Base = declarative_base()
