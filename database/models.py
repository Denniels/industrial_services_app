# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float, Text, Enum, Boolean, JSON, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    ADMIN = "admin"
    TECHNICIAN = "technician"
    CLIENT = "client"
    SUPERVISOR = "supervisor"

class ServiceType(enum.Enum):
    AUTOMATION = "Automatización"
    REFRIGERATION = "Refrigeración"
    ELECTROMECHANICAL = "Electromecánica Industrial"
    PNEUMATIC = "Neumática"
    HYDRAULIC = "Hidráulica"

class ServiceStatus(enum.Enum):
    PENDING = "Pendiente"
    SCHEDULED = "Programado"
    IN_PROGRESS = "En Proceso"
    COMPLETED = "Completado"
    CANCELLED = "Cancelado"

class ContractType(enum.Enum):
    NONE = "Sin Contrato"
    BASIC = "Contrato Básico"
    PREMIUM = "Contrato Premium"
    CUSTOM = "Contrato Personalizado"

class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    rut = Column(String(20), unique=True, nullable=False)
    address = Column(String(200))
    city = Column(String(50))
    region = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100))
    is_internal = Column(Boolean, default=False)  # True para Integral Service SPA
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    company = relationship('Company')

class Technician(Base):
    __tablename__ = 'technicians'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    specialty = Column(ARRAY(String))  # Lista de especialidades
    certification = Column(ARRAY(String))  # Lista de certificaciones
    position = Column(String(100))  # Cargo específico
    experience_years = Column(Integer)
    available = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User')

class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    contract_type = Column(Enum(ContractType), default=ContractType.NONE)
    contract_start_date = Column(DateTime)
    contract_end_date = Column(DateTime)
    payment_terms = Column(String(100))
    credit_limit = Column(Float)
    special_conditions = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    user = relationship('User')
    company = relationship('Company')

class EquipmentType(Base):
    __tablename__ = 'equipment_types'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))  # Refrigeración, Electromecánico, etc.
    description = Column(Text)
    technical_specs = Column(JSON)  # Especificaciones técnicas configurables
    required_measurements = Column(ARRAY(String))  # Mediciones requeridas
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

class Equipment(Base):
    __tablename__ = 'equipment'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    equipment_type_id = Column(Integer, ForeignKey('equipment_types.id'))
    name = Column(String(100), nullable=False)
    model = Column(String(100))
    serial_number = Column(String(100))
    manufacturer = Column(String(100))
    
    # Datos técnicos
    technical_specs = Column(JSON)  # Almacena datos de placa y especificaciones
    power_specs = Column(JSON)  # Especificaciones de potencia
    electrical_specs = Column(JSON)  # Datos eléctricos
    pneumatic_specs = Column(JSON)  # Datos neumáticos
    hydraulic_specs = Column(JSON)  # Datos hidráulicos
    
    installation_date = Column(DateTime)
    last_maintenance_date = Column(DateTime)
    maintenance_frequency = Column(Integer)  # en días
    location = Column(String(200))
    status = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    client = relationship('Client')
    equipment_type = relationship('EquipmentType')
    maintenance_history = relationship('Maintenance', back_populates='equipment')

class ServiceRequest(Base):
    __tablename__ = 'service_requests'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    equipment_id = Column(Integer, ForeignKey('equipment.id'))
    service_type = Column(Enum(ServiceType), nullable=False)
    is_contract_service = Column(Boolean, default=False)
    priority = Column(String(20))
    description = Column(Text)
    status = Column(Enum(ServiceStatus), default=ServiceStatus.PENDING)
    requested_date = Column(DateTime, nullable=False)
    scheduled_date = Column(DateTime)
    completion_date = Column(DateTime)
    technician_id = Column(Integer, ForeignKey('technicians.id'))
    supervisor_id = Column(Integer, ForeignKey('users.id'))
    estimated_hours = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    client = relationship('Client')
    equipment = relationship('Equipment')
    technician = relationship('Technician')
    supervisor = relationship('User', foreign_keys=[supervisor_id])
    technical_report = relationship('TechnicalReport', back_populates='service_request')

class TechnicalReport(Base):
    __tablename__ = 'technical_reports'
    
    id = Column(Integer, primary_key=True)
    service_request_id = Column(Integer, ForeignKey('service_requests.id'))
    technician_id = Column(Integer, ForeignKey('technicians.id'))
    
    # Diagnóstico y trabajo
    diagnosis = Column(Text)
    work_performed = Column(Text)
    maintenance_type = Column(String(50))  # Preventivo/Correctivo
    recommendations = Column(Text)
    
    # Equipos y materiales
    equipment_state = Column(String(50))
    materials_used = Column(Text)
    replacement_parts = Column(Text)
    spare_parts_used = Column(Text)
    
    # Tiempos y costos
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    hours_worked = Column(Float)
    travel_time = Column(Float)
    total_cost = Column(Float)
    
    # Seguimiento
    next_maintenance_date = Column(DateTime)
    requires_followup = Column(Boolean, default=False)
    followup_notes = Column(Text)
    
    # Evidencia y aprobación
    photos = Column(Text)  # URLs separadas por comas
    signature_client = Column(Text)
    signature_technician = Column(Text)
    approved_by_client = Column(Boolean, default=False)
    approved_by_supervisor = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    service_request = relationship('ServiceRequest', back_populates='technical_report')
    technician = relationship('Technician')
    materials = relationship('MaterialUsage', back_populates='technical_report')

class Material(Base):
    __tablename__ = 'materials'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    unit = Column(String(20))  # unidad de medida
    unit_price = Column(Float)
    stock = Column(Float)
    minimum_stock = Column(Float)
    supplier = Column(String(100))
    location = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    usages = relationship('MaterialUsage', back_populates='material')

class MaterialUsage(Base):
    __tablename__ = 'material_usage'
    
    id = Column(Integer, primary_key=True)
    technical_report_id = Column(Integer, ForeignKey('technical_reports.id'))
    material_id = Column(Integer, ForeignKey('materials.id'))
    quantity = Column(Float)
    unit_price = Column(Float)
    total_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    technical_report = relationship('TechnicalReport', back_populates='materials')
    material = relationship('Material', back_populates='usages')

class Invoice(Base):
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    service_request_id = Column(Integer, ForeignKey('service_requests.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    invoice_number = Column(String(20), unique=True)
    issue_date = Column(DateTime)
    due_date = Column(DateTime)
    subtotal = Column(Float)
    tax = Column(Float)
    total = Column(Float)
    status = Column(String(20), default='PENDING')  # PENDING, PAID, OVERDUE
    payment_date = Column(DateTime)
    payment_method = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    service_request = relationship('ServiceRequest')
    client = relationship('Client')

class Maintenance(Base):
    __tablename__ = 'maintenance_schedule'
    
    id = Column(Integer, primary_key=True)
    equipment_id = Column(Integer, ForeignKey('equipment.id'))
    scheduled_date = Column(DateTime)
    maintenance_type = Column(String(50))
    description = Column(Text)
    status = Column(String(20))
    technician_id = Column(Integer, ForeignKey('technicians.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    equipment = relationship('Equipment', back_populates='maintenance_history')
    technician = relationship('Technician')

class RepairParts(Base):
    __tablename__ = 'repair_parts'
    
    id = Column(Integer, primary_key=True)
    technical_report_id = Column(Integer, ForeignKey('technical_reports.id'))
    name = Column(String(100))
    description = Column(Text)
    quantity = Column(Float)
    unit = Column(String(20))
    unit_price = Column(Float)
    supplier = Column(String(100))
    purchase_date = Column(DateTime)
    arrival_date = Column(DateTime)
    is_client_supplied = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    technical_report = relationship('TechnicalReport')

class ServicePricing(Base):
    __tablename__ = 'service_pricing'
    
    id = Column(Integer, primary_key=True)
    service_type = Column(Enum(ServiceType), nullable=False)
    hourly_rate = Column(Float, nullable=False)
    travel_cost = Column(Float)
    min_service_cost = Column(Float)
    emergency_multiplier = Column(Float, default=1.5)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class ContractPricing(Base):
    __tablename__ = 'contract_pricing'
    
    id = Column(Integer, primary_key=True)
    contract_type = Column(Enum(ContractType), nullable=False)
    service_type = Column(Enum(ServiceType), nullable=False)
    discount_percentage = Column(Float)
    min_monthly_services = Column(Integer)
    response_time_hours = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class Budget(Base):
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True)
    service_request_id = Column(Integer, ForeignKey('service_requests.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    pricing_id = Column(Integer, ForeignKey('service_pricing.id'))
    
    # Costos y tiempos
    estimated_hours = Column(Float)
    hourly_rate = Column(Float)
    parts_cost = Column(Float)
    operational_cost = Column(Float)
    travel_cost = Column(Float)
    discount = Column(Float, default=0)
    
    # Totales
    subtotal = Column(Float)
    tax = Column(Float)
    total = Column(Float)
    
    status = Column(String(20))  # DRAFT, SENT, APPROVED, REJECTED
    valid_until = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime)
    
    service_request = relationship('ServiceRequest')
    client = relationship('Client')
    pricing = relationship('ServicePricing')
