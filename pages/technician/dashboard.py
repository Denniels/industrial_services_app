import streamlit as st
from database.config import get_db
from database.models import ServiceRequest, TechnicalReport
from datetime import datetime
from utils.helpers import format_datetime, show_status_badge
import pandas as pd

def technician_dashboard():
    st.header("Panel del Técnico")
    
    db = next(get_db())
    technician_id = st.session_state.user["id"]
    
    # Tabs para diferentes vistas
    tab1, tab2 = st.tabs(["Servicios Asignados", "Informes Técnicos"])
    
    with tab1:
        show_assigned_services(db, technician_id)
    
    with tab2:
        show_technical_reports(db, technician_id)

def show_assigned_services(db, technician_id):
    st.subheader("Servicios Asignados")
    
    # Obtener servicios asignados
    services = db.query(ServiceRequest).filter(
        ServiceRequest.technician_id == technician_id,
        ServiceRequest.status.in_(['PENDING', 'IN_PROGRESS'])
    ).all()
    
    if not services:
        st.info("No hay servicios asignados actualmente")
        return
    
    # Convertir a DataFrame para mejor visualización
    services_data = []
    for service in services:
        services_data.append({
            "ID": service.id,
            "Cliente": service.client.name,
            "Tipo": service.service_type,
            "Estado": show_status_badge(service.status),
            "Fecha Programada": format_datetime(service.scheduled_date),
            "Descripción": service.description
        })
    
    df = pd.DataFrame(services_data)
    st.write(df.to_html(escape=False), unsafe_allow_html=True)
    
    # Formulario para actualizar estado
    with st.expander("Actualizar Estado de Servicio"):
        update_service_status(db, services)

def update_service_status(db, services):
    with st.form("update_status_form"):
        service_id = st.selectbox(
            "Seleccionar Servicio",
            options=[s.id for s in services],
            format_func=lambda x: f"Servicio #{x}"
        )
        
        new_status = st.selectbox(
            "Nuevo Estado",
            options=["IN_PROGRESS", "COMPLETED"]
        )
        
        submit = st.form_submit_button("Actualizar Estado")
        
        if submit:
            try:
                service = db.query(ServiceRequest).get(service_id)
                service.status = new_status
                
                if new_status == "COMPLETED":
                    # Crear informe técnico automáticamente
                    create_technical_report(db, service)
                
                db.commit()
                st.success("Estado actualizado exitosamente")
                st.rerun()
            except Exception as e:
                st.error(f"Error al actualizar el estado: {str(e)}")
                db.rollback()

def create_technical_report(db, service):
    """Crea un nuevo informe técnico"""
    report = TechnicalReport(
        service_request_id=service.id,
        technician_id=service.technician_id,
        start_time=datetime.utcnow(),
        completion_date=datetime.utcnow(),
        diagnosis="",
        work_performed="",
        materials_used="",
        hours_worked=0.0,
        equipment_state="",
        maintenance_type="Correctivo",
        replacement_parts="",
        recommendations="",
        next_maintenance_date=None,
        photos="",
        signature_client="",
        signature_technician=""
    )
    db.add(report)

def show_technical_reports(db, technician_id):
    st.subheader("Informes Técnicos")
    
    reports = db.query(TechnicalReport).filter(
        TechnicalReport.technician_id == technician_id
    ).all()
    
    if not reports:
        st.info("No hay informes técnicos registrados")
        return
    
    for report in reports:
        with st.expander(f"Informe #{report.id} - {format_datetime(report.created_at)}"):
            show_report_details(report, db)

def show_report_details(report, db):
    """Muestra y permite editar los detalles de un informe técnico"""
    service = report.service_request

    # Información del servicio
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Información del Servicio")
        st.write(f"**Cliente:** {service.client.name}")
        st.write(f"**Tipo de Servicio:** {service.service_type}")
        st.write(f"**Fecha de Solicitud:** {format_datetime(service.requested_date)}")
    
    with col2:
        st.write("### Tiempo de Servicio")
        st.write(f"**Inicio:** {format_datetime(report.start_time)}")
        st.write(f"**Finalización:** {format_datetime(report.end_time)}")
        st.write(f"**Horas Trabajadas:** {report.hours_worked}")
    
    # Formulario para editar el informe
    with st.form(f"edit_report_{report.id}"):
        # Tabs para organizar la información
        tab1, tab2, tab3 = st.tabs(["Diagnóstico y Trabajo", "Materiales y Equipos", "Fotos y Firmas"])
        
        with tab1:
            maintenance_type = st.selectbox(
                "Tipo de Mantenimiento",
                options=["Correctivo", "Preventivo"],
                index=0 if report.maintenance_type == "Correctivo" else 1
            )
            
            diagnosis = st.text_area(
                "Diagnóstico",
                value=report.diagnosis,
                help="Describa el diagnóstico realizado"
            )
            
            work_performed = st.text_area(
                "Trabajo Realizado",
                value=report.work_performed,
                help="Describa el trabajo realizado"
            )
            
            recommendations = st.text_area(
                "Recomendaciones",
                value=report.recommendations,
                help="Recomendaciones para el cliente"
            )
        
        with tab2:
            equipment_state = st.selectbox(
                "Estado del Equipo",
                options=["Operativo", "Requiere Atención", "Crítico", "Fuera de Servicio"],
                index=0
            )
            
            materials_used = st.text_area(
                "Materiales Utilizados",
                value=report.materials_used,
                help="Liste los materiales utilizados"
            )
            
            replacement_parts = st.text_area(
                "Piezas Reemplazadas",
                value=report.replacement_parts,
                help="Liste las piezas reemplazadas"
            )
            
            next_maintenance = st.date_input(
                "Próximo Mantenimiento Recomendado",
                value=report.next_maintenance_date if report.next_maintenance_date else None,
                help="Fecha recomendada para el próximo mantenimiento"
            )
            
            hours_worked = st.number_input(
                "Horas Trabajadas",
                value=float(report.hours_worked) if report.hours_worked else 0.0,
                min_value=0.0,
                step=0.5
            )
        
        with tab3:
            # Aquí se pueden agregar campos para subir fotos y firmas
            st.write("### Evidencia Fotográfica")
            photo_upload = st.file_uploader("Subir Fotos", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
            
            st.write("### Firmas")
            col1, col2 = st.columns(2)
            with col1:
                signature_client = st.text_input("Firma del Cliente", value=report.signature_client)
            with col2:
                signature_technician = st.text_input("Firma del Técnico", value=report.signature_technician)
        
        if st.form_submit_button("Guardar Cambios"):
            try:
                # Actualizar el informe
                report.diagnosis = diagnosis
                report.work_performed = work_performed
                report.materials_used = materials_used
                report.hours_worked = hours_worked
                report.equipment_state = equipment_state
                report.maintenance_type = maintenance_type
                report.replacement_parts = replacement_parts
                report.recommendations = recommendations
                report.next_maintenance_date = next_maintenance
                report.signature_client = signature_client
                report.signature_technician = signature_technician
                report.end_time = datetime.utcnow()
                
                # Aquí se puede agregar la lógica para procesar y guardar las fotos
                
                db.commit()
                st.success("Informe actualizado exitosamente")
            except Exception as e:
                st.error(f"Error al actualizar el informe: {str(e)}")
                db.rollback()

def download_report_pdf(report):
    """Genera un PDF del informe técnico"""
    # Aquí se puede implementar la generación del PDF
    pass

def send_report_email(report):
    """Envía el informe por correo electrónico"""
    # Aquí se puede implementar el envío por correo
    pass
