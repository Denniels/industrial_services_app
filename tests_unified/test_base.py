# -*- coding: utf-8 -*-
"""
Base para pruebas que requieren acceso a la base de datos
"""
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from database.models import Base

class DatabaseTestCase(unittest.TestCase):
    """Clase base para pruebas que necesitan acceso a la base de datos"""
    
    @classmethod
    def setUpClass(cls):
        """Configurar la base de datos de prueba en memoria"""
        # Usar SQLite en memoria con pooling estático para las pruebas
        cls.engine = create_engine(
            'sqlite:///:memory:',
            connect_args={'check_same_thread': False},
            poolclass=StaticPool,
            echo=False
        )
        # Crear las tablas
        Base.metadata.create_all(cls.engine)
        # Crear la sesión
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session: Session = cls.Session()

    def setUp(self):
        """Limpiar la base de datos antes de cada prueba"""
        for table in reversed(Base.metadata.sorted_tables):
            self.session.execute(table.delete())
        self.session.commit()

    def tearDown(self):
        """Limpiar después de cada prueba"""
        self.session.rollback()
        
    @classmethod
    def tearDownClass(cls):
        """Limpiar al terminar todas las pruebas"""
        cls.session.close()
        Base.metadata.drop_all(cls.engine)
