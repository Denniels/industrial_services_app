#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from datetime import datetime
import psycopg2
from database.models import DATABASE_CONFIG

def create_backup():
    """Crear backup de la base de datos actual"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"backups/db_backup_{timestamp}.sql"
    
    # Asegurar que existe el directorio de backups
    os.makedirs('backups', exist_ok=True)
    
    # Crear backup usando pg_dump
    try:
        subprocess.run([
            'pg_dump',
            '-h', DATABASE_CONFIG['host'],
            '-U', DATABASE_CONFIG['user'],
            '-d', DATABASE_CONFIG['database'],
            '-f', backup_file,
            '-E', 'UTF8'
        ], check=True)
        print(f"‚úÖ Backup creado exitosamente: {backup_file}")
        return backup_file
    except subprocess.CalledProcessError as e:
        print(f"‚ùå Error al crear backup: {str(e)}")
        return None

def restore_backup(backup_file):
    """Restaurar backup espec√≠fico"""
    try:
        # Primero, cerrar todas las conexiones activas
        conn = psycopg2.connect(
            host=DATABASE_CONFIG['host'],
            database='postgres',  # conectar a base por defecto
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password']
        )
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Desconectar usuarios de la base de datos
        cur.execute(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{DATABASE_CONFIG['database']}'
            AND pid <> pg_backend_pid()
        """)
        
        # Eliminar y recrear la base de datos
        cur.execute(f"DROP DATABASE IF EXISTS {DATABASE_CONFIG['database']}")
        cur.execute(f"CREATE DATABASE {DATABASE_CONFIG['database']} WITH ENCODING 'UTF8'")
        
        cur.close()
        conn.close()
        
        # Restaurar el backup
        subprocess.run([
            'psql',
            '-h', DATABASE_CONFIG['host'],
            '-U', DATABASE_CONFIG['user'],
            '-d', DATABASE_CONFIG['database'],
            '-f', backup_file
        ], check=True)
        
        print(f"‚úÖ Base de datos restaurada desde: {backup_file}")
        return True
    except Exception as e:
        print(f"‚ùå Error al restaurar backup: {str(e)}")
        return False

def rollback_encoding():
    """Procedimiento completo de rollback"""
    print("üîÑ Iniciando procedimiento de rollback...")
    
    # 1. Crear backup de seguridad
    backup_file = create_backup()
    if not backup_file:
        print("‚ùå No se pudo crear backup de seguridad. Abortando rollback.")
        return False
    
    # 2. Restaurar √∫ltima configuraci√≥n conocida
    try:
        # Restaurar configuraci√≥n anterior de DATABASE_CONFIG
        with open('database/config.py.bak', 'r', encoding='utf-8') as f:
            with open('database/config.py', 'w', encoding='utf-8') as f_out:
                f_out.write(f.read())
        print("‚úÖ Configuraci√≥n anterior restaurada")
        
        # 3. Restaurar el backup
        if restore_backup(backup_file):
            print("‚úÖ Rollback completado exitosamente")
            return True
        else:
            print("‚ùå Error durante la restauraci√≥n del backup")
            return False
            
    except Exception as e:
        print(f"‚ùå Error durante el rollback: {str(e)}")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--rollback':
        rollback_encoding()
    else:
        print("Uso: python rollback_encoding.py --rollback")
