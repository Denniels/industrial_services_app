# Manual Técnico - Sistema de Gestión Integral Service

## Índice
1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Tecnologías Utilizadas](#tecnologías-utilizadas)
3. [Configuración del Entorno](#configuración-del-entorno)
4. [Estructura de la Base de Datos](#estructura-de-la-base-de-datos)
5. [Seguridad](#seguridad)
6. [Mantenimiento](#mantenimiento)
7. [Procedimientos de Backup](#procedimientos-de-backup)
8. [Troubleshooting](#troubleshooting)

## Arquitectura del Sistema

### Stack Tecnológico
```
Frontend:
- Streamlit (Framework web)
- HTML/CSS/JavaScript
- Plotly (Visualización de datos)

Backend:
- Python 3.12
- SQLAlchemy (ORM)
- JWT (Autenticación)
- Bcrypt (Hashing)

Base de Datos:
- PostgreSQL 15
- Alembic (Migraciones)

Servicios:
- Servidor Web: Streamlit
- Base de Datos: PostgreSQL
- Sistema de Archivos: Local
```

### Estructura del Proyecto
```
industrial_services_app/
├── auth/                 # Autenticación
│   └── login.py         # Manejo de sesiones
├── database/            # Capa de datos
│   ├── models.py       # Modelos SQLAlchemy
│   ├── config.py       # Configuración DB
│   └── migrations/     # Migraciones Alembic
├── pages/              # Interfaces de usuario
├── utils/              # Utilidades
└── main.py            # Punto de entrada
```

## Tecnologías Utilizadas

### Dependencias Principales
```python
streamlit==1.32.0
sqlalchemy==2.0.27
psycopg2-binary==2.9.9
python-jose==3.3.0
bcrypt==4.1.2
python-dotenv==1.0.1
plotly==5.18.0
pandas==2.2.0
alembic==1.13.1
```

### Versiones Compatibles
- Python: 3.8 - 3.12
- PostgreSQL: 12 - 15
- Sistemas Operativos:
  - Windows 10/11
  - Ubuntu 20.04+
  - macOS 11+

## Configuración del Entorno

### Variables de Entorno (.env)
```env
# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=integral_service_db
DB_USER=postgres
DB_PASSWORD=your_password

# Seguridad
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración de la aplicación
ENVIRONMENT=development
DEBUG=True
UPLOAD_FOLDER=./uploads
```

### Configuración de PostgreSQL
```sql
-- Crear base de datos
CREATE DATABASE integral_service_db
WITH 
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Spain.1252'
    LC_CTYPE = 'Spanish_Spain.1252';

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
```

## Estructura de la Base de Datos

### Tablas Principales
1. **users**
   - Almacena información de usuarios
   - Maneja roles y permisos
   - Gestiona autenticación

2. **service_requests**
   - Registra solicitudes de servicio
   - Mantiene estado y seguimiento
   - Relaciona clientes y técnicos

3. **companies**
   - Información de empresas cliente
   - Datos de contacto y ubicación
   - Historial de servicios

### Relaciones y Constraints
```sql
-- Ejemplo de relaciones
ALTER TABLE service_requests
ADD CONSTRAINT fk_client
FOREIGN KEY (client_id) REFERENCES users(id);

ALTER TABLE service_requests
ADD CONSTRAINT fk_technician
FOREIGN KEY (technician_id) REFERENCES users(id);
```

## Seguridad

### Autenticación
1. **JWT (JSON Web Tokens)**
   - Generación de tokens seguros
   - Validación de sesiones
   - Refresh tokens

2. **Hashing de Contraseñas**
   - Uso de Bcrypt
   - Salt aleatorio
   - Iteraciones configurables

### Autorización
1. **Roles de Usuario**
   - ADMIN
   - TECHNICIAN
   - CLIENT
   - SUPERVISOR

2. **Permisos por Rol**
   - Matriz de permisos
   - Validación por ruta
   - Middleware de autorización

## Mantenimiento

### Tareas Programadas
1. **Backups**
   ```bash
   # Backup diario
   0 0 * * * python /path/to/backup_db.py

   # Limpieza de archivos temporales
   0 1 * * * python /path/to/clean.py
   ```

2. **Monitoreo**
   - Logs de sistema
   - Métricas de rendimiento
   - Alertas automatizadas

### Scripts de Mantenimiento
```python
# Verificar integridad de la base de datos
python database/check_db.py

# Limpiar archivos temporales
python utils/clean_temp_files.py

# Verificar codificación de archivos
python utils/verify_encoding.py
```

## Procedimientos de Backup

### Backup de Base de Datos
```bash
# Backup completo
pg_dump integral_service_db > backup.sql

# Backup comprimido
pg_dump integral_service_db | gzip > backup.gz

# Restauración
psql integral_service_db < backup.sql
```

### Backup de Archivos
```bash
# Backup de uploads
tar -czf uploads_backup.tar.gz ./uploads/

# Backup de configuración
cp .env .env.backup
```

## Troubleshooting

### Problemas Comunes

1. **Error de Conexión DB**
   ```python
   # Verificar conexión
   python database/check_connection.py
   
   # Resetear conexiones
   SELECT pg_terminate_backend(pid) 
   FROM pg_stat_activity 
   WHERE datname = 'integral_service_db';
   ```

2. **Errores de Codificación**
   ```python
   # Verificar codificación
   python utils/check_encoding.py
   
   # Convertir a UTF-8
   python utils/fix_encoding.py
   ```

3. **Problemas de Rendimiento**
   - Revisar logs
   - Analizar consultas lentas
   - Verificar índices

### Logs y Monitoreo
```python
# Ubicación de logs
/logs/
  ├── app.log      # Logs de aplicación
  ├── error.log    # Errores
  ├── access.log   # Accesos
  └── debug.log    # Debugging
```

### Contacto Soporte Técnico
- Email: dev@integralservice.cl
- Teléfono: [número de soporte técnico]
- Repositorio: https://github.com/Denniels/industrial_services_app
