# Manual de Presupuestos y Facturación

## 1. Estructura de Costos

### 1.1 Costos Directos
- **Mano de Obra**
  - Hora técnico: Según categoría
  - Hora ingeniero: Según especialidad
  - Horas extra: Recargo del 50%
  - Trabajo nocturno: Recargo del 75%

- **Materiales y Repuestos**
  - Costo de adquisición
  - Gastos de importación si aplica
  - Almacenamiento y manejo
  - Margen de comercialización

### 1.2 Costos Indirectos
- **Operacionales**
  - Transporte y viáticos
  - Herramientas y equipos
  - Seguros y garantías
  - Gastos administrativos

- **Overhead**
  - Gastos generales: 15%
  - Utilidad: 25%
  - IVA: 19%
  - Otros impuestos aplicables

## 2. Tipos de Presupuesto

### 2.1 Servicio Spot
```python
Presupuesto = (Horas × Tarifa) + Materiales + Viáticos
Costos_Operacionales = Subtotal × % Operacional
Utilidad = (Subtotal + Costos_Operacionales) × % Utilidad
IVA = (Subtotal + Costos_Operacionales + Utilidad) × 0.19
```

### 2.2 Contrato de Mantenimiento
```python
Valor_Mensual = Visitas_Programadas + Soporte_Técnico + Materiales_Estimados
Descuento = Valor_Mensual × % Descuento_Contrato
Total_Mensual = (Valor_Mensual - Descuento) × (1 + IVA)
```

## 3. Proceso de Presupuestación

### 3.1 Evaluación Inicial
1. Visita técnica si es necesario
2. Diagnóstico del problema/necesidad
3. Estimación de recursos necesarios
4. Consulta de precios actualizados

### 3.2 Elaboración
1. Calcular horas requeridas
2. Listar materiales necesarios
3. Incluir costos adicionales
4. Aplicar márgenes correspondientes

### 3.3 Revisión y Aprobación
1. Verificación técnica
2. Validación de precios
3. Aprobación de supervisor
4. Envío al cliente

## 4. Facturación

### 4.1 Tipos de Factura
- **Servicios Spot**
  - Por trabajo realizado
  - Incluye desglose detallado
  - Adjunta informe técnico
  - Forma de pago acordada

- **Contratos**
  - Facturación mensual
  - Incluye servicios del período
  - Materiales adicionales
  - Servicios extra realizados

### 4.2 Proceso de Facturación
1. Verificar servicio completado
2. Confirmar aprobación del cliente
3. Generar factura según presupuesto
4. Adjuntar documentación requerida

## 5. Condiciones Comerciales

### 5.1 Formas de Pago
- Contado
- 30 días
- 45 días (clientes preferentes)
- Según contrato

### 5.2 Descuentos
- **Por Volumen**
  - 5% > $1.000.000
  - 10% > $5.000.000
  - 15% > $10.000.000

- **Por Contrato**
  - Básico: 10%
  - Premium: 15%
  - Personalizado: Según negociación

## 6. Control y Seguimiento

### 6.1 KPIs
- Margen bruto por servicio
- Costo operacional real vs presupuestado
- Tiempo facturado vs tiempo real
- Eficiencia en cobranza

### 6.2 Reportes
- Servicios facturados
- Pagos pendientes
- Análisis de rentabilidad
- Proyección de ingresos

## 7. Políticas Especiales

### 7.1 Garantías
- Cobertura de la garantía
- Exclusiones
- Proceso de reclamo
- Costos cubiertos

### 7.2 Modificaciones
- Cambios de alcance
- Trabajos adicionales
- Imprevistos
- Autorizaciones requeridas
