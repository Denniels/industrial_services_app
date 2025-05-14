# -*- coding: utf-8 -*-
import psycopg2
import logging
import os
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_database_encoding():
    """Verificar y corregir la codificación de la base de datos"""
    load_dotenv()
    db_url = os.getenv('DATABASE_URL')
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(db_url)
        conn.set_client_encoding('UTF8')
        
        with conn.cursor() as cur:
            # Verificar codificación de la base de datos
            cur.execute("SHOW server_encoding;")
            server_encoding = cur.fetchone()[0]
            logger.info(f"Codificación del servidor: {server_encoding}")
            
            cur.execute("SHOW client_encoding;")
            client_encoding = cur.fetchone()[0]
            logger.info(f"Codificación del cliente: {client_encoding}")
            
            # Verificar configuración de LC_COLLATE y LC_CTYPE
            cur.execute("SELECT datcollate, datctype FROM pg_database WHERE datname = current_database();")
            collate, ctype = cur.fetchone()
            logger.info(f"LC_COLLATE: {collate}")
            logger.info(f"LC_CTYPE: {ctype}")
            
            # Verificar codificación de las columnas de texto
            cur.execute("""
                SELECT table_name, column_name, character_maximum_length, collation_name
                FROM information_schema.columns
                WHERE data_type IN ('character varying', 'character', 'text')
                  AND table_schema = 'public';
            """)
            columns = cur.fetchall()
            
            logger.info("\nColumnas de texto encontradas:")
            for table, column, length, collation in columns:
                logger.info(f"Tabla: {table}, Columna: {column}, Longitud: {length}, Collation: {collation}")
            
            # Verificar si hay caracteres problemáticos
            for table, column, _, _ in columns:
                cur.execute(f"""
                    SELECT COUNT(*)
                    FROM {table}
                    WHERE {column} ~ '[^\\x00-\\x7F]';
                """)
                non_ascii_count = cur.fetchone()[0]
                if non_ascii_count > 0:
                    logger.warning(f"⚠️ Se encontraron {non_ascii_count} registros con caracteres no ASCII en {table}.{column}")
            
            logger.info("\n✅ Verificación de codificación completada")
            
    except Exception as e:
        logger.error(f"❌ Error durante la verificación: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_database_encoding()
