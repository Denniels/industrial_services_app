# -*- coding: utf-8 -*-
import psycopg2
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
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
            logger.info("Tablas encontradas:")
            for table in tables:
                logger.info(f"  - {table[0]}")
            
            # Verificar datos en companies
            cur.execute("SELECT COUNT(*) FROM companies;")
            company_count = cur.fetchone()[0]
            logger.info(f"Número de empresas: {company_count}")
            
            # Verificar datos en users
            cur.execute("SELECT COUNT(*) FROM users;")
            user_count = cur.fetchone()[0]
            logger.info(f"Número de usuarios: {user_count}")
            
            # Verificar datos en service_pricing
            cur.execute("SELECT COUNT(*) FROM service_pricing;")
            pricing_count = cur.fetchone()[0]
            logger.info(f"Número de precios de servicios: {pricing_count}")
            
            # Verificar datos en contract_pricing
            cur.execute("SELECT COUNT(*) FROM contract_pricing;")
            contract_count = cur.fetchone()[0]
            logger.info(f"Número de precios de contratos: {contract_count}")
            
        logger.info("✅ Verificación completada exitosamente")
        return True
            
    except Exception as e:
        logger.error(f"❌ Error durante la verificación: {str(e)}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    verify_database()
