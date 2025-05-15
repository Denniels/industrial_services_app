# -*- coding: utf-8 -*-
import os
import sys
import locale
import psycopg2
from database.models import DATABASE_CONFIG
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/system_check.log',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

def check_system_encoding():
    """Verificar la codificaci√≥n del sistema"""
    logger.info("Verificando codificaci√≥n del sistema...")
    
    # Verificar Python
    logger.info(f"Python default encoding: {sys.getdefaultencoding()}")
    logger.info(f"Filesystem encoding: {sys.getfilesystemencoding()}")
    logger.info(f"Locale: {locale.getpreferredencoding()}")
    
    # Verificar variables de entorno
    logger.info(f"PYTHONIOENCODING: {os.environ.get('PYTHONIOENCODING')}")
    logger.info(f"LANG: {os.environ.get('LANG')}")
    
    # Verificar stdout/stderr
    logger.info(f"stdout encoding: {sys.stdout.encoding}")
    logger.info(f"stderr encoding: {sys.stderr.encoding}")

def check_database_encoding():
    """Verificar la codificaci√≥n de la base de datos"""
    logger.info("Verificando codificaci√≥n de la base de datos...")
    
    try:
        conn = psycopg2.connect(
            host=DATABASE_CONFIG['host'],
            database=DATABASE_CONFIG['database'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password']
        )
        cur = conn.cursor()
        
        # Verificar codificaci√≥n de la base de datos
        cur.execute("SHOW server_encoding")
        server_encoding = cur.fetchone()[0]
        logger.info(f"Server encoding: {server_encoding}")
        
        # Verificar codificaci√≥n del cliente
        cur.execute("SHOW client_encoding")
        client_encoding = cur.fetchone()[0]
        logger.info(f"Client encoding: {client_encoding}")
        
        # Verificar LC_COLLATE
        cur.execute("SHOW lc_collate")
        lc_collate = cur.fetchone()[0]
        logger.info(f"LC_COLLATE: {lc_collate}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error al verificar base de datos: {str(e)}")

def test_special_chars():
    """Probar caracteres especiales"""
    logger.info("Probando caracteres especiales...")
    
    test_string = "√°√©√≠√≥√∫√±√Å√â√ç√ì√ö√ë"
    
    # Probar codificaci√≥n
    try:
        encoded = test_string.encode('utf-8')
        decoded = encoded.decode('utf-8')
        logger.info("Prueba de codificaci√≥n exitosa")
        logger.info(f"Original: {test_string}")
        logger.info(f"Encoded: {encoded}")
        logger.info(f"Decoded: {decoded}")
    except Exception as e:
        logger.error(f"Error en prueba de codificaci√≥n: {str(e)}")

if __name__ == "__main__":
    print("üîç Iniciando verificaci√≥n del sistema...")
    check_system_encoding()
    check_database_encoding()
    test_special_chars()
    print("‚úÖ Verificaci√≥n completada. Revise logs/system_check.log para m√°s detalles.")
