# -*- coding: utf-8 -*-
import os
import shutil

def clean_pyc_files():
    """Eliminar archivos .pyc y directorios __pycache__"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
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

if __name__ == '__main__':
    clean_pyc_files()
    print("\nLimpieza completada.")
