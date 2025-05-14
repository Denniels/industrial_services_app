from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
from datetime import datetime
from config import COMPANY_NAME, LOGO_PATH

class ReportGenerator:
    def __init__(self, output_path):
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self.width, self.height = letter
    
    def generate_technical_report(self, report, service, client, technician):
        """Genera un PDF del informe técnico"""
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Contenedor para elementos del PDF
        elements = []
        
        # Agregar encabezado
        self._add_header(elements)
        
        # Información del servicio
        self._add_service_info(elements, service, client)
        
        # Detalles técnicos
        self._add_technical_details(elements, report)
        
        # Materiales y repuestos
        self._add_materials_section(elements, report)
        
        # Tiempos y costos
        self._add_time_and_cost(elements, report)
        
        # Firmas
        self._add_signatures(elements, report, technician)
        
        # Generar PDF
        doc.build(elements)
    
    def _add_header(self, elements):
        """Agrega el encabezado del documento"""
        # Logo si existe
        if os.path.exists(LOGO_PATH):
            img = Image(LOGO_PATH, width=2*inch, height=1*inch)
            elements.append(img)
        
        # Título del informe
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            alignment=1,
            spaceAfter=30
        )
        elements.append(Paragraph(f"Informe Técnico - {COMPANY_NAME}", title_style))
        elements.append(Spacer(1, 12))
    
    def _add_service_info(self, elements, service, client):
        """Agrega la información del servicio y cliente"""
        data = [
            ["Cliente:", client.business_name],
            ["RUT:", client.rut],
            ["Fecha:", datetime.now().strftime("%d/%m/%Y")],
            ["Tipo de Servicio:", service.service_type.value],
            ["N° de Servicio:", str(service.id)]
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
    
    def _add_technical_details(self, elements, report):
        """Agrega los detalles técnicos del servicio"""
        elements.append(Paragraph("Detalles Técnicos", self.styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        # Diagnóstico
        elements.append(Paragraph("Diagnóstico:", self.styles['Heading3']))
        elements.append(Paragraph(report.diagnosis, self.styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Trabajo realizado
        elements.append(Paragraph("Trabajo Realizado:", self.styles['Heading3']))
        elements.append(Paragraph(report.work_performed, self.styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Recomendaciones
        elements.append(Paragraph("Recomendaciones:", self.styles['Heading3']))
        elements.append(Paragraph(report.recommendations, self.styles['Normal']))
        elements.append(Spacer(1, 20))
    
    def _add_materials_section(self, elements, report):
        """Agrega la sección de materiales y repuestos"""
        elements.append(Paragraph("Materiales y Repuestos", self.styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        if report.materials:
            data = [["Material", "Cantidad", "Unidad", "Costo"]]
            for material in report.materials:
                data.append([
                    material.material.name,
                    str(material.quantity),
                    material.material.unit,
                    f"${material.total_price:,.2f}"
                ])
            
            table = Table(data, colWidths=[3*inch, 1*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph("No se utilizaron materiales", self.styles['Normal']))
        
        elements.append(Spacer(1, 20))
    
    def _add_time_and_cost(self, elements, report):
        """Agrega la sección de tiempos y costos"""
        elements.append(Paragraph("Tiempos y Costos", self.styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        data = [
            ["Hora de Inicio:", report.start_time.strftime("%H:%M")],
            ["Hora de Fin:", report.end_time.strftime("%H:%M")],
            ["Horas Trabajadas:", f"{report.hours_worked:.2f}"],
            ["Tiempo de Viaje:", f"{report.travel_time:.2f} horas"],
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
    
    def _add_signatures(self, elements, report, technician):
        """Agrega la sección de firmas"""
        elements.append(Paragraph("Firmas", self.styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        # Si hay firmas digitales, agregarlas como imágenes
        if report.signature_client:
            elements.append(Image(report.signature_client, width=2*inch, height=1*inch))
        if report.signature_technician:
            elements.append(Image(report.signature_technician, width=2*inch, height=1*inch))
        
        # Líneas para firmas manuales
        data = [
            ["_"*30, "_"*30],
            ["Técnico", "Cliente"],
            [f"{technician.first_name} {technician.last_name}", ""],
        ]
        
        table = Table(data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(table)
