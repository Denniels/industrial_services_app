# -*- coding: utf-8 -*-
import importlib
import pkg_resources
import sys
import subprocess
import os

# Añadir el directorio raíz al path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def check_python_version():
    """Verificar la versión de Python"""
    print(f"Versión de Python: {sys.version}")
    if sys.version_info < (3, 8):
        print("Se requiere Python 3.8 o superior")
        return False
    return True

def check_package(package_name):
    """Verificar si un paquete está instalado y su versión"""
    try:
        pkg = pkg_resources.working_set.by_key[package_name]
        print(f"✓ {package_name}: {pkg.version}")
        return True
    except KeyError:
        print(f"✗ {package_name} no está instalado")
        return False

def check_dependencies():
    """Verificar todas las dependencias requeridas"""
    required_packages = [
        'sqlalchemy',
        'flask',
        'flask-login',
        'flask-sqlalchemy',
        'flask-jwt-extended',
        'psycopg2-binary',
        'python-dotenv',
        'bcrypt',
        'alembic'
    ]
    
    all_installed = True
    for package in required_packages:
        if not check_package(package):
            all_installed = False
    
    return all_installed

def check_postgresql():
    """Verificar la instalación de PostgreSQL"""
    try:
        import psycopg2
        print("\nVerificando PostgreSQL:")
        
        # Intenta conectar al servidor PostgreSQL
        from database.check_connection import check_postgres
        if check_postgres():
            print("✓ PostgreSQL está configurado correctamente")
            return True
        else:
            print("✗ Error en la configuración de PostgreSQL")
            return False
            
    except ImportError:
        print("✗ psycopg2 no está instalado")
        return False
    except Exception as e:
        print(f"✗ Error al verificar PostgreSQL: {str(e)}")
        return False

def main():
    print("=== Verificación del Sistema ===\n")
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    print("\n=== Verificando Dependencias ===")
    if not check_dependencies():
        print("\nAlgunas dependencias no están instaladas.")
        response = input("¿Desea instalar las dependencias faltantes? (s/n): ")
        if response.lower() == 's':
            setup_path = os.path.join(parent_dir, 'setup', 'setup.py')
            subprocess.run([sys.executable, setup_path, "install"])
        else:
            sys.exit(1)
    
    print("\n=== Verificando Base de Datos ===")
    if not check_postgresql():
        print("\nLa base de datos necesita configuración.")
        print("Por favor, ejecute: python setup/setup.py setup-db")
        sys.exit(1)
    
    print("\n=== Todo está correctamente configurado ===")
    print("\nPuede ejecutar la aplicación con:")
    print("python main.py")

if __name__ == "__main__":
    main()
