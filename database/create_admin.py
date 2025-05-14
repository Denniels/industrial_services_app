# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
import psycopg2
from werkzeug.security import generate_password_hash
from database.config import DATABASE_CONFIG

def create_admin_user():
    """Crear usuario administrador por defecto"""
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            dbname=DATABASE_CONFIG['database'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            host=DATABASE_CONFIG['host'],
            port=DATABASE_CONFIG['port']
        )
        cur = conn.cursor()
        
        # Verificar si ya existe un admin
        cur.execute("SELECT id FROM users WHERE role = 'admin'")
        admin = cur.fetchone()
        
        if not admin:
            # Crear usuario admin
            admin_data = {
                'username': 'admin',
                'email': 'admin@integralservice.cl',
                'password': generate_password_hash('IntegralService2024!'),
                'role': 'admin',
                'is_active': True,
                'first_name': 'Administrador',
                'last_name': 'Sistema'
            }
            
            cur.execute("""
                INSERT INTO users (username, email, password, role, is_active, first_name, last_name)
                VALUES (%(username)s, %(email)s, %(password)s, %(role)s, %(is_active)s, %(first_name)s, %(last_name)s)
            """, admin_data)
            
            conn.commit()
            print("Usuario administrador creado exitosamente")
            print("\nCredenciales de administrador:")
            print("-------------------------------")
            print("Usuario: admin")
            print("Contraseña: IntegralService2024!")
            print("\nPor favor, cambie la contraseña después del primer inicio de sesión.")
        else:
            print("Ya existe un usuario administrador")
            
    except Exception as e:
        print(f"Error al crear el usuario administrador: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_admin_user()
