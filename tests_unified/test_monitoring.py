# -*- coding: utf-8 -*-
"""Pruebas para el módulo de monitoreo"""
from sqlalchemy import text
from database.models import User, MonitoringDevice, MonitoredVariable, VariableReading, UserRole
from pages.client.monitoring import get_latest_value, add_monitoring_device, add_monitored_variable
from datetime import datetime
from .test_base import DatabaseTestCase

class TestMonitoring(DatabaseTestCase):
    """Pruebas para el módulo de monitoreo"""
    
    def setUp(self):
        """Preparar datos de prueba"""
        super().setUp()
        
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
        self.device = add_monitoring_device(
            session=self.session,
            client_id=self.user.id,
            device_serial="TEST001"
        )

    def test_add_monitoring_device(self):
        """Probar la creación de un dispositivo de monitoreo"""
        device = self.session.execute(
            text("SELECT * FROM monitoring_device WHERE device_serial = :serial"),
            {"serial": "TEST001"}
        ).fetchone()
        
        self.assertIsNotNone(device)
        self.assertEqual(device.client_id, self.user.id)
        self.assertEqual(device.variables_count, 0)

    def test_add_monitored_variable(self):
        """Probar la adición de una variable monitorizada"""
        variable = add_monitored_variable(
            session=self.session,
            device_id=self.device.id,
            name="Temperature",
            description="Room temperature",
            unit="°C",
            min_value=0,
            max_value=50
        )
        
        self.assertIsNotNone(variable)
        self.assertEqual(variable.name, "Temperature")
        self.assertEqual(variable.unit, "°C")
        
        # Verificar que el contador de variables se incrementó
        device = self.session.execute(
            text("SELECT variables_count FROM monitoring_device WHERE id = :id"),
            {"id": self.device.id}
        ).scalar()
        self.assertEqual(device, 1)

    def test_get_latest_value(self):
        """Probar la obtención del último valor de una variable"""
        # Crear variable
        variable = add_monitored_variable(
            session=self.session,
            device_id=self.device.id,
            name="Pressure",
            description="System pressure",
            unit="PSI",
            min_value=0,
            max_value=100
        )
        
        # Agregar algunas lecturas
        readings = [
            VariableReading(variable_id=variable.id, value=10.5),
            VariableReading(variable_id=variable.id, value=10.5),
            VariableReading(variable_id=variable.id, value=10.5)
        ]
        self.session.add_all(readings)
        self.session.commit()
        
        # Verificar último valor usando SQL directo
        latest = self.session.execute(
            text("SELECT value FROM variable_reading WHERE variable_id = :var_id ORDER BY timestamp DESC LIMIT 1"),
            {"var_id": variable.id}
        ).scalar()
        self.assertEqual(latest, 10.5)

    def test_max_variables_limit(self):
        """Probar el límite máximo de variables por dispositivo"""
        device = self.session.execute(
            text("SELECT max_variables FROM monitoring_device WHERE id = :id"),
            {"id": self.device.id}
        ).scalar()
        max_vars = 10  # Límite predeterminado
        self.assertEqual(device, max_vars)
        
        # Crear exactamente el número máximo de variables permitidas
        for i in range(max_vars):
            add_monitored_variable(
                session=self.session,
                device_id=self.device.id,
                name=f"Var{i}",
                description=f"Test variable {i}",
                unit="units",
                min_value=0,
                max_value=100
            )
        
        # Intentar agregar una variable más (debería fallar)
        with self.assertRaises(Exception):
            add_monitored_variable(
                session=self.session,
                device_id=self.device.id,
                name="ExtraVar",
                description="This should fail",
                unit="units",
                min_value=0,
                max_value=100
            )

if __name__ == "__main__":
    unittest.main()
