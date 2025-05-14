# -*- coding: utf-8 -*-
import sys
import os
import logging
from datetime import datetime
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Agregar el directorio raíz al path de Python
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

from database.models import (
    Base, Company, User, UserRole, ServiceType,
    ContractType, ServicePricing, ContractPricing
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_data():
    """Inicializar datos básicos en la base de datos"""
    # Crear conexión a la base de datos
    engine = create_engine('postgresql://postgres:admin@localhost:5432/integral_service_db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Crear empresa interna
        company = Company(
            name="Integral Service SPA",
            rut="76.512.925-7",
            address="Bulnes 368, of 802",
            city="Temuco",
            region="La Araucanía",
            phone="+56 9 6366 9300",
            email="contacto@integralservice.cl",
            is_internal=True,
            created_at=datetime.utcnow()
        )
        session.add(company)
        session.flush()
        
        # Crear usuario administrador
        password = "DAms15820"
        password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        
        admin_user = User(
            company_id=company.id,
            username="admin",
            email="admin@integralservice.cl",
            password_hash=password_hash,
            role=UserRole.ADMIN,
            first_name="Administrador",
            last_name="Sistema",
            is_active=True,
            created_at=datetime.utcnow()
        )
        session.add(admin_user)
        
        # Configurar precios de servicios
        for service_type in ServiceType:
            pricing = ServicePricing(
                service_type=service_type,
                hourly_rate=45000.0,  # $45,000 por hora
                travel_cost=15000.0,  # $15,000 por visita
                min_service_cost=30000.0,  # Mínimo $30,000
                emergency_multiplier=1.5  # 50% adicional por emergencias
            )
            session.add(pricing)
        
        # Configurar precios de contratos
        for contract_type in ContractType:
            if contract_type != ContractType.NONE:
                for service_type in ServiceType:
                    contract_pricing = ContractPricing(
                        contract_type=contract_type,
                        service_type=service_type,
                        discount_percentage=0.10,  # 10% de descuento
                        min_monthly_services=1,
                        response_time_hours=24
                    )
                    session.add(contract_pricing)
        
        session.commit()
        logger.info("✅ Datos iniciales creados exitosamente")
        return True
        
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"❌ Error al inicializar datos: {str(e)}")
        return False
    finally:
        session.close()

if __name__ == "__main__":
    initialize_data()
