# -*- coding: utf-8 -*-
import streamlit as st
from database.config import get_db
from database.models import ServiceRequest, User, Client, Equipment, TechnicalReport
from datetime import datetime, timedelta
import pandas as pd

def supervisor_dashboard():
    """Dashboard para supervisores"""
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        st.error("Por favor inicia sesión primero")
        return
        
    if st.session_state.user['role'] != 'SUPERVISOR':
        st.error("Acceso no autorizado")
        return
        
    st.title("Panel de Supervisor")
    
    # Menú principal
    menu = st.sidebar.selectbox(
        "Menú",
        ["Resumen de Servicios", "Asignación de Técnicos", "Programación", "Reportes"]
    )
    
    db = next(get_db())
    
    try:
        if menu == "Resumen de Servicios":
            show_services_summary(db)
        elif menu == "Asignación de Técnicos":
            show_technician_assignment(db)
        elif menu == "Programación":
            show_service_scheduling(db)
        elif menu == "Reportes":
            show_supervisor_reports(db)
    finally:
        db.close()

def show_services_summary(db):
    """Mostrar resumen de servicios"""
    st.header("Resumen de Servicios")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pending_services = db.query(ServiceRequest)\
            .filter(ServiceRequest.status == 'PENDING')\
            .count()
        st.metric("Servicios Pendientes", pending_services)
    
    with col2:
        in_progress = db.query(ServiceRequest)\
            .filter(ServiceRequest.status == 'IN_PROGRESS')\
            .count()
        st.metric("Servicios en Proceso", in_progress)
    
    with col3:
        completed_today = db.query(ServiceRequest)\
            .filter(
                ServiceRequest.status == 'COMPLETED',
                ServiceRequest.completion_date >= datetime.now().date()
            ).count()
        st.metric("Completados Hoy", completed_today)
    
    # Lista de servicios pendientes
    st.subheader("Servicios Pendientes")
    pending = db.query(ServiceRequest)\
        .filter(ServiceRequest.status.in_(['PENDING', 'IN_PROGRESS']))\
        .all()
    
    for service in pending:
        with st.expander(f"Servicio #{service.id} - {service.client.name}"):
            st.write(f"Tipo: {service.service_type}")
            st.write(f"Estado: {service.status}")
            st.write(f"Descripción: {service.description}")
            if service.technician:
                st.write(f"Técnico Asignado: {service.technician.username}")
            st.write(f"Fecha Solicitada: {service.requested_date}")

def show_technician_assignment(db):
    """Gestión de asignación de técnicos"""
    st.header("Asignación de Técnicos")
    
    # Mostrar servicios sin asignar
    unassigned = db.query(ServiceRequest)\
        .filter(ServiceRequest.assigned_technician_id == None)\
        .all()
    
    if unassigned:
        st.subheader("Servicios sin Asignar")
        for service in unassigned:
            with st.expander(f"Servicio #{service.id} - {service.client.name}"):
                st.write(f"Tipo: {service.service_type}")
                st.write(f"Descripción: {service.description}")
                
                # Lista de técnicos disponibles
                technicians = db.query(User)\
                    .filter(User.role == 'TECHNICIAN')\
                    .filter(User.is_active == True)\
                    .all()
                
                selected_tech = st.selectbox(
                    "Asignar Técnico",
                    options=[t.username for t in technicians],
                    key=f"tech_select_{service.id}"
                )
                
                if st.button("Asignar", key=f"assign_{service.id}"):
                    try:
                        tech = next(t for t in technicians if t.username == selected_tech)
                        service.assigned_technician_id = tech.id
                        db.commit()
                        st.success(f"Técnico {selected_tech} asignado exitosamente")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al asignar técnico: {str(e)}")

def show_service_scheduling(db):
    """Programación de servicios"""
    st.header("Programación de Servicios")
    
    # Calendario de servicios
    start_date = st.date_input("Fecha de inicio", datetime.now())
    end_date = start_date + timedelta(days=7)
    
    services = db.query(ServiceRequest)\
        .filter(ServiceRequest.scheduled_date.between(start_date, end_date))\
        .all()
    
    # Mostrar servicios programados por día
    current_date = start_date
    while current_date <= end_date:
        day_services = [s for s in services if s.scheduled_date.date() == current_date]
        
        with st.expander(f"{current_date.strftime('%A %d/%m/%Y')}", 
                        expanded=(current_date == start_date)):
            if day_services:
                for service in day_services:
                    st.write(f"- {service.scheduled_date.strftime('%H:%M')} - "
                            f"{service.client.name} ({service.service_type})")
            else:
                st.write("No hay servicios programados")
        
        current_date += timedelta(days=1)

def show_supervisor_reports(db):
    """Reportes para supervisores"""
    st.header("Reportes")
    
    # Métricas del mes
    st.subheader("Métricas del Mes")
    col1, col2 = st.columns(2)
    
    with col1:
        month_start = datetime.now().replace(day=1)
        month_services = db.query(ServiceRequest)\
            .filter(ServiceRequest.created_at >= month_start)\
            .count()
        st.metric("Servicios este mes", month_services)
    
    with col2:
        completed = db.query(ServiceRequest)\
            .filter(
                ServiceRequest.created_at >= month_start,
                ServiceRequest.status == 'COMPLETED'
            ).count()
        completion_rate = (completed / month_services * 100) if month_services > 0 else 0
        st.metric("Tasa de completitud", f"{completion_rate:.1f}%")
    
    # Rendimiento de técnicos
    st.subheader("Rendimiento de Técnicos")
    technicians = db.query(User)\
        .filter(User.role == 'TECHNICIAN')\
        .all()
    
    tech_data = []
    for tech in technicians:
        completed = db.query(ServiceRequest)\
            .filter(
                ServiceRequest.assigned_technician_id == tech.id,
                ServiceRequest.status == 'COMPLETED',
                ServiceRequest.created_at >= month_start
            ).count()
        
        pending = db.query(ServiceRequest)\
            .filter(
                ServiceRequest.assigned_technician_id == tech.id,
                ServiceRequest.status.in_(['PENDING', 'IN_PROGRESS'])
            ).count()
        
        tech_data.append({
            'Técnico': tech.username,
            'Servicios Completados': completed,
            'Servicios Pendientes': pending
        })
    
    if tech_data:
        st.dataframe(pd.DataFrame(tech_data))
