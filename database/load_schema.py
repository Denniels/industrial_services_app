# -*- coding: utf-8 -*-
import psycopg2
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_schema():
    """Cargar el esquema en la base de datos"""
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            dbname='integral_service_db',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        
        # Leer el archivo de esquema
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Ejecutar el script SQL
        with conn.cursor() as cur:
            cur.execute("SET client_encoding TO 'UTF8'")
            cur.execute(schema_sql)
            logger.info("✅ Esquema cargado exitosamente")
            
    except Exception as e:
        logger.error(f"❌ Error al cargar el esquema: {str(e)}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    load_schema()
