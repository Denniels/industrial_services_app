# Sistema de Gestión - Integral Service SPA

## Descripción
Sistema integral para la gestión de servicios industriales, desarrollado con Python, Streamlit y PostgreSQL. La aplicación permite gestionar solicitudes de servicio, seguimiento de técnicos, administración de clientes y generación de reportes para servicios de automatización, refrigeración, electromecánica, neumática e hidráulica.

## Características Principales
- 🔐 Autenticación multinivel (Administrador, Técnico, Cliente, Supervisor)
- 📊 Dashboard personalizado para cada tipo de usuario
- 🛠 Gestión de servicios técnicos industriales
- 📅 Programación y seguimiento de servicios
- 📝 Generación de reportes y documentación
- 📱 Interfaz responsive y amigable
- 🔄 Integración con PostgreSQL para almacenamiento seguro

## Requisitos del Sistema
- Python 3.8 o superior
- PostgreSQL 12 o superior
- Conexión a Internet para recursos externos
- Navegador web moderno
- Sistema operativo: Windows, Linux o macOS

## Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Denniels/industrial_services_app.git
cd industrial_services_app
```

### 2. Configurar el Entorno Virtual
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos
1. Asegúrate de tener PostgreSQL instalado y ejecutándose
2. Crea un archivo `.env` basado en `.env.example`
3. Ejecuta los scripts de inicialización:
```bash
python database/init_db.py
python database/init_tables.py
```

### 5. Iniciar la Aplicación
```bash
streamlit run main.py
```

## Estructura del Proyecto
```
industrial_services_app/
├── auth/                   # Autenticación y autorización
├── database/              # Gestión de base de datos
├── docs/                  # Documentación detallada
├── pages/                 # Interfaces de usuario
│   ├── admin/            # Panel de administración
│   ├── client/           # Portal de clientes
│   └── technician/       # Portal de técnicos
├── utils/                # Utilidades y helpers
└── uploads/              # Archivos subidos por usuarios
```

## Credenciales por Defecto
- **Usuario Administrador:**
  - Usuario: admin
  - Contraseña: admin
  - *Se requiere cambio de contraseña en el primer inicio de sesión*

## Documentación
Para más detalles, consulta los siguientes documentos:
- [Manual de Usuario](docs/manual_usuario.md)
- [Manual Técnico](docs/manual_tecnico.md)
- [Catálogo de Servicios](docs/catalogo_servicios.md)
- [Diagrama de Base de Datos](docs/database_diagram.md)

## Seguridad
- Todas las contraseñas se almacenan hasheadas
- Autenticación basada en tokens JWT
- Validación de entrada en todos los formularios
- Protección contra inyección SQL
- Manejo seguro de archivos subidos

## Mantenimiento
- Backups automáticos de la base de datos
- Scripts de diagnóstico y verificación
- Logs detallados de operaciones
- Herramientas de mantenimiento incluidas

## Soporte
Para soporte técnico o reportar problemas:
1. Abre un issue en GitHub
2. Contacta al equipo de desarrollo
3. Consulta la documentación técnica

## Licencia
Este proyecto está licenciado bajo términos privativos para uso exclusivo de Integral Service SPA.

## Actualizaciones y Versiones
- Versión actual: 1.0.0
- Última actualización: Mayo 2025
- Registro de cambios: Ver [CHANGELOG.md](CHANGELOG.md)
