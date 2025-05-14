# -*- coding: utf-8 -*-
import click
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import logging
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import subprocess

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

def get_db_url_parts():
    """Obtener las partes de la URL de la base de datos"""
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL no está definida en las variables de entorno")
    
    # postgresql://user:password@host:port/dbname
    parts = db_url.split('//')
    credentials = parts[1].split('@')[0]
    host_port = parts[1].split('@')[1].split('/')[0]
    dbname = parts[1].split('/')[-1]
    
    user, password = credentials.split(':')
    host, port = host_port.split(':')
    
    return {
        'user': user,
        'password': password,
        'host': host,
        'port': port,
        'dbname': dbname
    }

@click.group()
def cli():
    """Herramienta de administración de base de datos para Integral Service SPA"""
    pass

@cli.command()
def create_db():
    """Crear la base de datos y sus tablas"""
    try:
        db_parts = get_db_url_parts()
        
        # Conectar a postgres para crear la base de datos
        conn = psycopg2.connect(
            user=db_parts['user'],
            password=db_parts['password'],
            host=db_parts['host'],
            port=db_parts['port']
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        with conn.cursor() as cur:
            # Verificar si la base de datos existe
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_parts['dbname'],))
            if not cur.fetchone():
                cur.execute(f"CREATE DATABASE {db_parts['dbname']}")
                logger.info(f"Base de datos {db_parts['dbname']} creada exitosamente")
            else:
                logger.info(f"La base de datos {db_parts['dbname']} ya existe")
        
        # Inicializar las tablas y datos
        from database.init_db import init_db
        init_db()
        
    except Exception as e:
        logger.error(f"Error al crear la base de datos: {str(e)}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()

@cli.command()
def drop_db():
    """Eliminar la base de datos (¡CUIDADO!)"""
    if click.confirm('¿Estás seguro de que quieres eliminar la base de datos? Esta acción no se puede deshacer'):
        try:
            db_parts = get_db_url_parts()
            
            conn = psycopg2.connect(
                user=db_parts['user'],
                password=db_parts['password'],
                host=db_parts['host'],
                port=db_parts['port']
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            
            with conn.cursor() as cur:
                cur.execute(f"DROP DATABASE IF EXISTS {db_parts['dbname']}")
            
            logger.info(f"Base de datos {db_parts['dbname']} eliminada exitosamente")
            
        except Exception as e:
            logger.error(f"Error al eliminar la base de datos: {str(e)}")
            sys.exit(1)
        finally:
            if conn:
                conn.close()

@cli.command()
@click.argument('name')
def make_migration(name):
    """Crear una nueva migración"""
    try:
        subprocess.run(['alembic', 'revision', '--autogenerate', '-m', name], check=True)
        logger.info(f"Migración '{name}' creada exitosamente")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al crear la migración: {str(e)}")
        sys.exit(1)

@cli.command()
def migrate():
    """Ejecutar las migraciones pendientes"""
    try:
        subprocess.run(['alembic', 'upgrade', 'head'], check=True)
        logger.info("Migraciones ejecutadas exitosamente")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar las migraciones: {str(e)}")
        sys.exit(1)

@cli.command()
def rollback():
    """Revertir la última migración"""
    try:
        subprocess.run(['alembic', 'downgrade', '-1'], check=True)
        logger.info("Migración revertida exitosamente")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al revertir la migración: {str(e)}")
        sys.exit(1)

@cli.command()
def backup():
    """Crear un backup de la base de datos"""
    try:
        db_parts = get_db_url_parts()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"backup_{db_parts['dbname']}_{timestamp}.sql"
        
        # Crear directorio de backups si no existe
        os.makedirs('backups', exist_ok=True)
        
        command = [
            'pg_dump',
            '-h', db_parts['host'],
            '-p', db_parts['port'],
            '-U', db_parts['user'],
            '-F', 'c',  # Formato custom
            '-b',  # Include large objects
            '-v',  # Verbose
            '-f', f"backups/{backup_file}",
            db_parts['dbname']
        ]
        
        subprocess.run(command, env={'PGPASSWORD': db_parts['password']}, check=True)
        logger.info(f"Backup creado exitosamente: {backup_file}")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al crear el backup: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('backup_file')
def restore(backup_file):
    """Restaurar un backup de la base de datos"""
    if click.confirm('¿Estás seguro de que quieres restaurar la base de datos? Los datos actuales serán reemplazados'):
        try:
            db_parts = get_db_url_parts()
            
            command = [
                'pg_restore',
                '-h', db_parts['host'],
                '-p', db_parts['port'],
                '-U', db_parts['user'],
                '-d', db_parts['dbname'],
                '-v',  # Verbose
                f"backups/{backup_file}"
            ]
            
            subprocess.run(command, env={'PGPASSWORD': db_parts['password']}, check=True)
            logger.info("Backup restaurado exitosamente")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error al restaurar el backup: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    cli()
