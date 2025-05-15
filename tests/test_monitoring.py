# -*- coding: utf-8 -*-
"""
Pruebas unitarias para el sistema de monitoreo
"""

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import (
    Base, User, UserRole, 
    MonitoringDevice, MonitoredVariable, 
    VariableReading
)
from datetime import datetime

class TestMonitoring(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configurar la base de datos de prueba"""
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()

    def setUp(self):
        """Preparar datos de prueba"""
        # Limpiar datos existentes
        self.session.query(VariableReading).delete()
        self.session.query(MonitoredVariable).delete()
        self.session.query(MonitoringDevice).delete()
        self.session.query(User).delete()
        self.session.commit()

        # Crear usuario de prueba
        self.user = User(
            username="testuser",
            email="test@test.com",
            password="testpass",
            role=UserRole.CLIENT
        )
        self.session.add(self.user)
        self.session.commit()

        # Crear dispositivo de prueba
        self.device = MonitoringDevice(
            client_id=self.user.id,
            device_serial="TEST001",
            device_type="SENSOR",
            is_active=True
        )
        self.session.add(self.device)
        self.session.commit()

    def test_add_monitoring_device(self):
        """Probar la creación de un dispositivo de monitoreo"""
        device = self.session.query(MonitoringDevice)\
            .filter_by(device_serial="TEST001")\
            .first()
        self.assertIsNotNone(device)
        self.assertEqual(device.client_id, self.user.id)
        self.assertEqual(device.variables_count, 0)

    def test_add_monitored_variable(self):
        """Probar la adición de una variable monitorizada"""
        variable = MonitoredVariable(
            device_id=self.device.id,
            name="Temperature",
            description="Room temperature",
            unit="°C",
            min_value=0,
            max_value=50
        )
        self.session.add(variable)
        self.session.commit()
        
        self.device.variables_count += 1
        self.session.commit()
        
        self.assertIsNotNone(variable)
        self.assertEqual(variable.name, "Temperature")
        self.assertEqual(variable.unit, "°C")
        
        # Verificar que el contador de variables se incrementó
        device = self.session.query(MonitoringDevice).get(self.device.id)
        self.assertEqual(device.variables_count, 1)

    def test_add_reading(self):
        """Probar la adición de una lectura"""
        # Crear variable
        variable = MonitoredVariable(
            device_id=self.device.id,
            name="Pressure",
            description="System pressure",
            unit="PSI",
            min_value=0,
            max_value=100
        )
        self.session.add(variable)
        self.device.variables_count += 1
        self.session.commit()
        
        # Agregar algunas lecturas
        readings = [
            VariableReading(variable_id=variable.id, value=10.5),
            VariableReading(variable_id=variable.id, value=11.2),
            VariableReading(variable_id=variable.id, value=12.0)
        ]
        self.session.add_all(readings)
        self.session.commit()
        
        # Verificar último valor
        latest = self.session.query(VariableReading)\
            .filter_by(variable_id=variable.id)\
            .order_by(VariableReading.timestamp.desc())\
            .first()
        self.assertEqual(latest.value, 12.0)

    def test_max_variables_limit(self):
        """Probar el límite máximo de variables por dispositivo"""
        device = self.session.query(MonitoringDevice).get(self.device.id)
        max_vars = device.max_variables
        
        # Intentar agregar más variables que el límite
        for i in range(max_vars + 1):
            try:
                variable = MonitoredVariable(
                    device_id=device.id,
                    name=f"Var{i}",
                    description=f"Test variable {i}",
                    unit="units"
                )
                self.session.add(variable)
                device.variables_count += 1
                self.session.commit()
                
                if i >= max_vars:
                    self.fail("No se respetó el límite máximo de variables")
            except:
                self.assertEqual(i, max_vars)
                break
        
        # Verificar que no se excedió el límite
        device = self.session.query(MonitoringDevice).get(self.device.id)
        self.assertEqual(device.variables_count, max_vars)

    def test_cascade_delete(self):
        """Probar el borrado en cascada"""
        # Crear variable
        variable = MonitoredVariable(
            device_id=self.device.id,
            name="Test",
            description="Test variable",
            unit="units"
        )
        self.session.add(variable)
        self.device.variables_count += 1
        self.session.commit()
        
        # Agregar algunas lecturas
        readings = [
            VariableReading(variable_id=variable.id, value=1.0),
            VariableReading(variable_id=variable.id, value=2.0)
        ]
        self.session.add_all(readings)
        self.session.commit()
        
        # Borrar el dispositivo
        self.session.delete(self.device)
        self.session.commit()
        
        # Verificar que todo se borró
        self.assertIsNone(
            self.session.query(MonitoringDevice)
                .filter_by(id=self.device.id)
                .first()
        )
        self.assertIsNone(
            self.session.query(MonitoredVariable)
                .filter_by(id=variable.id)
                .first()
        )
        self.assertEqual(
            0,
            self.session.query(VariableReading)
                .filter_by(variable_id=variable.id)
                .count()
        )

    def test_relationships(self):
        """Probar las relaciones entre entidades"""
        # Crear una variable
        variable = MonitoredVariable(
            device_id=self.device.id,
            name="Test",
            description="Test variable",
            unit="units"
        )
        self.session.add(variable)
        self.device.variables_count += 1
        self.session.commit()
        
        # Verificar relación Device -> Variable
        device = self.session.query(MonitoringDevice).get(self.device.id)
        self.assertEqual(len(device.variables), 1)
        self.assertEqual(device.variables[0].name, "Test")
        
        # Verificar relación User -> Device
        user = self.session.query(User).get(self.user.id)
        self.assertEqual(len(user.devices), 1)
        self.assertEqual(user.devices[0].device_serial, "TEST001")

    def tearDown(self):
        """Limpiar datos de prueba"""
        self.session.query(VariableReading).delete()
        self.session.query(MonitoredVariable).delete()
        self.session.query(MonitoringDevice).delete()
        self.session.query(User).delete()
        self.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Cerrar la sesión"""
        cls.session.close()

if __name__ == '__main__':
    unittest.main()
