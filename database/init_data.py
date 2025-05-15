# -*- coding: utf-8 -*-
import sys
import os
import logging
from datetime import datetime
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import codecs

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
    try:
        # Crear conexión a la base de datos con codificación UTF-8
        engine = create_engine(
            'postgresql://postgres:DAms15820@localhost:5432/integral_service_db',
            connect_args={'client_encoding': 'utf8'}
        )
        Session = sessionmaker(bind=engine)
        session = Session()        # Verificar si la empresa ya existe
        company = session.query(Company).filter_by(rut="76.512.925-7").first()
        if not company:
            # Crear empresa interna
            company = Company(
                name="Integral Service SPA",
                rut="76.512.925-7",
                address="Bulnes 368, of 802",
                city="Temuco",
                region="La Araucania",
                phone="+56 9 6366 9300",
                email="contacto@integralservicespa.cl",
                is_internal=True,
                created_at=datetime.utcnow()
            )
            session.add(company)
            session.flush()
            logger.info("✅ Empresa interna creada")
        else:
            logger.info("ℹ️ La empresa interna ya existe")
          # Verificar si el usuario admin ya existe
        admin_exists = session.query(User).filter_by(username="admin").first()
        if not admin_exists:
            # Crear usuario administrador
            password_hash = bcrypt.hashpw(
                "DAms15820".encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
            
            admin_user = User(
                company_id=company.id,
                username="admin",
                email="contacto@integralservicespa.cl",
                password=password_hash,
                role=UserRole.ADMIN,
                first_name="Administrador",
                last_name="Sistema",
                is_active=True,
                created_at=datetime.utcnow()
            )
            session.add(admin_user)
            logger.info("✅ Usuario administrador creado")
        else:
            logger.info("ℹ️ El usuario administrador ya existe")
          # Verificar y configurar precios de servicios
        for service_type in ServiceType:
            existing_pricing = session.query(ServicePricing).filter_by(service_type=service_type).first()
            if not existing_pricing:
                pricing = ServicePricing(
                    service_type=service_type,
                    hourly_rate=45000.0,
                    travel_cost=15000.0,
                    min_service_cost=30000.0,
                    emergency_multiplier=1.5
                )
                session.add(pricing)
                logger.info(f"✅ Precio creado para servicio: {service_type.value}")
            else:
                logger.info(f"ℹ️ Ya existe precio para servicio: {service_type.value}")
        
        # Verificar y configurar precios de contratos
        for contract_type in ContractType:
            if contract_type != ContractType.NONE:
                for service_type in ServiceType:
                    existing_pricing = session.query(ContractPricing).filter_by(
                        contract_type=contract_type,
                        service_type=service_type
                    ).first()
                    
                    if not existing_pricing:
                        contract_pricing = ContractPricing(
                            contract_type=contract_type,
                            service_type=service_type,
                            discount_percentage=0.10,
                            min_monthly_services=1,
                            response_time_hours=24
                        )
                        session.add(contract_pricing)
                        logger.info(f"✅ Precio creado para contrato: {contract_type.value} - {service_type.value}")
                    else:
                        logger.info(f"ℹ️ Ya existe precio para contrato: {contract_type.value} - {service_type.value}")
        
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
