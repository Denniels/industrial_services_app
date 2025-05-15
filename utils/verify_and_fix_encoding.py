# -*- coding: utf-8 -*-

import os

import chardet

import logging

from pathlib import Path



# Configurar logging

logging.basicConfig(

    level=logging.DEBUG,

    format='%(asctime)s - %(levelname)s - %(message)s',

    filename='logs/encoding_fix.log',

    encoding='utf-8'

)

logger = logging.getLogger(__name__)



def verify_and_fix_file(file_path):

    """Verifica y corrige la codificaci√≥n de un archivo a UTF-8"""

    try:

        # Leer el contenido del archivo en modo binario

        with open(file_path, 'rb') as file:

            content = file.read()

            

        # Detectar la codificaci√≥n actual

        result = chardet.detect(content)

        encoding = result['encoding']

        confidence = result['confidence']

        

        logger.info(f"Verificando: {os.path.basename(file_path)}")

        logger.info(f"Codificaci√≥n detectada: {encoding} (confianza: {confidence})")

        

        if encoding and encoding.lower() != 'utf-8':

            # Decodificar contenido con la codificaci√≥n detectada

            try:

                decoded_content = content.decode(encoding)

                # Escribir contenido en UTF-8

                with open(file_path, 'w', encoding='utf-8') as file:

                    file.write(decoded_content)

                logger.info(f"‚úÖ Archivo convertido a UTF-8: {file_path}")

                return True

            except Exception as e:

                logger.error(f"Error al convertir {file_path}: {str(e)}")

                return False

        else:

            logger.info(f"‚úÖ Archivo ya est√° en UTF-8: {file_path}")

            return True

            

    except Exception as e:

        logger.error(f"Error procesando {file_path}: {str(e)}")

        return False



def fix_all_files(directory):

    """Corrige la codificaci√≥n de todos los archivos Python en el directorio"""

    python_files = []

    errors = []

    fixed = []

    

    # Buscar todos los archivos Python

    for root, _, files in os.walk(directory):

        for file in files:

            if file.endswith('.py'):

                file_path = os.path.join(root, file)

                python_files.append(file_path)

    

    logger.info(f"üîç Encontrados {len(python_files)} archivos Python")

    

    # Procesar cada archivo

    for file_path in python_files:

        try:

            if verify_and_fix_file(file_path):

                fixed.append(file_path)

            else:

                errors.append(file_path)

        except Exception as e:

            logger.error(f"Error procesando {file_path}: {str(e)}")

            errors.append(file_path)

    

    # Resumen

    logger.info("\n=== Resumen de la correcci√≥n ===")

    logger.info(f"Total de archivos: {len(python_files)}")

    logger.info(f"Archivos corregidos: {len(fixed)}")

    logger.info(f"Errores: {len(errors)}")

    

    if errors:

        logger.error("\nArchivos con errores:")

        for error_file in errors:

            logger.error(f"‚ùå {error_file}")

    

    return len(errors) == 0



if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print("üîç Iniciando verificaci√≥n y correcci√≥n de codificaci√≥n...")

    success = fix_all_files(base_dir)

    if success:

        print("‚úÖ Todos los archivos fueron procesados correctamente")

    else:

        print("‚ö†Ô∏è Algunos archivos no pudieron ser procesados. Revise logs/encoding_fix.log")

