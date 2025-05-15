# -*- coding: utf-8 -*-
import os
import sys
import psycopg2
import logging
from pathlib import Path
from database.models import DATABASE_CONFIG, User
from sqlalchemy import create_engine, text
import bcrypt
import base64

# Configurar logging
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'diagnostic.log'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file,
    encoding='utf-8'
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
    try:
        # Conexión directa con psycopg2
        conn = psycopg2.connect(
            host=DATABASE_CONFIG['host'],
            database=DATABASE_CONFIG['database'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password']
        )
        
        cur = conn.cursor()
        
        # Verificar codificación
        cur.execute("SHOW server_encoding")
        server_encoding = cur.fetchone()[0]
        logger.info(f"Codificación del servidor: {server_encoding}")
        
        cur.execute("SHOW client_encoding")
        client_encoding = cur.fetchone()[0]
        logger.info(f"Codificación del cliente: {client_encoding}")
        
        # Verificar configuración de locale
        cur.execute("SHOW lc_collate")
        lc_collate = cur.fetchone()[0]
        logger.info(f"LC_COLLATE: {lc_collate}")
        
        cur.close()
        conn.close()
        logger.info("✅ Conexión a base de datos verificada")
        return True
    except Exception as e:
        logger.error(f"Error de conexión: {str(e)}")
        return False

def verify_admin_user():
    """Verificar usuario administrador"""
    try:
        # Crear conexión SQLAlchemy
        db_url = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
        engine = create_engine(db_url)
        
        # Verificar usuario admin
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM users WHERE username = 'admin'"))
            admin = result.fetchone()
            
            if admin:
                logger.info(f"Usuario admin encontrado (ID: {admin.id})")
                logger.info(f"Email: {admin.email}")
                logger.info(f"Activo: {admin.is_active}")
                
                # Verificar hash de contraseña
                try:
                    password = "12345678"
                    stored_hash = admin.password
                    
                    # Decodificar hash
                    hash_bytes = base64.b64decode(stored_hash)
                    
                    # Verificar contraseña
                    password_bytes = password.encode('utf-8')
                    if bcrypt.checkpw(password_bytes, hash_bytes):
                        logger.info("✅ Hash de contraseña verificado correctamente")
                    else:
                        logger.error("❌ La contraseña no coincide con el hash")
                        
                except Exception as e:
                    logger.error(f"Error verificando hash: {str(e)}")
            else:
                logger.error("❌ Usuario admin no encontrado")
                
        return True
    except Exception as e:
        logger.error(f"Error verificando usuario admin: {str(e)}")
        return False

def run_diagnostics():
    """Ejecutar diagnóstico completo"""
    print("🔍 Iniciando diagnóstico...")
    
    # Verificar entorno
    print("\nVerificando entorno...")
    check_environment()
    
    # Verificar base de datos
    print("\nVerificando conexión a base de datos...")
    if check_database_connection():
        print("✅ Conexión a base de datos correcta")
    else:
        print("❌ Error en conexión a base de datos")
    
    # Verificar usuario admin
    print("\nVerificando usuario administrador...")
    if verify_admin_user():
        print("✅ Usuario admin verificado")
    else:
        print("❌ Error verificando usuario admin")
    
    print("\n📋 Diagnóstico completado. Revise logs/diagnostic.log para más detalles.")

if __name__ == "__main__":
    run_diagnostics()
