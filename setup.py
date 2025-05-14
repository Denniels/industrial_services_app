# -*- coding: utf-8 -*-
import subprocess
import sys
import os
from pathlib import Path
import time

def run_command(command, shell=True):
    """Ejecutar un comando y mostrar la salida en tiempo real"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=shell,
        text=True,
        encoding='utf-8'
    )
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    return process.poll()

def check_dependencies():
    """Verificar y instalar dependencias necesarias"""
    print("Verificando dependencias...")
    
    try:
        print("Instalando requisitos...")
        result = run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], shell=False)
        
        if result == 0:
            print("✓ Dependencias instaladas correctamente")
            return True
        else:
            print("Error al instalar dependencias")
            return False
    except Exception as e:
        print(f"Error al instalar dependencias: {e}")
        return False

def setup_database():
    """Configurar la base de datos"""
    print("\nConfigurando la base de datos...")
    try:
        # Verificar y crear la base de datos
        from database.check_connection import check_postgres
        if not check_postgres():
            print("Error al configurar la base de datos")
            return False
            
        # Dar tiempo para que PostgreSQL inicialice la base de datos
        print("Esperando a que la base de datos esté lista...")
        time.sleep(2)
            
        # Crear las tablas iniciales
        print("\nCreando tablas...")
        from database.init_db import init_db
        init_db()
        
        print("✓ Base de datos configurada correctamente")
        return True
    except Exception as e:
        print(f"Error en la configuración de la base de datos: {e}")
        return False

def main():
    print("=== Configuración inicial de Integral Service SPA ===\n")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("requirements.txt"):
        print("Error: Este script debe ejecutarse desde el directorio raíz del proyecto")
        sys.exit(1)
    
    # Ejecutar pasos de configuración
    steps = [
        ("Instalar dependencias", check_dependencies),
        ("Configurar base de datos", setup_database),
    ]
    
    for step_name, step_func in steps:
        print(f"\n=== {step_name} ===")
        if not step_func():
            print(f"\nError en el paso: {step_name}")
            print("Por favor, corrija los errores y vuelva a ejecutar el script")
            sys.exit(1)
    
    print("\n=== Configuración completada exitosamente ===")
    print("\nAhora puede ejecutar la aplicación con:")
    print("streamlit run main.py")

if __name__ == "__main__":
    main()
