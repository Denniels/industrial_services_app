# Sistema de Gestión - Integral Service SPA 🏭

![Badge Python](https://img.shields.io/badge/Python-3.8+-blue)
![Badge PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue)
![Badge Flask](https://img.shields.io/badge/Flask-2.0+-green)
![Badge SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange)
![Badge Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)
![Badge Tests](https://img.shields.io/badge/tests-passing-brightgreen)

## Descripción
Sistema integral para la gestión de servicios industriales, desarrollado con Python, Flask y PostgreSQL. La aplicación permite gestionar solicitudes de servicio, seguimiento de técnicos, administración de clientes y generación de reportes para servicios de:

- 🔧 Automatización industrial
- ❄️ Refrigeración industrial
- ⚡ Servicios electromecánicos
- 💨 Sistemas neumáticos
- 💧 Sistemas hidráulicos

## 🔑 Características Principales

### Sistema Base
- 🔐 Autenticación JWT con roles múltiples
- 📊 API RESTful con documentación OpenAPI
- 🛠 Arquitectura modular y escalable
- 📱 Interfaz responsive y accesible
- 🔄 Base de datos PostgreSQL con SQLAlchemy 2.0
- 📝 Logging detallado y monitoreo
- ✅ Tests automatizados con +95% de cobertura

### Gestión de Servicios
- 📋 Solicitudes de servicio con priorización
- 📅 Programación inteligente de mantenimientos
- 📍 Seguimiento en tiempo real de técnicos
- 📊 Reportes técnicos detallados
- 📈 Análisis de rendimiento y KPIs
- 🔔 Sistema de notificaciones

### Control de Equipos y Recursos
- 🔧 Registro detallado de equipos industriales
- 📄 Especificaciones técnicas y manuales
- 📊 Historiales de mantenimiento
- ⚡ Monitoreo de variables en tiempo real
- 🚨 Alertas predictivas
- 📦 Gestión de inventario y repuestos

### Portal de Cliente
- 👥 Gestión de usuarios y permisos
- 📱 Interfaz personalizada por rol
- 📊 Dashboard de servicios activos
- 📄 Acceso a documentación técnica
- 💰 Gestión de presupuestos
- 📈 Reportes y estadísticas

## ⚙️ Requisitos del Sistema

### Software
- Python 3.8 o superior
- PostgreSQL 12 o superior
- Git para control de versiones
- Navegador web moderno
- Sistema operativo: Windows, Linux o macOS

### Hardware Recomendado
- CPU: 2 cores o más
- RAM: 4GB mínimo
- Almacenamiento: 10GB disponibles
- Red: Conexión estable a Internet

### Dependencias Principales
- Flask >= 2.0.0
- SQLAlchemy >= 2.0.0
- Flask-SQLAlchemy >= 3.0.0
- Flask-JWT-Extended >= 4.5.0
- Pytest >= 7.0.0
- Python-dotenv >= 1.0.0

## 📦 Instalación

### 1. Clonar el Repositorio
```powershell
git clone https://github.com/Denniels/industrial_services_app.git
cd industrial_services_app
```

### 2. Configurar el Entorno Virtual
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows PowerShell)
.\.venv\Scripts\Activate

# Activar entorno (Linux/macOS)
source .venv/bin/activate

# Instalar dependencias
pip install -e .[dev,test]
```

### 3. Configurar Variables de Entorno
Crear archivo `.env`:
```env
# Base de datos
DATABASE_URL=postgresql://user:pass@localhost:5432/industrial_service_db
DATABASE_TEST_URL=postgresql://user:pass@localhost:5432/industrial_service_test

# Seguridad
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Configuración
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG
```

### 4. Inicializar Base de Datos
```powershell
# Crear base de datos y tablas
python database/init_db.py

# Ejecutar migraciones
alembic upgrade head

# Cargar datos iniciales
python database/init_data.py
```

### 5. Ejecutar Tests
```powershell
# Ejecutar tests con cobertura
pytest tests_unified -v --cov=. --cov-report=html

# Verificar reporte de cobertura
Start-Process "htmlcov/index.html"
```

### 6. Iniciar la Aplicación
```powershell
# Modo desarrollo
python main.py

# Modo producción
gunicorn "main:create_app()" --bind 0.0.0.0:5000 --workers 4
```

## 📁 Estructura del Proyecto
```
industrial_services_app/
├── alembic/              # Migraciones de base de datos
├── auth/                 # Autenticación y autorización
│   ├── jwt.py           # Manejo de tokens JWT
│   ├── login.py         # Lógica de login/logout
│   └── roles.py         # Control de roles y permisos
├── database/            # Capa de datos
│   ├── models/         # Modelos SQLAlchemy
│   ├── repositories/   # Patrón repositorio
│   └── services/      # Lógica de negocio
├── api/                # API RESTful
│   ├── routes/        # Endpoints por módulo
│   ├── schemas/       # Schemas Marshmallow
│   └── swagger/       # Documentación OpenAPI
├── tests_unified/     # Tests automatizados
│   ├── conftest.py    # Configuración de tests
│   ├── test_api.py    # Tests de API
│   ├── test_auth.py   # Tests de autenticación
│   └── test_models.py # Tests de modelos
├── utils/              # Utilidades generales
│   ├── logging.py     # Configuración de logs
│   ├── monitoring.py  # Monitoreo y métricas
│   └── validators.py  # Validadores comunes
├── static/            # Archivos estáticos
├── templates/         # Templates Jinja2
└── uploads/          # Archivos de usuario
```

## 👥 Roles y Credenciales

### Administrador
- Usuario: `admin@integral.com`
- Contraseña: `Admin@2025`
- Acceso total al sistema
- Gestión de usuarios y roles
- Configuración del sistema
- Reportes globales

### Supervisor
- Usuario: `supervisor@integral.com`
- Contraseña: `Supervisor@2025`
- Asignación de servicios
- Gestión de técnicos
- Reportes de rendimiento
- Control de calidad

### Técnico
- Usuario: `tecnico@integral.com`
- Contraseña: `Tecnico@2025`
- Gestión de servicios asignados
- Reportes técnicos
- Registro de mantenimientos
- App móvil de campo

### Cliente
- Usuario: `cliente@empresa.com`
- Contraseña: `Cliente@2025`
- Solicitud de servicios
- Seguimiento de tickets
- Acceso a documentación
- Portal personalizado

*Nota: Se requiere cambio de contraseña en el primer inicio de sesión*

## 📚 Documentación

### Manuales
- [Manual de Usuario](docs/manual_usuario.md)
- [Manual Técnico](docs/manual_tecnico.md)
- [Manual de Instalación](docs/manual_instalacion.md)
- [Manual de API](docs/api_reference.md)

### Técnica
- [Arquitectura del Sistema](docs/arquitectura.md)
- [Diagrama de Base de Datos](docs/database_diagram.md)
- [Documentación de API](docs/api_docs.md)
- [Guía de Desarrollo](docs/dev_guide.md)

### Procesos
- [Catálogo de Servicios](docs/catalogo_servicios.md)
- [Procedimientos Técnicos](docs/procedimientos.md)
- [Políticas de Seguridad](docs/security_policies.md)
- [Plan de Contingencia](docs/contingency_plan.md)

## 🔐 Seguridad

### Autenticación y Autorización
- Tokens JWT con renovación automática
- Roles y permisos granulares
- Sesiones seguras con expiración
- Bloqueo por intentos fallidos
- 2FA opcional para administradores

### Protección de Datos
- Contraseñas hasheadas con bcrypt
- Encriptación de datos sensibles
- Validación estricta de entrada
- Sanitización de datos SQL
- Control de acceso por IP

### Seguridad de Archivos
- Validación de tipos MIME
- Escaneo de malware
- Nombres aleatorios seguros
- Límites de tamaño
- Almacenamiento aislado

### Auditoría
- Registro detallado de acciones
- Detección de anomalías
- Alertas de seguridad
- Backups automáticos
- Logs de auditoría

## 🛠 Mantenimiento y Monitoreo

### Respaldos
- Backups automáticos diarios
- Replicación de base de datos
- Rotación de logs
- Recuperación punto a punto
- Entornos de contingencia

### Monitoreo
- Dashboard de estado
- Métricas de rendimiento
- Alertas configurables
- Monitoreo de recursos
- Logs centralizados

### Herramientas
- Scripts de diagnóstico
- Verificación de integridad
- Limpieza automática
- Recuperación de errores
- Mantenimiento predictivo

### Actualizaciones
- Actualizaciones automáticas
- Rollback seguro
- Migración de datos
- Versionado semántico
- Changelog detallado

## 🤝 Soporte y Contribución

### Soporte Técnico
- **Email**: contacto@integralservicespa.cl
- **Teléfono**: +56 9 6366 9300
- **Horario**: Lun-Vie 9:00-18:00
- **Portal**: https://integralservicespa.cl

### Contribuir
1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

### Reportar Problemas
1. Usa el [Issue Tracker](https://github.com/Denniels/industrial-services-app/issues)
2. Proporciona detalles completos
3. Incluye logs relevantes
4. Agrega capturas de pantalla
5. Sigue las actualizaciones

## 📄 Licencia
Copyright © 2025 Integral Service SPA. Todos los derechos reservados.

Este software está protegido por derechos de autor y su uso está restringido según los términos del Acuerdo de Licencia de Software.

## 🔄 Versiones

### Versión Actual
- **Versión**: 2.0.0
- **Fecha**: Mayo 2025
- **Compatibilidad**: Python 3.8-3.12
- **Estado**: Estable

### Historial
- [CHANGELOG.md](CHANGELOG.md)
- [Notas de Versión](docs/release_notes.md)
- [Guía de Migración](docs/migration_guide.md)

### Próximas Características
- 📱 Aplicación móvil para técnicos
- 🤖 Asignación automática de servicios
- 📊 Dashboard mejorado con ML
- 🔄 Integración con ERP
- 🌐 Soporte multi-idioma
