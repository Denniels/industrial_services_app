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
            dbname='postgres',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Verificar si la base de datos existe
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()
        
        if not exists:
            # Crear base de datos
            cur.execute(f"CREATE DATABASE {db_name}")
            logger.info(f"✅ Base de datos {db_name} creada exitosamente")
        else:
            logger.info(f"Base de datos {db_name} ya existe")
            
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
