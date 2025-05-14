# -*- coding: utf-8 -*-
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database():
    """Crear la base de datos si no existe"""
    db_name = 'integral_service_db'
    
    try:
        # Conectar a postgres
        conn = psycopg2.connect(
            dbname='postgres',  # Primero nos conectamos a la base postgres
            user='postgres',    # Usuario por defecto de PostgreSQL
            password='DAms15820',
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Eliminar conexiones existentes a la base de datos
        cur = conn.cursor()
        cur.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{db_name}'
            AND pid <> pg_backend_pid()
        """)
        
        # Eliminar la base de datos si existe
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        logger.info(f"Base de datos {db_name} eliminada (si existía)")
        
        # Crear base de datos nueva
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
        logger.info(f"✅ Base de datos {db_name} creada exitosamente")
            
    except Exception as e:
        logger.error(f"❌ Error al crear la base de datos: {str(e)}")
        raise
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_database()
