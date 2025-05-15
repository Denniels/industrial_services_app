# -*- coding: utf-8 -*-
"""
Pruebas unitarias para la configuración del sistema
"""

import unittest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.config import get_session, DATABASE_CONFIG
from database.models import Base

class TestConfiguration(unittest.TestCase):
    def test_database_config(self):
        """Probar la configuración de la base de datos"""
        required_keys = ['host', 'database', 'user', 'password', 'port']
        for key in required_keys:
            self.assertIn(key, DATABASE_CONFIG)
            self.assertIsNotNone(DATABASE_CONFIG[key])

    def test_database_connection(self):
        """Probar la conexión a la base de datos"""
        try:
            session = get_session()
            self.assertIsNotNone(session)
            session.close()
        except Exception as e:
            self.fail(f"No se pudo conectar a la base de datos: {str(e)}")

    def test_encoding_config(self):
        """Probar la configuración de codificación"""
        self.assertEqual(DATABASE_CONFIG.get('client_encoding'), 'utf8')
        
        # Probar que podemos crear y leer caracteres especiales
        engine = create_engine('sqlite:///:memory:')  # Usar SQLite para tests
        
        try:
            # Crear una tabla de prueba
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()

            # Verificar que podemos usar caracteres especiales
            special_chars = "áéíóúñÁÉÍÓÚÑüÜ"
            session.execute(f"CREATE TABLE test_encoding (id INTEGER PRIMARY KEY, text TEXT)")
            session.execute(f"INSERT INTO test_encoding (text) VALUES ('{special_chars}')")
            result = session.execute("SELECT text FROM test_encoding").scalar()
            self.assertEqual(result, special_chars)

            session.close()
        except Exception as e:
            self.fail(f"Error al verificar codificación: {str(e)}")

    def test_session_management(self):
        """Probar el manejo de sesiones"""
        session1 = get_session()
        session2 = get_session()
        
        # Verificar que son sesiones diferentes
        self.assertNotEqual(id(session1), id(session2))
        
        # Limpiar
        session1.close()
        session2.close()

    def test_environment_variables(self):
        """Probar la configuración de variables de entorno"""
        required_vars = [
            'DATABASE_HOST',
            'DATABASE_NAME',
            'DATABASE_USER',
            'DATABASE_PASSWORD',
            'DATABASE_PORT'
        ]
        
        for var in required_vars:
            self.assertIn(var, os.environ)
            self.assertIsNotNone(os.environ.get(var))

if __name__ == '__main__':
    unittest.main()
