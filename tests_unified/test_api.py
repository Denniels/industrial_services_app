# -*- coding: utf-8 -*-
"""Pruebas para los endpoints de la API"""
import json
from sqlalchemy import text
from flask import url_for
from database.models import User, MonitoringDevice, MonitoredVariable, UserRole
from .test_base import DatabaseTestCase
from main import create_app

class TestAPIEndpoints(DatabaseTestCase):
    """Pruebas para los endpoints de la API"""

    def setUp(self):
        """Preparar datos y cliente de prueba"""
        super().setUp()
        
        # Crear aplicación de prueba
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Crear contexto de aplicación
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        
        # Crear usuario de prueba
        self.test_password = "Test@Password123"
        self.user = User(
            username="testapi",
            email="testapi@test.com",
            password=self.test_password,
            role=UserRole.CLIENT
        )
        self.session.add(self.user)
        self.session.commit()
        
        # Datos de login
        self.credentials = {
            "username": "testapi",
            "password": self.test_password
        }

    def tearDown(self):
        """Limpiar después de cada prueba"""
        super().tearDown()
        self.ctx.pop()

    def test_login_endpoint(self):
        """Probar el endpoint de login"""
        # Login exitoso
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(self.credentials),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)
        
        # Login fallido - credenciales incorrectas
        bad_credentials = dict(self.credentials)
        bad_credentials['password'] = 'wrong'
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(bad_credentials),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    def test_device_endpoints(self):
        """Probar los endpoints de dispositivos"""
        # Primero hacer login
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(self.credentials),
            content_type='application/json'
        )
        token = json.loads(response.data)['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Crear dispositivo
        device_data = {
            "device_serial": "API001",
            "description": "API Test Device"
        }
        response = self.client.post(
            '/api/devices',
            data=json.dumps(device_data),
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, 201)
        device_id = json.loads(response.data)['id']
        
        # Obtener dispositivo
        response = self.client.get(
            f'/api/devices/{device_id}',
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        device = json.loads(response.data)
        self.assertEqual(device['device_serial'], "API001")
        
        # Actualizar dispositivo
        update_data = {
            "description": "Updated Description"
        }
        response = self.client.put(
            f'/api/devices/{device_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Verificar actualización
        response = self.client.get(
            f'/api/devices/{device_id}',
            headers=headers
        )
        device = json.loads(response.data)
        self.assertEqual(device['description'], "Updated Description")
        
        # Eliminar dispositivo
        response = self.client.delete(
            f'/api/devices/{device_id}',
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Verificar eliminación
        response = self.client.get(
            f'/api/devices/{device_id}',
            headers=headers
        )
        self.assertEqual(response.status_code, 404)

    def test_variable_endpoints(self):
        """Probar los endpoints de variables"""
        # Primero hacer login
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(self.credentials),
            content_type='application/json'
        )
        token = json.loads(response.data)['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Crear dispositivo para las pruebas
        device_data = {
            "device_serial": "VARS001",
            "description": "Variables Test Device"
        }
        response = self.client.post(
            '/api/devices',
            data=json.dumps(device_data),
            content_type='application/json',
            headers=headers
        )
        device_id = json.loads(response.data)['id']
        
        # Crear variable
        variable_data = {
            "name": "Temperature",
            "description": "Room temperature",
            "unit": "°C",
            "min_value": 0,
            "max_value": 50
        }
        response = self.client.post(
            f'/api/devices/{device_id}/variables',
            data=json.dumps(variable_data),
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, 201)
        variable_id = json.loads(response.data)['id']
        
        # Obtener variable
        response = self.client.get(
            f'/api/variables/{variable_id}',
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        variable = json.loads(response.data)
        self.assertEqual(variable['name'], "Temperature")
        
        # Actualizar variable
        update_data = {
            "description": "Updated variable description",
            "max_value": 60
        }
        response = self.client.put(
            f'/api/variables/{variable_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Verificar actualización
        response = self.client.get(
            f'/api/variables/{variable_id}',
            headers=headers
        )
        variable = json.loads(response.data)
        self.assertEqual(variable['description'], "Updated variable description")
        self.assertEqual(variable['max_value'], 60)
        
        # Agregar lectura
        reading_data = {
            "value": 25.5,
            "timestamp": "2025-05-15T10:30:00Z"
        }
        response = self.client.post(
            f'/api/variables/{variable_id}/readings',
            data=json.dumps(reading_data),
            content_type='application/json',
            headers=headers
        )
        self.assertEqual(response.status_code, 201)
        
        # Obtener lecturas
        response = self.client.get(
            f'/api/variables/{variable_id}/readings',
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        readings = json.loads(response.data)
        self.assertEqual(len(readings), 1)
        self.assertEqual(readings[0]['value'], 25.5)

if __name__ == '__main__':
    unittest.main()
