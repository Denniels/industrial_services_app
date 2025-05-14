# -*- coding: ascii -*-
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging
import os
import sys

# Configurar logging con codificacion ASCII
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def create_database():
    """Crear la base de datos si no existe"""
    db_name = 'integral_service_db'
    conn = None
    
    try:
        # Conectar a postgres con codificacion ASCII
        conn = psycopg2.connect(
            dbname='integral_service_db',
            user='postgres',
            password='DAms15820',
            host='localhost',
            port='5432',
            options='-c client_encoding=SQL_ASCII'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Verificar si la base de datos existe
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()
        
        if not exists:
            # Crear base de datos con configuracion segura
            create_command = """
            CREATE DATABASE integral_service_db
            WITH 
                OWNER = postgres
                ENCODING = 'UTF8'
                LC_COLLATE = 'C'
                LC_CTYPE = 'C'
                TEMPLATE = template0
                CONNECTION LIMIT = -1;
            """
            cur.execute(create_command)
            logger.info(f"Base de datos {db_name} creada exitosamente")
        else:
            logger.info(f"Base de datos {db_name} ya existe")
            
        # Crear esquema
        conn.close()
        conn = psycopg2.connect(
            dbname=db_name,
            user='postgres',
            password='admin',
            host='localhost',
            port='5432',
            options='-c client_encoding=SQL_ASCII'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Leer y ejecutar el esquema
        schema_path = os.path.join(os.path.dirname(__file__), 'schema_new.sql')
        with open(schema_path, 'r', encoding='ascii') as f:
            schema_sql = f.read()
            
        with conn.cursor() as cur:
            cur.execute(schema_sql)
            logger.info("Esquema creado exitosamente")
        
        return True
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    if create_database():
        logger.info("Inicializacion completada exitosamente")
        sys.exit(0)
    else:
        logger.error("Error en la inicializacion")
        sys.exit(1)
