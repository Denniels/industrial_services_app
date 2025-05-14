# -*- coding: ascii -*-
import psycopg2
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/db_check.log', 'w', encoding='ascii'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_connection():
    try:
        conn = psycopg2.connect(
            dbname='integral_service_db',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )
        
        with conn.cursor() as cur:
            cur.execute('SELECT version();')
            version = cur.fetchone()[0]
            logger.info(f'PostgreSQL version: {version}')
            
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = cur.fetchall()
            logger.info('Tablas en la base de datos:')
            for table in tables:
                logger.info(f'  - {table[0]}')
                
        logger.info('Conexion exitosa')
        return True
        
    except Exception as e:
        logger.error(f'Error de conexion: {str(e)}')
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    check_connection()
