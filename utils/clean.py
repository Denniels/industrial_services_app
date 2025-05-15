# -*- coding: utf-8 -*-
"""
Script para limpiar archivos compilados y temporales
"""

import os
import shutil

def clean_pyc_files():
    """Eliminar archivos .pyc y directorios __pycache__"""
    # Obtener el directorio raíz del proyecto
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("Limpiando archivos compilados y temporales...")
    
    # Caminar por todos los directorios
    for root, dirs, files in os.walk(current_dir):
        # Eliminar directorios __pycache__
        if '__pycache__' in dirs:
            pycache_dir = os.path.join(root, '__pycache__')
            print(f"Eliminando {pycache_dir}")
            shutil.rmtree(pycache_dir)
        
        # Eliminar archivos .pyc
        for file in files:
            if file.endswith('.pyc'):
                pyc_file = os.path.join(root, file)
                print(f"Eliminando {pyc_file}")
                os.remove(pyc_file)

def clean_coverage_files():
    """Eliminar archivos de cobertura de código"""
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    files_to_remove = [
        '.coverage',
        'coverage.xml',
        'coverage.json'
    ]
    
    dirs_to_remove = [
        'htmlcov',
        '.pytest_cache'
    ]
    
    for file in files_to_remove:
        file_path = os.path.join(current_dir, file)
        if os.path.exists(file_path):
            print(f"Eliminando {file_path}")
            os.remove(file_path)
    
    for dir_name in dirs_to_remove:
        dir_path = os.path.join(current_dir, dir_name)
        if os.path.exists(dir_path):
            print(f"Eliminando {dir_path}")
            shutil.rmtree(dir_path)

if __name__ == '__main__':
    clean_pyc_files()
    clean_coverage_files()
    print("\nLimpieza completada.")
