# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float, Text, Enum, Boolean, JSON, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum
import os

DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'integral_service_db',
    'user': 'postgres',
    'password': 'DAms15820',
    'port': '5432',
    'client_encoding': 'utf8',
    'options': '-c client_encoding=utf8'
}

def init_database():
    """Inicializa la conexión a la base de datos y crea las tablas si no existen"""
    try:
        # Crear URL de conexión con parámetros de codificación
        db_url = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
        
        # Crear el motor de la base de datos con configuración UTF-8
        engine = create_engine(
            db_url, 
            echo=False,
            connect_args={
                'client_encoding': 'utf8',
                'options': '-c search_path=public -c client_encoding=utf8'
            }
        )
        
        # Crear todas las tablas definidas
        Base.metadata.create_all(engine)
        
        # Crear y devolver la sesión
        Session = sessionmaker(bind=engine)
        return Session()
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")
        raise

Base = declarative_base()

class UserRole(enum.Enum):
    ADMIN = "admin"
    TECHNICIAN = "technician"
    CLIENT = "client"
    SUPERVISOR = "supervisor"

class ServiceType(enum.Enum):
    AUTOMATION = "Automatización"
    REFRIGERATION = "Refrigeración"
    ELECTROMECHANICAL = "Electromecánica"
    PNEUMATIC = "Neumática"
    HYDRAULIC = "Hidráulica"

class ServiceStatus(enum.Enum):
    PENDING = "Pendiente"
    SCHEDULED = "Programado"
    IN_PROGRESS = "En Proceso"
    COMPLETED = "Completado"
    CANCELLED = "Cancelado"

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
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    users = relationship('User', back_populates='company')

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    is_active = Column(Boolean, default=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    company = relationship('Company', back_populates='users')
    devices = relationship('MonitoringDevice', back_populates='client', cascade='all, delete-orphan')
    devices = relationship('MonitoringDevice', back_populates='client')

class Equipment(Base):
    __tablename__ = 'equipment'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    model = Column(String(50))
    serial_number = Column(String(50))
    manufacturer = Column(String(50))
    installation_date = Column(DateTime)
    last_maintenance = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class ServiceRequest(Base):
    __tablename__ = 'service_requests'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    assigned_technician_id = Column(Integer, ForeignKey('users.id'))
    equipment_id = Column(Integer, ForeignKey('equipment.id'))
    service_type = Column(Enum(ServiceType), nullable=False)
    description = Column(Text)
    status = Column(Enum(ServiceStatus), default=ServiceStatus.PENDING)
    priority = Column(Integer, default=3)
    requested_date = Column(DateTime, default=datetime.utcnow)
    scheduled_date = Column(DateTime)
    completion_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class MonitoringDevice(Base):
    __tablename__ = 'monitoring_devices'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    device_serial = Column(String(50), unique=True, nullable=False)
    device_type = Column(String(50))
    variables_count = Column(Integer, default=0)
    max_variables = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)
    last_connection = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    client = relationship('User', back_populates='devices')
    variables = relationship('MonitoredVariable', back_populates='device', cascade='all, delete-orphan')

class MonitoredVariable(Base):
    __tablename__ = 'monitored_variables'
    
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('monitoring_devices.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    unit = Column(String(20))
    min_value = Column(Float)
    max_value = Column(Float)
    alert_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    device = relationship('MonitoringDevice', back_populates='variables')
    readings = relationship('VariableReading', back_populates='variable', cascade='all, delete-orphan')

class VariableReading(Base):
    __tablename__ = 'variable_readings'
    
    id = Column(Integer, primary_key=True)
    variable_id = Column(Integer, ForeignKey('monitored_variables.id'), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    quality = Column(Integer)  # Calidad de la lectura (0-100)
    
    variable = relationship('MonitoredVariable', back_populates='readings')

# Configuración de las relaciones bidireccionales después de definir todas las clases
User.submitted_requests = relationship('ServiceRequest', 
                                    foreign_keys=[ServiceRequest.client_id],
                                    primaryjoin='ServiceRequest.client_id == User.id',
                                    backref='client')

User.assigned_services = relationship('ServiceRequest',
                                    foreign_keys=[ServiceRequest.assigned_technician_id],
                                    primaryjoin='ServiceRequest.assigned_technician_id == User.id',
                                    backref='technician')

Equipment.service_requests = relationship('ServiceRequest', backref='equipment')
