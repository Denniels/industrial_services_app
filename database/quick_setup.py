#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import bcrypt
import base64
from database.models import init_database, User, UserRole, Company
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def hash_password(password: str) -> str:
    """Genera un hash seguro de la contrase√±a"""
    try:
        # Convertir la contrase√±a a bytes
        password_bytes = password.encode('utf-8')
        # Generar salt y hash
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        # Codificar en base64 para almacenamiento
        encoded = base64.b64encode(hashed).decode('ascii')
        logger.debug(f"Hash generado exitosamente, longitud: {len(encoded)}")
        return encoded
    except Exception as e:
        logger.error(f"Error al generar hash: {str(e)}")
        raise

def setup_admin(force=True):
    """Configurar usuario administrador inicial"""
    session = init_database()
    
    try:
        # Crear compa√±√≠a Integral Service si no existe
        company = session.query(Company).filter_by(name="Integral Service SPA").first()
        if not company:
            company = Company(
                name="Integral Service SPA",
                rut="76.123.456-7",
                address="Av. Industrial 1234",
                city="Santiago",
                region="Metropolitana",
                is_internal=True
            )
            session.add(company)
            session.commit()
            logger.info("‚úÖ Compa√±√≠a creada")
        
        # Si force es True, eliminar usuario admin existente
        if force:
            admin = session.query(User).filter_by(username="admin").first()
            if admin:
                session.delete(admin)
                session.commit()
                logger.info("Usuario admin existente eliminado")
        
        # Crear nuevo usuario admin
        password_hash = hash_password("12345678")
        admin = User(
            username="admin",
            email="admin@integralservice.cl",
            password=password_hash,
            role=UserRole.ADMIN,
            first_name="Administrador",
            last_name="Sistema",
            company_id=company.id,
            is_active=True,
            first_login=False
        )
        session.add(admin)
        session.commit()
        logger.info("‚úÖ Usuario administrador creado exitosamente")
            
    except Exception as e:
        logger.error(f"‚ùå Error durante la configuraci√≥n: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    print("üîÑ Configurando entorno inicial...")
    try:
        setup_admin(force=True)
        print("\n‚úÖ Configuraci√≥n completada. Puede iniciar sesi√≥n con:")
        print("Usuario: admin")
        print("Contrase√±a: 12345678")
    except Exception as e:
        print(f"‚ùå Error durante la configuraci√≥n: {str(e)}")
        sys.exit(1)
