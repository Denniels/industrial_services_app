# -*- coding: utf-8 -*-
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database_encoding():
    """Verificar la codificación de la base de datos"""
    try:
        conn = psycopg2.connect(
            dbname='integral_service_db',
            user='postgres',
            password='DAms15820',
            host='localhost',
            port='5432'
        )
        
        cur = conn.cursor()
        
        # Verificar codificación de la base de datos
        cur.execute("SHOW server_encoding;")
        server_encoding = cur.fetchone()[0]
        logger.info(f"Codificación del servidor: {server_encoding}")
        
        # Verificar codificación del cliente
        cur.execute("SHOW client_encoding;")
        client_encoding = cur.fetchone()[0]
        logger.info(f"Codificación del cliente: {client_encoding}")
        
        if server_encoding == 'UTF8' and client_encoding == 'UTF8':
            logger.info("✅ La codificación está configurada correctamente")
        else:
            logger.warning("⚠️ La codificación no está en UTF-8")
            
    except Exception as e:
        logger.error(f"❌ Error durante la verificación: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_database_encoding()
