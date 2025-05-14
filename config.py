# -*- coding: utf-8 -*-
"""
Configuración principal de la aplicación Industrial Services
"""

import os
import sys
from dotenv import load_dotenv

# Asegurar que Python use UTF-8 por defecto
if sys.platform.startswith('win'):
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'es-ES.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')
    
    # Forzar UTF-8 en Windows
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Cargar variables de entorno
load_dotenv(encoding='utf-8')

# Configuración de la aplicación
APP_NAME = "Sistema de Gestión - Integral Service SPA"
COMPANY_NAME = os.getenv('COMPANY_NAME', 'Integral Service SPA')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Configuración de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost:5432/integral_service_db')

# Configuración de seguridad
SECRET_KEY = os.getenv('SECRET_KEY', 'tu-clave-secreta-aqui')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 horas

# Estados de servicio
SERVICE_STATUS = {
    'PENDING': 'Pendiente',
    'SCHEDULED': 'Programado',
    'IN_PROGRESS': 'En Proceso',
    'COMPLETED': 'Completado',
    'CANCELLED': 'Cancelado'
}

# Tipos de servicio
SERVICE_TYPES = [
    'AUTOMATION',
    'REFRIGERATION',
    'ELECTROMECHANICAL',
    'PNEUMATIC',
    'HYDRAULIC'
]

# Tipos de contrato
CONTRACT_TYPES = [
    'NONE',
    'BASIC',
    'PREMIUM',
    'CUSTOM'
]

# Mapeo de nombres en español
SERVICE_TYPE_NAMES = {
    'AUTOMATION': 'Automatización',
    'REFRIGERATION': 'Refrigeración',
    'ELECTROMECHANICAL': 'Electromecánica Industrial',
    'PNEUMATIC': 'Neumática',
    'HYDRAULIC': 'Hidráulica'
}

# Tipos de contrato
CONTRACT_TYPES = {
    'NONE': 'Sin Contrato',
    'BASIC': 'Contrato Básico',
    'PREMIUM': 'Contrato Premium',
    'CUSTOM': 'Contrato Personalizado'
}

# Configuración de correo electrónico
EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'False').lower() == 'true'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

# Configuración de archivos
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Configuración de facturación
IVA = 0.19
DEFAULT_OPERATIONAL_COST = 0.15  # 15% por defecto
DEFAULT_PROFIT_MARGIN = 0.25    # 25% por defecto

# Configuración de la interfaz
THEME_COLOR = "#1f77b4"
LOGO_PATH = "assets/logo.png"

# Timeouts y límites
REQUEST_TIMEOUT = 30  # segundos
MAX_RETRY_ATTEMPTS = 3
RATE_LIMIT = "100/minute"
