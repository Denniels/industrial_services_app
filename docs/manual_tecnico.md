# Manual Técnico - Integral Service SPA

## 🔧 Arquitectura del Sistema

### 1. Stack Tecnológico
- **Frontend**: Streamlit
- **Backend**: Python
- **Base de Datos**: PostgreSQL
- **ORM**: SQLAlchemy
- **Autenticación**: JWT

### 2. Estructura del Proyecto
```
industrial_services_app/
├── auth/               # Autenticación y autorización
├── database/          # Modelos y configuración BD
├── pages/             # Interfaces de usuario
│   ├── admin/        # Páginas administrativas
│   ├── technician/   # Páginas para técnicos
│   └── client/       # Páginas para clientes
└── utils/            # Utilidades generales
```

## 📊 Base de Datos

### Modelo de Datos
El sistema utiliza una base de datos PostgreSQL con las siguientes entidades principales:

#### Entidades Core
1. **Companies**
   - Gestión de empresas clientes y proveedoras
   - Tracking de información fiscal y de contacto
   - Relaciones con usuarios y servicios

2. **Users**
   - Sistema de roles múltiples
   - Autenticación JWT
   - Perfiles personalizados por rol

3. **Equipment**
   - Catálogo de equipos industriales
   - Especificaciones técnicas en formato JSON
   - Histórico de mantenimiento

4. **Services**
   - Solicitudes de servicio
   - Asignación de técnicos
   - Seguimiento de estados

#### Diagrama ER
Ver el [Diagrama Completo](database_diagram.md)

### Índices y Optimización
```sql
-- Índices principales
CREATE INDEX idx_users_company ON users(company_id);
CREATE INDEX idx_equipment_client ON equipment(client_id);
CREATE INDEX idx_service_requests_client ON service_requests(client_id);
```

### Mantenimiento DB
```powershell
# Backup diario automatizado
.\scripts\backup_db.ps1

# Verificación de integridad
.\scripts\check_db_integrity.ps1
```

### 3. Modelos de Base de Datos

#### 3.1 Tabla Users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    is_active BOOLEAN DEFAULT true
);
```

[Documentación completa de todas las tablas...]

## 🔒 Seguridad

### Autenticación
- JWT con rotación de tokens
- Almacenamiento seguro de contraseñas (bcrypt)
- Rate limiting en intentos de login

### Control de Accesos
```python
@require_role(['admin', 'supervisor'])
def admin_dashboard():
    # Lógica del dashboard
    pass
```

### Protección de Datos
1. **Encriptación**
   - Datos sensibles en reposo
   - Comunicaciones TLS
   - Claves en variables de entorno

2. **Validación**
   - Sanitización de inputs
   - Prevención de SQL injection
   - Validación de tipos de archivo

3. **Auditoría**
   - Logs de acceso
   - Registro de cambios
   - Alertas de seguridad

### 4. API y Endpoints

#### 4.1 Autenticación
- POST /auth/login
- POST /auth/refresh
- POST /auth/logout

#### 4.2 Servicios
- GET /services
- POST /services
- PUT /services/{id}
- DELETE /services/{id}

### 5. Seguridad

#### 5.1 Autenticación
- JWT para tokens de acceso
- Refresh tokens
- Encriptación de contraseñas

#### 5.2 Autorización
- RBAC (Control de acceso basado en roles)
- Middleware de verificación
- Logs de acceso

### 6. Configuración del Entorno

#### 6.1 Variables de Entorno
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/db
SECRET_KEY=your-secret-key
ENVIRONMENT=development
```

#### 6.2 Dependencias
```plaintext
streamlit>=1.22.0
pandas>=1.5.3
sqlalchemy>=2.0.0
...
```

## 📊 Monitoreo

### Sistema de Logs
```python
logger.error("Error crítico: {}".format(error))
logger.warning("Advertencia: {}".format(warning))
logger.info("Información: {}".format(info))
```

### Métricas
- Tiempo de respuesta
- Uso de recursos
- Errores por minuto

### Alertas
- Notificaciones por email
- Integración con Slack
- Escalamiento automático

### 7. Despliegue

#### 7.1 Desarrollo Local
```powershell
# Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run main.py
```

#### 7.2 Producción
- Usar Nginx como proxy inverso
- Configurar SSL/TTLS
- Implementar backups automáticos

## 🔧 Mantenimiento

### Tareas Programadas
1. **Diarias**
   - Backup de base de datos
   - Limpieza de logs
   - Verificación de servicios

2. **Semanales**
   - Análisis de rendimiento
   - Optimización de índices
   - Rotación de logs

3. **Mensuales**
   - Actualización de dependencias
   - Revisión de seguridad
   - Limpieza de archivos temporales

### Recuperación
```powershell
# Restaurar desde backup
.\scripts\restore_db.ps1 backup_20250514.sql

# Verificar integridad
.\scripts\verify_system.ps1
```

### 8. Mantenimiento

#### 8.1 Backups
- Respaldo diario de base de datos
- Respaldo semanal completo
- Rotación de logs

#### 8.2 Monitoreo
- Logs de aplicación
- Métricas de rendimiento
- Alertas automáticas

### 9. Integración y Despliegue Continuo

#### 9.1 Pipeline CI/CD
```yaml
stages:
  - test
  - build
  - deploy
```

### 10. Troubleshooting

#### 10.1 Problemas Comunes
- Errores de conexión a BD
- Problemas de autenticación
- Errores de permisos

#### 10.2 Logs
- Ubicación de logs
- Formato de logs
- Niveles de logging

### 11. Mejores Prácticas

#### 11.1 Código
- PEP 8 para Python
- Docstrings
- Type hints

#### 11.2 Base de Datos
- Índices optimizados
- Consultas eficientes
- Manejo de transacciones

### 12. Escalabilidad

#### 12.1 Vertical
- Recursos de servidor
- Configuración de BD

#### 12.2 Horizontal
- Load balancing
- Sharding de BD

## 📞 Soporte

### Niveles de Servicio
1. **Nivel 1**
   - Problemas de acceso
   - Errores de usuario
   - Consultas generales

2. **Nivel 2**
   - Problemas técnicos
   - Configuración avanzada
   - Optimización

3. **Nivel 3**
   - Incidentes críticos
   - Problemas de seguridad
   - Cambios mayores

### Contacto
- **Email**: soporte@integralservice.cl
- **Teléfono**: +56 9 XXXX XXXX
- **Horario**: 24/7

## 🔄 Actualizaciones

### Proceso de Despliegue
1. Backup del sistema
2. Activar modo mantenimiento
3. Actualizar código
4. Ejecutar migraciones
5. Pruebas de regresión
6. Desactivar modo mantenimiento

### Rollback
```powershell
# Revertir última actualización
.\scripts\rollback.ps1 --version previous

# Restaurar datos
.\scripts\restore_data.ps1 --backup pre_update
```
