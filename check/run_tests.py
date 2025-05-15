# -*- coding: utf-8 -*-
"""
Script para ejecutar todas las pruebas unitarias
"""

import os
import sys
import logging
import unittest
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agregar el directorio actual al path de Python
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def generate_report(results, duration, report_path):
    """
    Generar un reporte markdown con los resultados de las pruebas
    """
    now = datetime.now()
    
    md = f"""# Reporte de Pruebas

## Resumen
- **Fecha de Ejecución**: {now.strftime('%Y-%m-%d %H:%M:%S')}
- **Duración Total**: {duration:.2f} segundos
- **Tests Ejecutados**: {results.testsRun}
- **Tests Exitosos**: {results.testsRun - len(results.failures) - len(results.errors) - len(results.skipped)}
- **Tests Fallidos**: {len(results.failures)}
- **Errores**: {len(results.errors)}
- **Tests Saltados**: {len(results.skipped)}

## Detalles

### Tests Exitosos ✅
"""
    
    if results.wasSuccessful():
        md += "Todos los tests pasaron exitosamente\n"
    
    if results.failures:
        md += "\n### Tests Fallidos ❌\n"
        for test, error in results.failures:
            md += f"- {test}\n  ```\n  {error}\n  ```\n"
    
    if results.errors:
        md += "\n### Errores 🔴\n"
        for test, error in results.errors:
            md += f"- {test}\n  ```\n  {error}\n  ```\n"
            
    if results.skipped:
        md += "\n### Tests Saltados ⚠️\n"
        for test, reason in results.skipped:
            md += f"- {test}\n  ```\n  {reason}\n  ```\n"

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(md)

def run_all_tests():
    """
    Ejecutar todas las pruebas y generar reporte
    """
    start_time = datetime.now()
    
    print(f"Directorio actual: {current_dir}")
    print(f"Directorio raíz del proyecto: {project_root}")
    
    # Crear directorio de tests si no existe
    tests_dir = os.path.join(project_root, 'tests')
    if not os.path.exists(tests_dir):
        os.makedirs(tests_dir)
    print(f"Directorio de tests: {tests_dir}")
    
    # Descubrir tests
    loader = unittest.TestLoader()
    suite = loader.discover(tests_dir, pattern='test_*.py')
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generar reporte
    duration = (datetime.now() - start_time).total_seconds()
    report_path = os.path.join(current_dir, 'test_report.md')
    generate_report(result, duration, report_path)
    
    print(f"\nReporte generado en: {os.path.abspath(report_path)}")
    
    # Retornar éxito/fallo
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
