# -*- coding: ascii -*-
import psycopg2
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def verify_database():
    """Verificar el estado de la base de datos"""
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            dbname='integral_service_db',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )
        
        with conn.cursor() as cur:
            # Verificar las tablas
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cur.fetchall()
            logger.info("=== Tablas encontradas ===")
            for table in tables:
                logger.info(f"  - {table[0]}")
                
                # Contar registros en cada tabla
                cur.execute(f"SELECT COUNT(*) FROM {table[0]};")
                count = cur.fetchone()[0]
                logger.info(f"    Registros: {count}")
            
            # Verificar tipos ENUM
            cur.execute("""
                SELECT t.typname, e.enumlabel
                FROM pg_type t 
                JOIN pg_enum e ON t.oid = e.enumtypid
                ORDER BY t.typname, e.enumsortorder;
            """)
            enums = cur.fetchall()
            logger.info("\n=== Tipos ENUM ===")
            current_type = None
            for enum in enums:
                if enum[0] != current_type:
                    current_type = enum[0]
                    logger.info(f"\n  {current_type}:")
                logger.info(f"    - {enum[1]}")
            
            # Verificar servidor PostgreSQL
            cur.execute("SHOW server_encoding;")
            server_encoding = cur.fetchone()[0]
            cur.execute("SHOW client_encoding;")
            client_encoding = cur.fetchone()[0]
            cur.execute("SHOW timezone;")
            timezone = cur.fetchone()[0]
            
            logger.info("\n=== Configuracion del Servidor ===")
            logger.info(f"  Codificacion del servidor: {server_encoding}")
            logger.info(f"  Codificacion del cliente: {client_encoding}")
            logger.info(f"  Zona horaria: {timezone}")
            
        logger.info("\n✅ Verificacion completada exitosamente")
        return True
            
    except Exception as e:
        logger.error(f"\n❌ Error durante la verificacion: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    verify_database()
