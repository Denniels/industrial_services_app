# -*- coding: ascii -*-
from datetime import datetime
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import (
    Base, Company, User, UserRole, ServiceType,
    ContractType, ServicePricing, ContractPricing
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_data():
    try:
        engine = create_engine('postgresql://postgres:admin@localhost:5432/integral_service_db')
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Crear empresa interna
        company = Company(
            name="Integral Service SPA",
            rut="76.512.925-7",
            address="Bulnes 368, of 802",
            city="Temuco",
            region="La Araucania",
            phone="+56 9 6366 9300",
            email="contacto@integralservice.cl",
            is_internal=True,
            created_at=datetime.utcnow()
        )
        session.add(company)
        session.flush()
        
        # Crear usuario administrador
        admin_user = User(
            company_id=company.id,
            username="admin",
            email="admin@integralservice.cl",
            password_hash=bcrypt.hashpw("DAms15820".encode('ascii'), bcrypt.gensalt()).decode('ascii'),
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
                hourly_rate=45000.0,
                travel_cost=15000.0,
                min_service_cost=30000.0,
                emergency_multiplier=1.5
            )
            session.add(pricing)
        
        # Configurar precios de contratos
        for contract_type in ContractType:
            if contract_type != ContractType.NONE:
                for service_type in ServiceType:
                    contract_pricing = ContractPricing(
                        contract_type=contract_type,
                        service_type=service_type,
                        discount_percentage=0.10,
                        min_monthly_services=1,
                        response_time_hours=24
                    )
                    session.add(contract_pricing)
        
        session.commit()
        logger.info("Datos iniciales creados exitosamente")
        return True
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error: {str(e)}")
        return False
    finally:
        session.close()

if __name__ == "__main__":
    init_data()
