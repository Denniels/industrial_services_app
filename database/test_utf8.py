import unittest
from database.models import init_database, Company, ServiceType, User, UserRole
from sqlalchemy.orm import Session
from datetime import datetime

class TestUTF8Encoding(unittest.TestCase):
    def setUp(self):
        self.session = init_database()
        
    def test_company_special_chars(self):
        # Prueba con caracteres especiales en el nombre
        company = Company(
            name="Compañía de Señales & Electrónica",
            rut="76.543.210-K",
            address="Avenida José María Pérez N°123",
            city="Viña del Mar",
            region="Valparaíso"
        )
        self.session.add(company)
        self.session.commit()
        
        # Verificar recuperación
        saved_company = self.session.query(Company).filter_by(rut="76.543.210-K").first()
        self.assertEqual(saved_company.name, "Compañía de Señales & Electrónica")
        
    def test_service_type_special_chars(self):
        # Verificar enumeración con caracteres especiales
        self.assertEqual(ServiceType.AUTOMATION.value, "Automatización")
        self.assertEqual(ServiceType.ELECTROMECHANICAL.value, "Electromecánica")
        
    def test_user_special_chars(self):
        # Prueba con usuario que tiene caracteres especiales
        user = User(
            username="josé.garcía",
            email="josé.garcía@ejemplo.com",
            password="contraseña123",
            role=UserRole.TECHNICIAN,
            first_name="José",
            last_name="García"
        )
        self.session.add(user)
        self.session.commit()
        
        # Verificar recuperación
        saved_user = self.session.query(User).filter_by(username="josé.garcía").first()
        self.assertEqual(saved_user.first_name, "José")
        
    def tearDown(self):
        # Limpiar datos de prueba
        self.session.rollback()
        self.session.close()

if __name__ == '__main__':
    unittest.main()
