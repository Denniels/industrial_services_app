# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path de Python
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from database.models import Base, User, UserRole
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_tables():
    """Inicializar las tablas de la base de datos"""
    try:
        # Crear conexión
        engine = create_engine(
            'postgresql://postgres:DAms15820@localhost:5432/integral_service_db',
            echo=True
        )
        
        # Crear todas las tablas
        Base.metadata.drop_all(engine)  # Eliminar tablas existentes
        Base.metadata.create_all(engine)
        
        logger.info("✅ Tablas creadas exitosamente")
        return engine
        
    except Exception as e:
        logger.error(f"❌ Error al crear las tablas: {str(e)}")
        raise

def create_admin_user(engine):
    """Crear usuario administrador inicial"""
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Crear usuario administrador
        admin = User(
            username="admin",
            email="admin@integralservice.cl",
            password=generate_password_hash("admin"),
            role=UserRole.ADMIN,
            first_name="Administrador",
            last_name="Sistema",
            is_active=True,
            first_login=True,
            created_at=datetime.utcnow()
        )
        
        session.add(admin)
        session.commit()
        logger.info("✅ Usuario administrador creado exitosamente")
        logger.info("Usuario: admin")
        logger.info("Contraseña: admin")
        
    except Exception as e:
        session.rollback()
        logger.error(f"❌ Error al crear el usuario administrador: {str(e)}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    engine = init_tables()
    create_admin_user(engine)
