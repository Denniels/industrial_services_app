-- Crear tipos ENUM
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
        CREATE TYPE user_role AS ENUM ('admin', 'technician', 'client', 'supervisor');
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'service_type') THEN
        CREATE TYPE service_type AS ENUM ('Automatizacion', 'Refrigeracion', 'Electromecanica', 'Neumatica', 'Hidraulica');
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'service_status') THEN
        CREATE TYPE service_status AS ENUM ('Pendiente', 'Programado', 'En Proceso', 'Completado', 'Cancelado');
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'contract_type') THEN
        CREATE TYPE contract_type AS ENUM ('Sin Contrato', 'Contrato Basico', 'Contrato Premium', 'Contrato Personalizado');
    END IF;
END $$;

-- Tabla de Empresas
CREATE TABLE IF NOT EXISTS companies (
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
CREATE TABLE IF NOT EXISTS users (
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

-- Tabla de Tecnicos
CREATE TABLE IF NOT EXISTS technicians (
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
CREATE TABLE IF NOT EXISTS clients (
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
CREATE TABLE IF NOT EXISTS equipment_types (
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
CREATE TABLE IF NOT EXISTS equipment (
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

-- Tabla de Precios de Servicios
CREATE TABLE IF NOT EXISTS service_pricing (
    id SERIAL PRIMARY KEY,
    service_type service_type NOT NULL,
    hourly_rate DECIMAL(10,2) NOT NULL,
    travel_cost DECIMAL(10,2),
    min_service_cost DECIMAL(10,2),
    emergency_multiplier DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE(service_type)
);

-- Tabla de Precios de Contratos
CREATE TABLE IF NOT EXISTS contract_pricing (
    id SERIAL PRIMARY KEY,
    contract_type contract_type NOT NULL,
    service_type service_type NOT NULL,
    discount_percentage DECIMAL(5,2),
    min_monthly_services INTEGER,
    response_time_hours INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE(contract_type, service_type)
);
