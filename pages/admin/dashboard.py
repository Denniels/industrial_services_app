import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from database.config import get_db
from database.models import ServiceRequest, TechnicalReport, Client, Equipment, User, UserRole

def admin_dashboard():
    st.header("Panel de Control Administrativo")
    
    # Obtener datos
    db = next(get_db())
    
    # Layout en pestañas
    tab1, tab2, tab3, tab4 = st.tabs([
        "Vista General",
        "Servicios",
        "Técnicos",
        "Finanzas"
    ])
    
    with tab1:
        show_general_overview(db)
    
    with tab2:
        show_services_overview(db)
    
    with tab3:
        show_technicians_overview(db)
    
    with tab4:
        show_financial_overview(db)

def show_general_overview(db):
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    # Total de servicios activos
    active_services = db.query(ServiceRequest).filter(
        ServiceRequest.status.in_(['PENDING', 'IN_PROGRESS'])
    ).count()
    
    # Total de clientes activos
    active_clients = db.query(Client).filter(Client.is_active == True).count()
    
    # Total de equipos registrados
    total_equipment = db.query(Equipment).count()
    
    # Total de técnicos
    total_technicians = db.query(User).filter(User.role == UserRole.TECHNICIAN).count()
    
    with col1:
        st.metric("Servicios Activos", active_services)
    with col2:
        st.metric("Clientes Activos", active_clients)
    with col3:
        st.metric("Equipos Registrados", total_equipment)
    with col4:
        st.metric("Técnicos", total_technicians)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        show_services_trend(db)
    
    with col2:
        show_service_types_distribution(db)

def show_services_overview(db):
    st.subheader("Resumen de Servicios")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        date_range = st.date_input(
            "Rango de fechas",
            value=(datetime.now() - timedelta(days=30), datetime.now())
        )
    with col2:
        status_filter = st.multiselect(
            "Estado",
            ["PENDING", "IN_PROGRESS", "COMPLETED", "CANCELLED"],
            default=["PENDING", "IN_PROGRESS"]
        )
    
    # Tabla de servicios
    services = db.query(ServiceRequest).filter(
        ServiceRequest.status.in_(status_filter)
    ).all()
    
    show_services_table(services)

def show_technicians_overview(db):
    st.subheader("Desempeño de Técnicos")
    
    # Estadísticas por técnico
    technicians = db.query(User).filter(User.role == UserRole.TECHNICIAN).all()
    
    for tech in technicians:
        with st.expander(f"{tech.first_name} {tech.last_name}"):
            show_technician_stats(tech, db)

def show_financial_overview(db):
    st.subheader("Resumen Financiero")
    
    # Métricas financieras
    col1, col2 = st.columns(2)
    
    with col1:
        show_monthly_revenue(db)
    
    with col2:
        show_pending_payments(db)

def show_services_trend(db):
    # Implementar gráfico de tendencia de servicios
    pass

def show_service_types_distribution(db):
    # Implementar gráfico de distribución de tipos de servicio
    pass

def show_services_table(services):
    # Implementar tabla de servicios
    pass

def show_technician_stats(technician, db):
    # Implementar estadísticas del técnico
    pass

def show_monthly_revenue(db):
    # Implementar gráfico de ingresos mensuales
    pass

def show_pending_payments(db):
    # Implementar resumen de pagos pendientes
    pass
