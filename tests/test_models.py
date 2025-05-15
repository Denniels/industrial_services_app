# -*- coding: utf-8 -*-
"""
Pruebas unitarias para los modelos de base de datos
"""

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, User, Company, Equipment, ServiceRequest
from database.models import UserRole, ServiceType, ServiceStatus

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configurar la base de datos de prueba"""
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()

    def setUp(self):
        """Preparar cada prueba"""
        self.session.query(ServiceRequest).delete()
        self.session.query(Equipment).delete()
        self.session.query(User).delete()
        self.session.query(Company).delete()
        self.session.commit()

        # Crear compañía de prueba
        self.company = Company(
            name="Test Company",
            rut="76.123.456-7",
            address="Test Address",
            city="Test City",
            region="Test Region"
        )
        self.session.add(self.company)
        self.session.commit()

    def test_company_creation(self):
        """Probar la creación de una compañía"""
        company = self.session.query(Company)\
            .filter_by(rut="76.123.456-7")\
            .first()
        self.assertIsNotNone(company)
        self.assertEqual(company.name, "Test Company")

    def test_user_creation(self):
        """Probar la creación de un usuario"""
        user = User(
            username="testuser",
            email="test@test.com",
            password="testpass",
            role=UserRole.CLIENT,
            company_id=self.company.id,
            first_name="Test",
            last_name="User"
        )
        self.session.add(user)
        self.session.commit()

        created_user = self.session.query(User)\
            .filter_by(email="test@test.com")\
            .first()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, "testuser")
        self.assertEqual(created_user.role, UserRole.CLIENT)

    def test_service_request_creation(self):
        """Probar la creación de una solicitud de servicio"""
        # Crear usuario
        user = User(
            username="testuser",
            email="test@test.com",
            password="testpass",
            role=UserRole.CLIENT,
            company_id=self.company.id
        )
        self.session.add(user)
        self.session.commit()

        # Crear solicitud de servicio
        request = ServiceRequest(
            client_id=user.id,
            description="Test service request",
            status=ServiceStatus.PENDING,
            service_type=ServiceType.MAINTENANCE,
            priority=1
        )
        self.session.add(request)
        self.session.commit()

        created_request = self.session.query(ServiceRequest)\
            .filter_by(client_id=user.id)\
            .first()
        self.assertIsNotNone(created_request)
        self.assertEqual(created_request.status, ServiceStatus.PENDING)
        self.assertEqual(created_request.service_type, ServiceType.MAINTENANCE)

    def test_relationships(self):
        """Probar las relaciones entre modelos"""
        # Crear usuario
        user = User(
            username="testuser",
            email="test@test.com",
            password="testpass",
            role=UserRole.CLIENT,
            company_id=self.company.id
        )
        self.session.add(user)

        # Crear equipo
        equipment = Equipment(
            serial_number="EQUIP001",
            name="Test Equipment",
            model="Test Model",
            company_id=self.company.id
        )
        self.session.add(equipment)

        # Crear solicitud de servicio
        request = ServiceRequest(
            client_id=user.id,
            equipment_id=equipment.id,
            description="Test service request",
            status=ServiceStatus.PENDING,
            service_type=ServiceType.MAINTENANCE,
            priority=1
        )
        self.session.add(request)
        self.session.commit()

        # Verificar relaciones
        user_requests = self.session.query(User)\
            .filter_by(id=user.id)\
            .first()\
            .service_requests
        self.assertEqual(len(user_requests), 1)
        self.assertEqual(user_requests[0].description, "Test service request")

        equipment_requests = self.session.query(Equipment)\
            .filter_by(id=equipment.id)\
            .first()\
            .service_requests
        self.assertEqual(len(equipment_requests), 1)
        self.assertEqual(equipment_requests[0].equipment_id, equipment.id)

    def tearDown(self):
        """Limpiar después de cada prueba"""
        self.session.query(ServiceRequest).delete()
        self.session.query(Equipment).delete()
        self.session.query(User).delete()
        self.session.query(Company).delete()
        self.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Cerrar sesión al terminar"""
        cls.session.close()

if __name__ == '__main__':
    unittest.main()
