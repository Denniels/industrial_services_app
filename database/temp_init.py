# -*- coding: ascii -*-
import psycopg2
import logging
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    try:
        # Conectar a postgres
        logger.info("Conectando a PostgreSQL...")
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        db_name = 'integral_service_db'
        
        with conn.cursor() as cur:
            # Verificar si la base de datos existe
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            if not cur.fetchone():
                # Crear base de datos
                cur.execute(f"CREATE DATABASE {db_name}")
                logger.info(f"Base de datos {db_name} creada")
            else:
                logger.info(f"Base de datos {db_name} ya existe")
                
        # Conectar a la base de datos creada
        conn.close()
        conn = psycopg2.connect(
            dbname=db_name,
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Ejecutar el esquema
        with open('database/schema_new.sql', 'r', encoding='ascii') as f:
            schema = f.read()
            
        with conn.cursor() as cur:
            cur.execute(schema)
            logger.info("Esquema creado exitosamente")
            
        logger.info("Inicialización completada")
        return True
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    init_db()
