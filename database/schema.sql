-- Schema for integral_service_db
-- Crear tipos ENUM
CREATE TYPE user_role AS ENUM ('admin', 'technician', 'client', 'supervisor');
CREATE TYPE service_type AS ENUM ('Automatizacion', 'Refrigeracion', 'Electromecanica Industrial', 'Neumatica', 'Hidraulica');
CREATE TYPE service_status AS ENUM ('Pendiente', 'Programado', 'En Proceso', 'Completado', 'Cancelado');
CREATE TYPE contract_type AS ENUM ('Sin Contrato', 'Contrato Basico', 'Contrato Premium', 'Contrato Personalizado');ear tipos ENUM
CREATE TYPE user_role AS ENUM ('admin', 'technician', 'client', 'supervisor');
CREATE TYPE service_type AS ENUM ('Automatizacion', 'Refrigeracion', 'Electromecanica Industrial', 'Neumatica', 'Hidraulica');
CREATE TYPE service_status AS ENUM ('Pendiente', 'Programado', 'En Proceso', 'Completado', 'Cancelado');
CREATE TYPE contract_type AS ENUM ('Sin Contrato', 'Contrato Basico', 'Contrato Premium', 'Contrato Personalizado');

-- Tabla de Empresas
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    rut VARCHAR(20) UNIQUE NOT NULL,
    address VARCHAR(200),
    city VARCHAR(50),
    region VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100),
    is_internal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Tabla de Usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    role user_role NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Tabla de Técnicos
CREATE TABLE technicians (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id),
    specialty VARCHAR[],
    certification VARCHAR[],
    position VARCHAR(100),
    experience_years INTEGER,
    available BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Clientes
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    company_id INTEGER REFERENCES companies(id),
    contract_type contract_type DEFAULT 'Sin Contrato',
    contract_start_date TIMESTAMP,
    contract_end_date TIMESTAMP,
    payment_terms VARCHAR(100),
    credit_limit FLOAT,
    special_conditions TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Tabla de Tipos de Equipo
CREATE TABLE equipment_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    description TEXT,
    technical_specs JSONB,
    required_measurements VARCHAR[],
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Equipos
CREATE TABLE equipment (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    equipment_type_id INTEGER REFERENCES equipment_types(id),
    name VARCHAR(100) NOT NULL,
    model VARCHAR(100),
    serial_number VARCHAR(100),
    manufacturer VARCHAR(100),
    technical_specs JSONB,
    power_specs JSONB,
    electrical_specs JSONB,
    pneumatic_specs JSONB,
    hydraulic_specs JSONB,
    installation_date TIMESTAMP,
    last_maintenance_date TIMESTAMP,
    maintenance_frequency INTEGER,
    location VARCHAR(200),
    status VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Solicitudes de Servicio
CREATE TABLE service_requests (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    equipment_id INTEGER REFERENCES equipment(id),
    service_type service_type NOT NULL,
    is_contract_service BOOLEAN DEFAULT FALSE,
    priority VARCHAR(20),
    description TEXT,
    status service_status DEFAULT 'Pendiente',
    requested_date TIMESTAMP NOT NULL,
    scheduled_date TIMESTAMP,
    completion_date TIMESTAMP,
    technician_id INTEGER REFERENCES technicians(id),
    supervisor_id INTEGER REFERENCES users(id),
    estimated_hours FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Reportes Técnicos
CREATE TABLE technical_reports (
    id SERIAL PRIMARY KEY,
    service_request_id INTEGER REFERENCES service_requests(id),
    technician_id INTEGER REFERENCES technicians(id),
    diagnosis TEXT,
    work_performed TEXT,
    maintenance_type VARCHAR(50),
    recommendations TEXT,
    equipment_state VARCHAR(50),
    materials_used TEXT,
    replacement_parts TEXT,
    spare_parts_used TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    hours_worked FLOAT,
    travel_time FLOAT,
    total_cost FLOAT,
    next_maintenance_date TIMESTAMP,
    requires_followup BOOLEAN DEFAULT FALSE,
    followup_notes TEXT
);

-- Índices
CREATE INDEX idx_users_company ON users(company_id);
CREATE INDEX idx_equipment_client ON equipment(client_id);
CREATE INDEX idx_service_requests_client ON service_requests(client_id);
CREATE INDEX idx_service_requests_equipment ON service_requests(equipment_id);
CREATE INDEX idx_technical_reports_service ON technical_reports(service_request_id);

-- Triggers para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_companies_updated_at
    BEFORE UPDATE ON companies
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_clients_updated_at
    BEFORE UPDATE ON clients
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
