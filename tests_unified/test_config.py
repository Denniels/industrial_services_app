# -*- coding: utf-8 -*-
"""Pruebas para la configuración de la base de datos"""
import unittest
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session
from database.config import get_session, DATABASE_CONFIG
from .test_base import DatabaseTestCase

class TestConfiguration(DatabaseTestCase):
    """Pruebas de configuración de la base de datos"""
    
    def test_database_config(self):
        """Probar la configuración de la base de datos"""
        required_keys = ["host", "database", "user", "password", "port"]
        for key in required_keys:
            self.assertIn(key, DATABASE_CONFIG)
            self.assertIsNotNone(DATABASE_CONFIG[key])

    def test_database_connection(self):
        """Probar la conexión a la base de datos"""
        with get_session() as session:
            self.assertIsNotNone(session)
            # Verificar que podemos ejecutar una consulta simple
            result = session.execute(text("SELECT 1")).scalar()
            self.assertEqual(result, 1)

    def test_encoding_config(self):
        """Probar la configuración de codificación"""
        self.assertEqual(DATABASE_CONFIG.get("client_encoding", "utf8"), "utf8")
        
        # Probar caracteres especiales
        special_chars = "áéíóúñÁÉÍÓÚÑüÜ"
        
        # Crear tabla temporal
        self.session.execute(text("""
            CREATE TABLE IF NOT EXISTS test_encoding (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL
            )
        """))
        
        # Insertar y leer caracteres especiales
        self.session.execute(
            text("INSERT INTO test_encoding (id, content) VALUES (:id, :content)"),
            {"id": 1, "content": special_chars}
        )
        self.session.commit()
        
        # Verificar el contenido
        result = self.session.execute(
            text("SELECT content FROM test_encoding WHERE id = :id"),
            {"id": 1}
        ).scalar()
        self.assertEqual(result, special_chars)

    def test_session_management(self):
        """Probar el manejo de sesiones"""
        session1: Session = get_session()
        session2: Session = get_session()
        
        try:
            # Verificar que son sesiones diferentes
            self.assertIsNot(session1, session2)
            
            # Verificar que ambas sesiones funcionan
            result1 = session1.execute(text("SELECT 1")).scalar()
            result2 = session2.execute(text("SELECT 2")).scalar()
            
            self.assertEqual(result1, 1)
            self.assertEqual(result2, 2)
            
        finally:
            session1.close()
            session2.close()

if __name__ == "__main__":
    unittest.main()
