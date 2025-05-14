# -*- coding: utf-8 -*-
"""
Script para verificar y corregir la codificación de archivos en el proyecto
"""

import os
import chardet
import logging
from pathlib import Path
import shutil
import sys

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/encoding_check.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EncodingChecker:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.extensions = ['.py', '.sql', '.md', '.txt']
        self.files_checked = 0
        self.files_fixed = 0
        self.errors = []

    def should_check_file(self, file_path: Path) -> bool:
        """Determinar si un archivo debe ser verificado."""
        return (
            file_path.suffix in self.extensions and
            not any(part.startswith('.') for part in file_path.parts) and
            'venv' not in file_path.parts and
            '__pycache__' not in file_path.parts
        )

    def detect_encoding(self, file_path: Path) -> dict:
        """Detectar la codificación de un archivo."""
        try:
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                return {
                    'encoding': result['encoding'],
                    'confidence': result['confidence'],
                    'raw_data': raw_data
                }
        except Exception as e:
            logger.error(f"Error al detectar codificación de {file_path}: {str(e)}")
            return None

    def has_coding_declaration(self, content: str) -> bool:
        """Verificar si un archivo Python tiene declaración de codificación."""
        first_lines = content.split('\n')[:2]
        return any('coding' in line and 'utf-8' in line.lower() for line in first_lines)

    def add_coding_declaration(self, content: str) -> str:
        """Agregar declaración de codificación a un archivo Python."""
        if content.startswith('#!'):
            # Si tiene shebang, insertar después
            lines = content.split('\n')
            return lines[0] + '\n# -*- coding: utf-8 -*-\n' + '\n'.join(lines[1:])
        return '# -*- coding: utf-8 -*-\n' + content

    def fix_file_encoding(self, file_path: Path, detection_result: dict) -> bool:
        """Corregir la codificación de un archivo a UTF-8."""
        try:
            # Crear backup
            backup_path = file_path.with_suffix(file_path.suffix + '.bak')
            shutil.copy2(file_path, backup_path)

            # Leer contenido
            content = detection_result['raw_data'].decode(detection_result['encoding'])

            # Para archivos Python, verificar/agregar declaración de codificación
            if file_path.suffix == '.py' and not self.has_coding_declaration(content):
                content = self.add_coding_declaration(content)

            # Escribir con UTF-8
            with open(file_path, 'w', encoding='utf-8', newline='') as file:
                file.write(content)

            # Si todo salió bien, eliminar backup
            backup_path.unlink()
            return True

        except Exception as e:
            logger.error(f"Error al corregir {file_path}: {str(e)}")
            # Restaurar backup si existe
            if backup_path.exists():
                shutil.move(str(backup_path), str(file_path))
            return False

    def check_and_fix_encoding(self):
        """Verificar y corregir la codificación de todos los archivos relevantes."""
        logger.info("🔍 Iniciando verificación de codificación de archivos...")

        for file_path in self.project_root.rglob('*'):
            if not self.should_check_file(file_path):
                continue

            self.files_checked += 1
            logger.info(f"Verificando: {file_path.relative_to(self.project_root)}")

            detection_result = self.detect_encoding(file_path)
            if not detection_result:
                continue

            if detection_result['encoding'] != 'utf-8':
                logger.warning(f"⚠️ Archivo no UTF-8 detectado: {file_path}")
                logger.warning(f"   Codificación actual: {detection_result['encoding']}")
                logger.warning(f"   Confianza: {detection_result['confidence']}")

                if self.fix_file_encoding(file_path, detection_result):
                    self.files_fixed += 1
                    logger.info(f"✅ Archivo convertido a UTF-8: {file_path}")
                else:
                    self.errors.append(str(file_path))

        # Resumen
        logger.info("\n=== Resumen de la verificación ===")
        logger.info(f"Archivos verificados: {self.files_checked}")
        logger.info(f"Archivos corregidos: {self.files_fixed}")
        logger.info(f"Errores encontrados: {len(self.errors)}")

        if self.errors:
            logger.error("\nArchivos con errores:")
            for error in self.errors:
                logger.error(f"❌ {error}")

if __name__ == "__main__":
    checker = EncodingChecker()
    checker.check_and_fix_encoding()
    sys.exit(len(checker.errors))
