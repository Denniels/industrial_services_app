# -*- coding: utf-8 -*-
import psycopg2
import click
import os
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

def get_connection_params(database="postgres"):
    """Obtener parámetros de conexión"""
    return {
        "host": "localhost",
        "port": "5432",
        "user": "postgres",
        "password": "DAms15820",
        "database": database
    }

@click.group()
def cli():
    """Herramientas de administración de PostgreSQL"""
    pass

@cli.command()
def create_database():
    """Crear la base de datos integral_service_db"""
    params = get_connection_params()
    
    try:
        # Conectar a postgres (base de datos por defecto)
        logger.info("Conectando al servidor PostgreSQL...")
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Verificar si la base de datos existe
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'integral_service_db'")
        exists = cur.fetchone()
        
        if not exists:
            logger.info("Creando base de datos integral_service_db...")
            cur.execute('CREATE DATABASE integral_service_db')
            logger.info("✓ Base de datos creada exitosamente")
        else:
            logger.info("La base de datos ya existe")
        
        cur.close()
        conn.close()
        
        # Conectar a la base de datos creada
        params["database"] = "integral_service_db"
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Crear extensiones necesarias
        logger.info("Configurando extensiones...")
        cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
        
        # Configurar el esquema
        logger.info("Configurando esquema...")
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS public;
            GRANT ALL ON SCHEMA public TO postgres;
            GRANT ALL ON SCHEMA public TO public;
        """)
        
        logger.info("✓ Base de datos configurada correctamente")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

@cli.command()
def check_connection():
    """Verificar la conexión a la base de datos"""
    params = get_connection_params("integral_service_db")
    
    try:
        logger.info("Verificando conexión...")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        # Verificar versión
        cur.execute('SELECT version()')
        version = cur.fetchone()[0]
        logger.info(f"Versión de PostgreSQL: {version}")
        
        # Verificar extensiones
        cur.execute("""
            SELECT extname, extversion 
            FROM pg_extension 
            WHERE extname = 'uuid-ossp'
        """)
        extensions = cur.fetchall()
        logger.info("Extensiones instaladas:")
        for ext in extensions:
            logger.info(f"  - {ext[0]} v{ext[1]}")
        
        # Verificar esquemas
        cur.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name NOT LIKE 'pg_%' 
            AND schema_name != 'information_schema'
        """)
        schemas = cur.fetchall()
        logger.info("Esquemas disponibles:")
        for schema in schemas:
            logger.info(f"  - {schema[0]}")
        
        logger.info("✓ Conexión exitosa")
        return True
        
    except Exception as e:
        logger.error(f"Error de conexión: {str(e)}")
        return False
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

@cli.command()
def list_tables():
    """Listar todas las tablas de la base de datos"""
    params = get_connection_params("integral_service_db")
    
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                table_schema,
                table_name,
                (SELECT count(*) FROM information_schema.columns 
                 WHERE table_name=t.table_name) as columns
            FROM information_schema.tables t
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY table_schema, table_name;
        """)
        
        tables = cur.fetchall()
        if tables:
            logger.info("\nTablas en la base de datos:")
            for schema, table, cols in tables:
                logger.info(f"  - {schema}.{table} ({cols} columnas)")
        else:
            logger.info("No hay tablas en la base de datos")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    cli()
