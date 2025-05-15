# -*- coding: utf-8 -*-
"""
Configuración para las pruebas unitarias
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al path de Python
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configuración de la base de datos de prueba
TEST_DATABASE = {
    'host': 'localhost',
    'database': 'test_industrial_services',
    'user': 'test_user',
    'password': 'test_pass',
    'port': 5432,
    'client_encoding': 'utf8'
}

# Configurar variables de entorno para las pruebas
os.environ.update({
    'DATABASE_HOST': TEST_DATABASE['host'],
    'DATABASE_NAME': TEST_DATABASE['database'],
    'DATABASE_USER': TEST_DATABASE['user'],
    'DATABASE_PASSWORD': TEST_DATABASE['password'],
    'DATABASE_PORT': str(TEST_DATABASE['port']),
    'TEST_MODE': 'True'
})
