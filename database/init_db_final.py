# -*- coding: utf-8 -*-
import os
import psycopg2
import logging
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from database.models import DATABASE_CONFIG, Base, User, Company, UserRole
from database.quick_setup import setup_admin
import bcrypt
import base64

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(nivel)s - %(mensaje)s',
    filename='logs/db_init.log',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

def get_database_url():
    """Obtener URL de conexión a la base de datos"""
    return f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@" \
           f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}" \
           f"?client_encoding=utf8"

def init_database():
    """Inicializar la base de datos desde cero"""
    try:
        # Conectar a postgres para poder crear/eliminar la base de datos
        conn = psycopg2.connect(
            host=DATABASE_CONFIG['host'],
            database='postgres',
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password']
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Cerrar conexiones existentes
        cur.execute(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{DATABASE_CONFIG['database']}'
            AND pid <> pg_backend_pid()
        """)
        
        # Eliminar base de datos si existe
        cur.execute(f"DROP DATABASE IF EXISTS {DATABASE_CONFIG['database']}")
        logger.info("Base de datos eliminada si existía")
        
        # Crear nueva base de datos con UTF-8
        cur.execute(f"""
            CREATE DATABASE {DATABASE_CONFIG['database']}
            WITH ENCODING 'UTF8'
            LC_COLLATE = 'Spanish_Spain.1252'
            LC_CTYPE = 'Spanish_Spain.1252'
            TEMPLATE template0
        """)
        logger.info("Base de datos creada con codificación UTF-8")
        
        # Cerrar conexión a postgres
        cur.close()
        conn.close()
        
        # Crear el motor SQLAlchemy
        engine = create_engine(
            get_database_url(),
            echo=False,
            connect_args={'options': DATABASE_CONFIG['options']}
        )
        
        # Crear todas las tablas
        Base.metadata.create_all(engine)
        logger.info("Tablas creadas exitosamente")
        
        # Crear sesión
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try:
            # Crear la compañía principal
            company = Company(
                name="Integral Service SPA",
                rut="76.123.456-7",
                address="Dirección Principal 123",
                city="Ciudad",
                region="Región",
                phone="+56 9 1234 5678",
                email="contacto@integralservice.cl"
            )
            session.add(company)
            session.commit()
            
            # Crear usuario administrador
            admin = User(
                username="admin",
                email="admin@integralservice.cl",
                role=UserRole.ADMIN,
                is_active=True,
                company_id=company.id,
                first_name="Administrador",
                last_name="Sistema"
            )
            
            # Generar hash de la contraseña
            password = "12345678"
            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_bytes, salt)
            admin.password = base64.b64encode(hashed).decode('ascii')
            
            session.add(admin)
            session.commit()
            logger.info("Usuario administrador creado exitosamente")
            
            return True
            
        except Exception as e:
            logger.error(f"Error al crear datos iniciales: {str(e)}")
            session.rollback()
            raise
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error durante la inicialización: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔄 Iniciando configuración de base de datos...")
    if init_database():
        print("✅ Base de datos inicializada exitosamente!")
        print("\nCredenciales de administrador:")
        print("Usuario: admin")
        print("Contraseña: 12345678")
    else:
        print("❌ Error durante la inicialización")
