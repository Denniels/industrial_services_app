# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
import os
import logging
import sys
from contextlib import contextmanager

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
    'options': '-c client_encoding=utf8 -c standard_conforming_strings=on',
    'client_encoding': 'utf8'
}

def get_database_url():
    """Obtener URL de conexión a la base de datos con la configuración correcta"""
    return f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@" \
           f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}" \
           f"?client_encoding=utf8"

# Crear el motor de base de datos con la configuración correcta
engine = create_engine(
    get_database_url(),
    pool_size=5,
    max_overflow=10,
    echo=False,
    poolclass=QueuePool,
    connect_args={'options': DATABASE_CONFIG['options']}
)

# Configurar eventos de conexión
@event.listens_for(engine, 'connect')
def configure_connection(dbapi_connection, connection_record):
    """Configurar la conexión cuando se establece"""
    cursor = dbapi_connection.cursor()
    cursor.execute("SET client_encoding TO 'utf8';")
    cursor.execute("SET standard_conforming_strings TO on;")
    cursor.close()

# Crear fábrica de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Crear sesión con scope
ScopedSession = scoped_session(SessionLocal)

def get_session():
    """Obtener una nueva sesión de base de datos"""
    session = ScopedSession()
    try:
        return session
    except Exception as e:
        logger.error(f"Error al crear sesión: {str(e)}")
        session.close()
        raise

def get_db():
    """Generator para obtener una sesión de base de datos"""
    session = ScopedSession()
    try:
        yield session
    finally:
        session.close()

# Base para modelos declarativos
Base = declarative_base()
