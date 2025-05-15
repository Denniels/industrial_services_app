"""
Script para realizar copias de seguridad automatizadas de la base de datos
y mantener un historial de respaldos.
"""

import os
import sys
import subprocess
import logging
from datetime import datetime
import shutil
import psycopg2
from config import DATABASE_URL

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/backup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabaseBackup:
    def __init__(self):
        self.backup_dir = 'backups'
        self.max_backups = 30  # Mantener m√°ximo 30 backups
        
        # Crear directorio de backups si no existe
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def create_backup(self):
        """Crear una nueva copia de seguridad."""
        try:
            # Generar nombre del archivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(self.backup_dir, f'backup_{timestamp}.sql')
            
            # Ejecutar pg_dump
            cmd = f'pg_dump "{DATABASE_URL}" > "{backup_file}"'
            subprocess.run(cmd, shell=True, check=True)
            
            logger.info(f"‚úÖ Backup creado exitosamente: {backup_file}")
            return backup_file
        
        except subprocess.CalledProcessError as e:
            logger.error(f"‚ùå Error al crear backup: {str(e)}")
            return None

    def compress_backup(self, backup_file):
        """Comprimir el archivo de backup."""
        try:
            compressed_file = f"{backup_file}.gz"
            subprocess.run(['gzip', '-f', backup_file])
            logger.info(f"‚úÖ Backup comprimido: {compressed_file}")
            return compressed_file
        
        except Exception as e:
            logger.error(f"‚ùå Error al comprimir backup: {str(e)}")
            return None

    def clean_old_backups(self):
        """Eliminar backups antiguos manteniendo solo los √∫ltimos N."""
        try:
            # Listar todos los backups
            backups = []
            for file in os.listdir(self.backup_dir):
                if file.startswith('backup_') and (file.endswith('.sql') or file.endswith('.sql.gz')):
                    full_path = os.path.join(self.backup_dir, file)
                    backups.append((full_path, os.path.getmtime(full_path)))
            
            # Ordenar por fecha de modificaci√≥n
            backups.sort(key=lambda x: x[1], reverse=True)
            
            # Eliminar backups antiguos
            for backup_path, _ in backups[self.max_backups:]:
                os.remove(backup_path)
                logger.info(f"üóëÔ∏è Backup antiguo eliminado: {backup_path}")
        
        except Exception as e:
            logger.error(f"‚ùå Error al limpiar backups antiguos: {str(e)}")

    def verify_backup(self, backup_file):
        """Verificar la integridad del backup."""
        try:
            # Crear una base de datos temporal para pruebas
            test_db_name = "backup_test_db"
            conn = psycopg2.connect(DATABASE_URL)
            conn.autocommit = True
            
            with conn.cursor() as cur:
                # Eliminar DB de prueba si existe
                cur.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
                # Crear DB de prueba
                cur.execute(f"CREATE DATABASE {test_db_name}")
            
            # Restaurar backup en la DB de prueba
            test_db_url = DATABASE_URL.replace(conn.dbname, test_db_name)
            cmd = f'psql "{test_db_url}" < "{backup_file}"'
            subprocess.run(cmd, shell=True, check=True)
            
            logger.info(f"‚úÖ Backup verificado exitosamente")
            
            # Limpiar
            with conn.cursor() as cur:
                cur.execute(f"DROP DATABASE {test_db_name}")
            
            return True
        
        except Exception as e:
            logger.error(f"‚ùå Error al verificar backup: {str(e)}")
            return False

    def run_backup(self):
        """Ejecutar el proceso completo de backup."""
        logger.info("üöÄ Iniciando proceso de backup...")
        
        # Crear backup
        backup_file = self.create_backup()
        if not backup_file:
            return False
        
        # Verificar backup
        if not self.verify_backup(backup_file):
            logger.error("‚ùå Backup verification failed")
            return False
        
        # Comprimir backup
        compressed_file = self.compress_backup(backup_file)
        if not compressed_file:
            return False
        
        # Limpiar backups antiguos
        self.clean_old_backups()
        
        logger.info("‚úÖ Proceso de backup completado exitosamente")
        return True

if __name__ == "__main__":
    backup = DatabaseBackup()
    if backup.run_backup():
        sys.exit(0)
    else:
        sys.exit(1)
