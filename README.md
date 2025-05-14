# Integral Service SPA - Sistema de Gestión de Servicios

Sistema de gestión integral para empresas de servicios técnicos industriales, desarrollado con Streamlit y PostgreSQL.

## 🔧 Características Principales

- Gestión de servicios técnicos
- Control de equipos industriales
- Seguimiento de mantenimientos
- Generación de presupuestos
- Gestión de clientes y contratos
- Reportes técnicos detallados
- Panel de control administrativo

## 📋 Requisitos del Sistema

- Python 3.8+
- PostgreSQL 12+
- pip (gestor de paquetes de Python)
- Terminal con PowerShell (Windows)

## 🚀 Instalación

1. **Clonar el repositorio**
```powershell
git clone <url-del-repositorio>
cd industrial_services_app
```

2. **Configurar el entorno virtual**
```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

3. **Configurar PostgreSQL**
   - Instalar PostgreSQL desde [postgresql.org](https://www.postgresql.org/download/windows/)
   - Durante la instalación:
     - Puerto: 5432
     - Contraseña para usuario postgres: admin
     - Idioma: Spanish

4. **Configurar el archivo .env**
```env
DATABASE_URL=postgresql://postgres:admin@localhost:5432/integral_service_db
SECRET_KEY=tu-clave-secreta-aqui
COMPANY_NAME=Integral Service SPA
ENVIRONMENT=development
```

5. **Inicializar la base de datos**
```powershell
python database/init_db.py
```

## 🏃‍♂️ Ejecutar la Aplicación

```powershell
streamlit run main.py
```

## 👥 Roles de Usuario

### Administrador
- Gestión completa del sistema
- Dashboard administrativo
- Gestión de usuarios y permisos
- Control de precios y presupuestos
- Reportes y estadísticas

### Supervisor
- Asignación de técnicos
- Seguimiento de servicios
- Aprobación de informes
- Gestión de programación

### Técnico
- Registro de servicios realizados
- Informes técnicos
- Registro de materiales utilizados
- Calendario de servicios

### Cliente
- Solicitud de servicios
- Seguimiento de mantenimientos
- Visualización de informes
- Acceso a facturas

## 📱 Módulos Principales

### Gestión de Clientes
- Registro de empresas
- Contratos y condiciones
- Historial de servicios
- Equipos registrados

### Gestión de Equipos
- Registro detallado
- Especificaciones técnicas
- Historial de mantenimiento
- Estados y ubicaciones

### Servicios Técnicos
- Solicitudes de servicio
- Programación
- Seguimiento en tiempo real
- Informes técnicos

### Presupuestos y Facturación
- Generación automática
- Cálculo de costos
- Control de pagos
- Histórico de transacciones

## 🔄 Flujo de Trabajo

1. **Solicitud de Servicio**
   - Cliente genera solicitud
   - Especifica tipo de servicio
   - Selecciona equipo
   - Describe el problema

2. **Procesamiento**
   - Supervisor revisa solicitud
   - Asigna técnico
   - Programa fecha
   - Genera presupuesto inicial

3. **Ejecución**
   - Técnico realiza servicio
   - Registra trabajo realizado
   - Documenta materiales
   - Genera informe técnico

4. **Cierre**
   - Supervisor aprueba informe
   - Cliente valida trabajo
   - Se genera factura
   - Se programa siguiente mantenimiento

## 🛠 Configuración Técnica

### Base de Datos
- PostgreSQL para datos estructurados
- Modelos SQLAlchemy
- Migraciones automáticas

### Backend
- Python con Streamlit
- SQLAlchemy ORM
- JWT para autenticación

### Frontend
- Interfaz Streamlit
- Componentes responsive
- Formularios dinámicos

## 📊 Tipos de Servicio

- Automatización Industrial
- Refrigeración
- Electromecánica Industrial
- Neumática
- Hidráulica

## 💼 Tipos de Contrato

- Spot (Sin Contrato)
- Contrato Básico
- Contrato Premium
- Contrato Personalizado

## 🔐 Seguridad

- Autenticación JWT
- Roles y permisos
- Encriptación de datos sensibles
- Registro de actividades

## 📈 Reportes Disponibles

- Dashboard gerencial
- Estadísticas de servicios
- Rendimiento de técnicos
- Control de costos
- Satisfacción de clientes

## 🤝 Soporte

Para soporte técnico, contactar a:
- Email: soporte@integralservice.cl
- Teléfono: +56 9 XXXX XXXX

## 🔄 Actualizaciones

El sistema se actualiza regularmente con:
- Nuevas funcionalidades
- Mejoras de seguridad
- Optimizaciones de rendimiento
- Corrección de errores

## 📝 Licencia

Todos los derechos reservados - Integral Service SPA
