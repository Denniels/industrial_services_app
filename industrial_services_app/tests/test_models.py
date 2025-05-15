# -*- coding: utf-8 -*-
"""
Pruebas unitarias para los modelos de la base de datos
"""

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import (
    Base, User, Company, Equipment, ServiceRequest,
    UserRole, ServiceType, ServiceStatus
)
from datetime import datetime

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configurar la base de datos de prueba"""
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()

    def setUp(self):
        """Preparar datos de prueba"""
        # Crear compañía de prueba
        self.company = Company(
            name="Test Company",
            rut="12.345.678-9",
            address="Test Address",
            city="Test City",
            region="Test Region"
        )
        self.session.add(self.company)
        self.session.commit()

        # Crear usuario de prueba
        self.user = User(
            username="testuser",
            email="test@test.com",
            password="testpass",
            role=UserRole.CLIENT,
            company_id=self.company.id
        )
        self.session.add(self.user)
        self.session.commit()

    def test_company_creation(self):
        """Probar la creación de una compañía"""
        company = self.session.query(Company).filter_by(name="Test Company").first()
        self.assertIsNotNone(company)
        self.assertEqual(company.rut, "12.345.678-9")

    def test_user_creation(self):
        """Probar la creación de un usuario"""
        user = self.session.query(User).filter_by(username="testuser").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.role, UserRole.CLIENT)

    def test_service_request_creation(self):
        """Probar la creación de una solicitud de servicio"""
        # Crear equipo
        equipment = Equipment(
            name="Test Equipment",
            model="Test Model",
            serial_number="123456"
        )
        self.session.add(equipment)
        self.session.commit()

        # Crear solicitud
        service_request = ServiceRequest(
            client_id=self.user.id,
            equipment_id=equipment.id,
            service_type=ServiceType.AUTOMATION,
            description="Test service request",
            status=ServiceStatus.PENDING
        )
        self.session.add(service_request)
        self.session.commit()

        # Verificar
        request = self.session.query(ServiceRequest).first()
        self.assertIsNotNone(request)
        self.assertEqual(request.client_id, self.user.id)
        self.assertEqual(request.service_type, ServiceType.AUTOMATION)
        self.assertEqual(request.status, ServiceStatus.PENDING)

    def test_relationships(self):
        """Probar las relaciones entre modelos"""
        # Crear solicitud de servicio
        service_request = ServiceRequest(
            client_id=self.user.id,
            service_type=ServiceType.AUTOMATION,
            description="Test service request",
            status=ServiceStatus.PENDING
        )
        self.session.add(service_request)
        self.session.commit()

        # Verificar relación User -> ServiceRequest
        user = self.session.query(User).filter_by(username="testuser").first()
        self.assertTrue(len(user.submitted_requests) > 0)
        self.assertEqual(user.submitted_requests[0].description, "Test service request")

    def tearDown(self):
        """Limpiar datos de prueba"""
        self.session.query(ServiceRequest).delete()
        self.session.query(Equipment).delete()
        self.session.query(User).delete()
        self.session.query(Company).delete()
        self.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Cerrar la sesión"""
        cls.session.close()

if __name__ == '__main__':
    unittest.main()
