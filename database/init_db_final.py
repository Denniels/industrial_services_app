# -*- coding: utf-8 -*-
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging
import os
import sys
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/db_init.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def create_database():
    """Crear la base de datos si no existe"""
    db_name = 'integral_service_db'
    conn = None
    
    try:
        # Conectar a postgres (base de datos por defecto)
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='DAms15820',
            host='localhost',
            port='5432',
            client_encoding='utf8'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Verificar si la base de datos existe
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()
        
        if not exists:
            # Crear base de datos con soporte UTF-8
            cur.execute(f"""
                CREATE DATABASE {db_name}
                WITH 
                    OWNER = postgres
                    ENCODING = 'UTF8'
                    LC_COLLATE = 'Spanish_Spain.1252'
                    LC_CTYPE = 'Spanish_Spain.1252'
                    TEMPLATE = template0
                    CONNECTION LIMIT = -1;
            """)
            logger.info(f"Base de datos {db_name} creada exitosamente")
        else:
            logger.info(f"La base de datos {db_name} ya existe")
            
    except Exception as e:
        logger.error(f"Error al crear la base de datos: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()
            
def init_schema():
    """Inicializar el esquema de la base de datos"""
    try:
        # Conectar a la base de datos creada
        conn = psycopg2.connect(
            dbname='integral_service_db',
            user='postgres',
            password='DAms15820',
            host='localhost',
            port='5432',
            client_encoding='utf8'
        )
        
        cur = conn.cursor()
        
        # Leer y ejecutar el script SQL
        schema_path = Path(__file__).parent / 'schema_new.sql'
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            
        cur.execute(sql_script)
        conn.commit()
        logger.info("Esquema de base de datos inicializado exitosamente")
        
    except Exception as e:
        logger.error(f"Error al inicializar el esquema: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    try:
        create_database()
        init_schema()
        logger.info("Inicialización de la base de datos completada con éxito")
    except Exception as e:
        logger.error(f"Error durante la inicialización: {str(e)}")
        sys.exit(1)
