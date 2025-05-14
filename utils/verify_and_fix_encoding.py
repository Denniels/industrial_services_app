# -*- coding: utf-8 -*-
import os
import chardet
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='logs/encoding_fix.log',
    encoding='utf-8'
)

logger = logging.getLogger(__name__)

def detect_file_encoding(file_path):
    """Detecta la codificación de un archivo"""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def convert_file_to_utf8(file_path):
    """Convierte un archivo a UTF-8 si es necesario"""
    try:
        # Detectar codificación actual
        current_encoding = detect_file_encoding(file_path)
        
        if current_encoding and current_encoding.lower() != 'utf-8':
            # Leer el contenido con la codificación detectada
            with open(file_path, 'r', encoding=current_encoding, errors='replace') as file:
                content = file.read()
            
            # Escribir el contenido en UTF-8
            with open(file_path, 'w', encoding='utf-8', newline='') as file:
                file.write(content)
            
            logger.info(f"Convertido {file_path} de {current_encoding} a UTF-8")
            return True
        return False
    except Exception as e:
        logger.error(f"Error al procesar {file_path}: {str(e)}")
        return False

def fix_project_encoding():
    """Corrige la codificación de todos los archivos relevantes del proyecto"""
    base_dir = Path(__file__).parent.parent
    extensions = {'.py', '.sql', '.md', '.txt', '.env'}
    
    for ext in extensions:
        for file_path in base_dir.rglob(f'*{ext}'):
            if convert_file_to_utf8(str(file_path)):
                print(f"Convertido: {file_path}")

if __name__ == '__main__':
    # Asegurarse de que el directorio de logs existe
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    print("Iniciando corrección de codificación...")
    fix_project_encoding()
    print("Proceso completado. Revisa logs/encoding_fix.log para más detalles")
