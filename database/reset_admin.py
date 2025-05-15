# -*- coding: utf-8 -*-
import bcrypt
import base64
from database.models import init_database, User, Company, UserRole
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def reset_admin():
    """Reiniciar usuario administrador con configuraci√≥n limpia"""
    session = init_database()
    try:
        # 1. Eliminar usuario admin existente
        admin = session.query(User).filter_by(username="admin").first()
        if admin:
            session.delete(admin)
            session.commit()
            logger.info("Usuario admin existente eliminado")
        
        # 2. Verificar/crear compa√±√≠a
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
            logger.info("Compa√±√≠a creada")
        
        # 3. Crear hash de contrase√±a
        password = "12345678"
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        password_hash = base64.b64encode(hashed).decode('ascii')
        
        # 4. Crear nuevo usuario admin
        new_admin = User(
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
        
        session.add(new_admin)
        session.commit()
        
        # 5. Verificar el hash
        admin = session.query(User).filter_by(username="admin").first()
        decoded_hash = base64.b64decode(admin.password)
        verify_result = bcrypt.checkpw(password_bytes, decoded_hash)
        
        if verify_result:
            logger.info("‚úÖ Usuario admin creado y verificado correctamente")
            logger.info(f"Hash length: {len(admin.password)}")
            logger.info(f"Decoded hash length: {len(decoded_hash)}")
        else:
            logger.error("‚ùå Error en la verificaci√≥n de contrase√±a")
            
    except Exception as e:
        logger.error(f"Error durante el reset: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    print("üîÑ Reiniciando usuario administrador...")
    reset_admin()
    print("‚úÖ Proceso completado. Use las siguientes credenciales:")
    print("Usuario: admin")
    print("Contrase√±a: 12345678")