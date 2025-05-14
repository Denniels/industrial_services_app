# -*- coding: ascii -*-
import os
import sys
import psycopg2
import logging
from pathlib import Path

# Configurar logging básico
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'database_diagnostic.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def check_environment():
    """Verificar variables de entorno y configuración"""
    logger.info("=== Verificacion del Entorno ===")
    
    # Verificar Python
    logger.info(f"Version de Python: {sys.version}")
    logger.info(f"Encoding por defecto: {sys.getdefaultencoding()}")
    logger.info(f"Encoding del filesystem: {sys.getfilesystemencoding()}")
    
    # Variables de entorno importantes
    env_vars = ['PYTHONIOENCODING', 'PGCLIENTENCODING', 'DATABASE_URL']
    for var in env_vars:
        logger.info(f"{var}: {os.getenv(var, 'no definido')}")

def check_database_connection():
    """Verificar conexión a la base de datos"""
    logger.info("\n=== Verificacion de Base de Datos ===")
    
    try:
        # Intentar conexión a postgres primero
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )
        
        with conn.cursor() as cur:
            # Verificar versión
            cur.execute('SELECT version();')
            version = cur.fetchone()[0]
            logger.info(f"Version PostgreSQL: {version}")
            
            # Listar bases de datos
            cur.execute("""
                SELECT datname, encoding::int, 
                pg_encoding_to_char(encoding) as encoding_name
                FROM pg_database
                WHERE datistemplate = false;
            """)
            databases = cur.fetchall()
            logger.info("\nBases de datos:")
            for db in databases:
                logger.info(f"  - {db[0]} (encoding: {db[2]})")
        
        conn.close()
        
        # Intentar conexión a integral_service_db
        conn = psycopg2.connect(
            dbname='integral_service_db',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )
        
        with conn.cursor() as cur:
            # Verificar tablas
            cur.execute("""
                SELECT table_name, pg_size_pretty(pg_total_relation_size(quote_ident(table_name))) as size
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY pg_total_relation_size(quote_ident(table_name)) DESC;
            """)
            tables = cur.fetchall()
            logger.info("\nTablas en integral_service_db:")
            for table in tables:
                logger.info(f"  - {table[0]} (tamano: {table[1]})")
            
            # Verificar configuración
            cur.execute("SHOW ALL;")
            settings = cur.fetchall()
            logger.info("\nConfiguracion relevante:")
            important_settings = ['client_encoding', 'server_encoding', 'timezone']
            for setting in settings:
                if setting[0] in important_settings:
                    logger.info(f"  - {setting[0]}: {setting[1]}")
        
        logger.info("\n✅ Verificacion completada exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"\n❌ Error durante la verificacion: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    try:
        check_environment()
        check_database_connection()
    except Exception as e:
        logger.error(f"Error general: {str(e)}")
    finally:
        logger.info("\nRevisa el archivo logs/database_diagnostic.log para mas detalles")
