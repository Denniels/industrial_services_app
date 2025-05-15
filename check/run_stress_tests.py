# -*- coding: utf-8 -*-
"""
Script para ejecutar pruebas de carga y estrés del sistema
"""

import os
import sys
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from database.config import get_session
from database.models import (
    User, Company, Equipment, ServiceRequest,
    UserRole, ServiceType, ServiceStatus,
    MonitoringDevice, MonitoredVariable, VariableReading
)
from datetime import datetime, timedelta
import random

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='logs/stress_test.log'
)
logger = logging.getLogger(__name__)

class StressTest:
    def __init__(self):
        self.session = get_session()
        self.start_time = None
        self.end_time = None
        self.results = {
            'users_created': 0,
            'companies_created': 0,
            'devices_created': 0,
            'variables_created': 0,
            'readings_created': 0,
            'service_requests_created': 0,
            'errors': []
        }

    def create_test_data(self, num_companies=10, users_per_company=5):
        """Crear datos de prueba"""
        try:
            for i in range(num_companies):
                # Crear compañía
                company = Company(
                    name=f"Test Company {i}",
                    rut=f"76.{i:03d}.{i:03d}-{i%9}",
                    address=f"Address {i}",
                    city=f"City {i}",
                    region=f"Region {i}"
                )
                self.session.add(company)
                self.results['companies_created'] += 1

                # Crear usuarios para la compañía
                for j in range(users_per_company):
                    user = User(
                        username=f"user{i}_{j}",
                        email=f"user{i}_{j}@test.com",
                        password="testpass",
                        role=random.choice(list(UserRole)),
                        company_id=company.id,
                        first_name=f"User {j}",
                        last_name=f"Company {i}"
                    )
                    self.session.add(user)
                    self.results['users_created'] += 1

                self.session.commit()

        except Exception as e:
            self.results['errors'].append(f"Error creando datos base: {str(e)}")
            self.session.rollback()

    def simulate_device_readings(self, num_devices=100, readings_per_device=1000):
        """Simular lecturas de dispositivos"""
        try:
            # Obtener usuarios tipo cliente
            clients = self.session.query(User)\
                .filter(User.role == UserRole.CLIENT)\
                .all()

            if not clients:
                return

            for i in range(num_devices):
                # Crear dispositivo
                device = MonitoringDevice(
                    client_id=random.choice(clients).id,
                    device_serial=f"DEV{i:05d}",
                    device_type="SENSOR",
                    is_active=True
                )
                self.session.add(device)
                self.results['devices_created'] += 1

                # Crear variables para el dispositivo
                num_vars = random.randint(1, 5)
                variables = []
                for j in range(num_vars):
                    variable = MonitoredVariable(
                        device_id=device.id,
                        name=f"Var{j}",
                        description=f"Variable {j} of device {i}",
                        unit=random.choice(["°C", "PSI", "kPa", "RPM"]),
                        min_value=0,
                        max_value=100
                    )
                    self.session.add(variable)
                    variables.append(variable)
                    self.results['variables_created'] += 1
                
                device.variables_count = len(variables)
                self.session.commit()

                # Generar lecturas
                base_time = datetime.now() - timedelta(days=30)
                for v in variables:
                    readings = []
                    for k in range(readings_per_device):
                        value = random.uniform(v.min_value or 0, v.max_value or 100)
                        timestamp = base_time + timedelta(
                            minutes=random.randint(0, 43200)
                        )
                        reading = VariableReading(
                            variable_id=v.id,
                            value=value,
                            timestamp=timestamp,
                            quality=random.randint(0, 100)
                        )
                        readings.append(reading)
                        self.results['readings_created'] += 1

                    self.session.bulk_save_objects(readings)
                
                if i % 10 == 0:  # Commit cada 10 dispositivos
                    self.session.commit()
                    logger.info(f"Procesados {i+1} dispositivos")

            self.session.commit()

        except Exception as e:
            self.results['errors'].append(f"Error simulando lecturas: {str(e)}")
            self.session.rollback()

    def simulate_service_requests(self, num_requests=1000):
        """Simular solicitudes de servicio"""
        try:
            clients = self.session.query(User)\
                .filter(User.role == UserRole.CLIENT)\
                .all()
            technicians = self.session.query(User)\
                .filter(User.role == UserRole.TECHNICIAN)\
                .all()
            equipment = self.session.query(Equipment).all()

            if not clients or not technicians:
                return

            # Crear solicitudes en paralelo
            def create_request(i):
                try:
                    client = random.choice(clients)
                    request = ServiceRequest(
                        client_id=client.id,
                        assigned_technician_id=random.choice(technicians).id if random.random() > 0.3 else None,
                        equipment_id=random.choice(equipment).id if equipment and random.random() > 0.5 else None,
                        service_type=random.choice(list(ServiceType)),
                        description=f"Test request {i}",
                        status=random.choice(list(ServiceStatus)),
                        priority=random.randint(1, 3),
                        requested_date=datetime.now() - timedelta(days=random.randint(0, 30))
                    )
                    return request
                except Exception as e:
                    self.results['errors'].append(f"Error creando solicitud {i}: {str(e)}")
                    return None

            with ThreadPoolExecutor(max_workers=10) as executor:
                requests = list(executor.map(create_request, range(num_requests)))
                requests = [r for r in requests if r is not None]
                self.session.bulk_save_objects(requests)
                self.session.commit()
                self.results['service_requests_created'] = len(requests)

        except Exception as e:
            self.results['errors'].append(f"Error simulando solicitudes: {str(e)}")
            self.session.rollback()

    def run(self):
        """Ejecutar todas las pruebas de estrés"""
        self.start_time = datetime.now()
        logger.info("Iniciando pruebas de estrés...")

        # Crear datos base
        logger.info("Creando datos de prueba...")
        self.create_test_data()

        # Simular lecturas de dispositivos
        logger.info("Simulando lecturas de dispositivos...")
        self.simulate_device_readings()

        # Simular solicitudes de servicio
        logger.info("Simulando solicitudes de servicio...")
        self.simulate_service_requests()

        self.end_time = datetime.now()
        logger.info("Pruebas de estrés completadas")

    def generate_report(self):
        """Generar reporte de las pruebas"""
        duration = (self.end_time - self.start_time).total_seconds()
        
        report = f"""# Reporte de Pruebas de Estrés

## Resumen
- **Fecha de Ejecución**: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}
- **Duración Total**: {duration:.2f} segundos

## Datos Generados
- **Compañías**: {self.results['companies_created']}
- **Usuarios**: {self.results['users_created']}
- **Dispositivos**: {self.results['devices_created']}
- **Variables**: {self.results['variables_created']}
- **Lecturas**: {self.results['readings_created']}
- **Solicitudes de Servicio**: {self.results['service_requests_created']}

## Rendimiento
- **Lecturas por segundo**: {self.results['readings_created']/duration:.2f}
- **Solicitudes por segundo**: {self.results['service_requests_created']/duration:.2f}

## Errores
"""
        if not self.results['errors']:
            report += "No se encontraron errores\n"
        else:
            for error in self.results['errors']:
                report += f"- {error}\n"

        # Guardar reporte
        report_path = os.path.join('check', 'stress_test_report.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return report_path

def main():
    """Función principal"""
    try:
        stress_test = StressTest()
        stress_test.run()
        report_path = stress_test.generate_report()
        print(f"\nReporte generado en: {os.path.abspath(report_path)}")
        
    except Exception as e:
        logger.error(f"Error ejecutando pruebas de estrés: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
