# -*- coding: utf-8 -*-
"""Pruebas para el módulo de autenticación"""
from sqlalchemy import text
from database.models import User, UserRole
from auth.login import authenticate_user, create_user, validate_password
from .test_base import DatabaseTestCase

class TestAuthentication(DatabaseTestCase):
    """Pruebas para la autenticación de usuarios"""

    def setUp(self):
        """Preparar datos de prueba"""
        super().setUp()
        self.test_password = "Test@Password123"
        self.user = create_user(
            session=self.session,
            username="testuser",
            email="test@test.com",
            password=self.test_password,
            role=UserRole.CLIENT
        )
        self.session.commit()

    def test_user_creation(self):
        """Probar la creación de usuarios"""
        # Verificar que el usuario existe
        user = self.session.execute(
            text("SELECT * FROM user_account WHERE username = :username"),
            {"username": "testuser"}
        ).fetchone()
        
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.role, UserRole.CLIENT)

    def test_password_validation(self):
        """Probar la validación de contraseñas"""
        # Probar contraseña válida
        self.assertTrue(validate_password(self.test_password))
        
        # Probar contraseñas inválidas
        invalid_passwords = [
            "short",           # Muy corta
            "nouppercase123",  # Sin mayúsculas
            "NOLOWERCASE123",  # Sin minúsculas
            "NoNumbers!",      # Sin números
            "no spaces",       # Con espacios
            "ñóáéí123A"       # Caracteres especiales no permitidos
        ]
        
        for password in invalid_passwords:
            self.assertFalse(
                validate_password(password), 
                f"La contraseña '{password}' debería ser inválida"
            )

    def test_authentication(self):
        """Probar el proceso de autenticación"""
        # Autenticación exitosa
        user = authenticate_user(
            session=self.session,
            username="testuser",
            password=self.test_password
        )
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")
        
        # Autenticación fallida - contraseña incorrecta
        user = authenticate_user(
            session=self.session,
            username="testuser",
            password="wrong_password"
        )
        self.assertIsNone(user)
        
        # Autenticación fallida - usuario no existe
        user = authenticate_user(
            session=self.session,
            username="nonexistent",
            password=self.test_password
        )
        self.assertIsNone(user)

    def test_password_hashing(self):
        """Probar el hash de contraseñas"""
        # Verificar que la contraseña está hasheada en la base de datos
        hashed_password = self.session.execute(
            text("SELECT password FROM user_account WHERE username = :username"),
            {"username": "testuser"}
        ).scalar()
        
        # La contraseña no debe estar en texto plano
        self.assertNotEqual(hashed_password, self.test_password)
        self.assertTrue(len(hashed_password) > 20)  # El hash debe ser suficientemente largo

if __name__ == "__main__":
    unittest.main()
