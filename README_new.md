# Industrial Services App 🏭

## Descripción
Sistema de gestión integral para empresas de servicios técnicos industriales. Permite administrar servicios técnicos, mantenimientos, equipos, clientes y generar reportes detallados.

![Badge Python](https://img.shields.io/badge/Python-3.8+-blue)
![Badge PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue)
![Badge Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![Badge License](https://img.shields.io/badge/License-MIT-green)

## 🔑 Características Principales

### Gestión de Servicios
- Solicitudes de servicio
- Programación de mantenimientos
- Seguimiento en tiempo real
- Reportes técnicos detallados
- Historial de servicios

### Control de Equipos
- Registro detallado de equipos
- Especificaciones técnicas
- Historial de mantenimiento
- Programación de mantenimiento preventivo
- Alertas de mantenimiento

### Gestión de Clientes
- Perfiles de empresa
- Contratos de servicio
- Historial de servicios
- Facturación y presupuestos
- Portal de cliente

### Panel Administrativo
- Dashboard de KPIs
- Gestión de técnicos
- Asignación de servicios
- Reportes y análisis
- Control de inventario

## 🗄️ Estructura de la Base de Datos

### Diagrama ER
![Diagrama ER](docs/images/er_diagram.png)

### Principales Entidades

#### Usuarios y Roles
- Administradores
- Técnicos
- Clientes
- Supervisores

#### Equipos
- Tipos de equipo
- Especificaciones técnicas
- Historial de mantenimiento
- Ubicación y estado

#### Servicios
- Solicitudes
- Programación
- Reportes técnicos
- Seguimiento

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.8+
- **Base de Datos**: PostgreSQL 12+
- **ORM**: SQLAlchemy
- **Frontend**: Streamlit
- **Autenticación**: JWT
- **Reportes**: ReportLab
- **Logging**: Python logging

## ⚙️ Requisitos

### Software
- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)
- Git

### Hardware Recomendado
- CPU: 2 cores o más
- RAM: 4GB mínimo
- Almacenamiento: 10GB disponibles

## 📦 Instalación

1. **Clonar el Repositorio**
```powershell
git clone https://github.com/Denniels/industrial-services-app.git
cd industrial-services-app
```

2. **Configurar Entorno Virtual**
```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

3. **Configurar Base de Datos**
```powershell
# Asegúrate de tener PostgreSQL instalado y ejecutando
python database/init_db.py
```

4. **Variables de Entorno**
Crear archivo `.env` con:
```env
DATABASE_URL=postgresql://postgres:admin@localhost:5432/industrial_service_db
SECRET_KEY=your-secret-key
COMPANY_NAME=Integral Service SPA
ENVIRONMENT=development
```

5. **Iniciar la Aplicación**
```powershell
python main.py
```

## 🔧 Configuración

### Base de Datos
La aplicación utiliza PostgreSQL. Configuración por defecto:
- Host: localhost
- Puerto: 5432
- Usuario: postgres
- Contraseña: admin
- Base de datos: integral_service_db

### Roles de Usuario
1. **Administrador**
   - Acceso total al sistema
   - Gestión de usuarios
   - Reportes administrativos

2. **Técnico**
   - Gestión de servicios asignados
   - Creación de reportes técnicos
   - Actualización de estados

3. **Cliente**
   - Solicitud de servicios
   - Seguimiento de servicios
   - Acceso a reportes

## 📚 Documentación

- [Manual de Usuario](docs/manual_usuario.md)
- [Manual Técnico](docs/manual_tecnico.md)
- [Catálogo de Servicios](docs/catalogo_servicios.md)
- [Procedimientos](docs/procedimientos.md)

## 🤝 Contribución

1. Fork el proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: alguna característica asombrosa'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.

## ✉️ Contacto

Daniel Montes - [@Denniels](https://github.com/Denniels)

Link del Proyecto: [https://github.com/Denniels/industrial-services-app](https://github.com/Denniels/industrial-services-app)
