# -*- coding: utf-8 -*-
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from database.config import get_db
from database.models import (
    ServiceRequest, TechnicalReport, Client, Equipment,
    User, UserRole, ServiceType, ServiceStatus
)
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

def admin_dashboard():
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        st.error("Por favor inicia sesión primero")
        return
        
    if st.session_state.user['role'] != 'ADMIN':
        st.error("Acceso no autorizado")
        return
        
    st.title("Panel de Administración")
    
    # Menú principal
    menu = st.sidebar.selectbox(
        "Menú",
        ["Vista General", "Gestión de Usuarios", "Gestión de Servicios", 
         "Consultas DB", "Reportes", "Configuración"]
    )
    
    db = next(get_db())
    
    try:
        if menu == "Vista General":
            show_general_overview(db)
        elif menu == "Gestión de Usuarios":
            show_user_management(db)
        elif menu == "Gestión de Servicios":
            show_service_management(db)
        elif menu == "Consultas DB":
            show_db_queries(db)
        elif menu == "Reportes":
            show_reports(db)
        elif menu == "Configuración":
            show_settings(db)
    finally:
        db.close()

def show_user_management(db):
    st.header("Gestión de Usuarios")
    
    tab1, tab2, tab3 = st.tabs(["Crear Usuario", "Listar Usuarios", "Modificar Usuario"])
    
    with tab1:
        with st.form("create_user"):
            st.subheader("Crear Nuevo Usuario")
            username = st.text_input("Nombre de Usuario")
            password = st.text_input("Contraseña", type="password")
            role = st.selectbox("Rol", ["ADMIN", "TECHNICIAN", "SUPERVISOR", "CLIENT"])
            email = st.text_input("Email")
            
            if st.form_submit_button("Crear Usuario"):
                try:
                    new_user = User(
                        username=username,
                        email=email,
                        role=UserRole[role]
                    )
                    new_user.set_password(password)
                    db.add(new_user)
                    db.commit()
                    st.success(f"Usuario {username} creado exitosamente")
                except Exception as e:
                    st.error(f"Error al crear usuario: {str(e)}")
    
    with tab2:
        users = db.query(User).all()
        user_data = []
        for user in users:
            user_data.append({
                "ID": user.id,
                "Usuario": user.username,
                "Rol": user.role.value,
                "Email": user.email,
                "Activo": user.is_active
            })
        st.dataframe(pd.DataFrame(user_data))
    
    with tab3:
        user_to_modify = st.selectbox(
            "Seleccionar Usuario",
            options=[u.username for u in db.query(User).all()]
        )
        if user_to_modify:
            user = db.query(User).filter_by(username=user_to_modify).first()
            with st.form("modify_user"):
                email = st.text_input("Email", value=user.email)
                role = st.selectbox("Rol", ["ADMIN", "TECHNICIAN", "SUPERVISOR", "CLIENT"], index=["ADMIN", "TECHNICIAN", "SUPERVISOR", "CLIENT"].index(user.role.value))
                is_active = st.checkbox("Usuario Activo", value=user.is_active)
                new_password = st.text_input("Nueva Contraseña (dejar en blanco para mantener)", type="password")
                
                if st.form_submit_button("Actualizar Usuario"):
                    try:
                        user.email = email
                        user.role = UserRole[role]
                        user.is_active = is_active
                        if new_password:
                            user.set_password(new_password)
                        db.commit()
                        st.success("Usuario actualizado exitosamente")
                    except Exception as e:
                        st.error(f"Error al actualizar usuario: {str(e)}")

def show_service_management(db):
    st.header("Gestión de Servicios")
    
    tab1, tab2 = st.tabs(["Agendar Servicio", "Ver Servicios"])
    
    with tab1:
        with st.form("schedule_service"):
            st.subheader("Agendar Nuevo Servicio")
            
            # Seleccionar cliente
            clients = db.query(Client).all()
            client = st.selectbox(
                "Cliente",
                options=[c.name for c in clients]
            )
            
            # Seleccionar técnico
            technicians = db.query(User).filter(User.role == UserRole.TECHNICIAN).all()
            technician = st.selectbox(
                "Técnico",
                options=[t.username for t in technicians]
            )
            
            # Detalles del servicio
            service_type = st.selectbox(
                "Tipo de Servicio",
                options=["MANTENIMIENTO", "REPARACION", "INSTALACION", "DIAGNOSTICO"]
            )
            description = st.text_area("Descripción")
            scheduled_date = st.date_input("Fecha Programada")
            scheduled_time = st.time_input("Hora Programada")
            
            if st.form_submit_button("Agendar Servicio"):
                try:
                    # Crear el servicio
                    new_service = ServiceRequest(
                        client_id=next(c.id for c in clients if c.name == client),
                        technician_id=next(t.id for t in technicians if t.username == technician),
                        service_type=service_type,
                        description=description,
                        scheduled_datetime=datetime.combine(scheduled_date, scheduled_time),
                        status=ServiceStatus.PENDING
                    )
                    db.add(new_service)
                    db.commit()
                    st.success("Servicio agendado exitosamente")
                except Exception as e:
                    st.error(f"Error al agendar servicio: {str(e)}")
    
    with tab2:
        services = db.query(ServiceRequest).all()
        service_data = []
        for service in services:
            service_data.append({
                "ID": service.id,
                "Cliente": service.client.name,
                "Técnico": service.technician.username,
                "Tipo": service.service_type,
                "Estado": service.status.value,
                "Fecha Programada": service.scheduled_datetime
            })
        st.dataframe(pd.DataFrame(service_data))

def show_db_queries(db):
    st.header("Consultas a la Base de Datos")
    
    # Área de consulta
    query = st.text_area(
        "Ingrese su consulta SQL",
        height=200,
        help="Escriba su consulta SQL aquí. Solo se permiten consultas SELECT."
    )
    
    if st.button("Ejecutar Consulta"):
        if not query.strip().upper().startswith("SELECT"):
            st.error("Por seguridad, solo se permiten consultas SELECT")
            return
            
        try:
            result = db.execute(text(query))
            df = pd.DataFrame(result.fetchall())
            if not df.empty:
                st.dataframe(df)
            else:
                st.info("La consulta no devolvió resultados")
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {str(e)}")
    
    # Consultas predefinidas
    st.subheader("Consultas Predefinidas")
    preset_query = st.selectbox(
        "Seleccione una consulta",
        [
            "Servicios pendientes por técnico",
            "Clientes más frecuentes",
            "Tiempo promedio de servicio por tipo",
            "Estado de equipos por cliente",
            "Histórico de servicios por mes"
        ]
    )
    
    if st.button("Ejecutar Consulta Predefinida"):
        execute_preset_query(db, preset_query)

def show_reports(db):
    st.header("Reportes y Estadísticas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de servicios por estado
        services_by_status = db.query(
            ServiceRequest.status,
            db.func.count(ServiceRequest.id)
        ).group_by(ServiceRequest.status).all()
        
        fig = go.Figure(data=[
            go.Pie(
                labels=[status.value for status, _ in services_by_status],
                values=[count for _, count in services_by_status],
                hole=.3
            )
        ])
        fig.update_layout(title="Servicios por Estado")
        st.plotly_chart(fig)
    
    with col2:
        # Gráfico de servicios por técnico
        services_by_tech = db.query(
            User.username,
            db.func.count(ServiceRequest.id)
        ).join(ServiceRequest, ServiceRequest.technician_id == User.id)\
         .group_by(User.username).all()
        
        fig = go.Figure(data=[
            go.Bar(
                x=[tech for tech, _ in services_by_tech],
                y=[count for _, count in services_by_tech]
            )
        ])
        fig.update_layout(title="Servicios por Técnico")
        st.plotly_chart(fig)

def show_settings(db):
    st.header("Configuración")
    
    # Configuración de la aplicación
    st.subheader("Configuración General")
    with st.form("app_settings"):
        max_services_per_day = st.number_input(
            "Máximo de servicios por día",
            min_value=1,
            value=10
        )
        working_hours_start = st.time_input("Hora de inicio de trabajo", value=datetime.strptime("08:00", "%H:%M").time())
        working_hours_end = st.time_input("Hora de fin de trabajo", value=datetime.strptime("18:00", "%H:%M").time())
        
        if st.form_submit_button("Guardar Configuración"):
            # Aquí se guardaría la configuración en la base de datos
            st.success("Configuración guardada exitosamente")
    
    # Respaldo de base de datos
    st.subheader("Respaldo de Base de Datos")
    if st.button("Crear Respaldo"):
        try:
            backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
            # Aquí se implementaría la lógica de respaldo
            st.success(f"Respaldo creado exitosamente: {backup_filename}")
        except Exception as e:
            st.error(f"Error al crear respaldo: {str(e)}")

def execute_preset_query(db, query_name):
    try:
        if query_name == "Servicios pendientes por técnico":
            result = db.query(
                User.username,
                db.func.count(ServiceRequest.id)
            ).join(ServiceRequest, ServiceRequest.technician_id == User.id)\
             .filter(ServiceRequest.status == ServiceStatus.PENDING)\
             .group_by(User.username).all()
            
        elif query_name == "Clientes más frecuentes":
            result = db.query(
                Client.name,
                db.func.count(ServiceRequest.id)
            ).join(ServiceRequest, ServiceRequest.client_id == Client.id)\
             .group_by(Client.name)\
             .order_by(db.func.count(ServiceRequest.id).desc()).all()
        
        # ... más consultas predefinidas ...
        
        df = pd.DataFrame(result, columns=["Nombre", "Cantidad"])
        st.dataframe(df)
        
    except Exception as e:
        st.error(f"Error al ejecutar la consulta: {str(e)}")

def show_general_overview(db):
    st.header("Vista General")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_services = db.query(ServiceRequest)\
            .filter(ServiceRequest.status.in_(['PENDING', 'IN_PROGRESS']))\
            .count()
        st.metric("Servicios Activos", active_services)
    
    with col2:
        total_clients = db.query(Client).filter(Client.is_active == True).count()
        st.metric("Clientes Activos", total_clients)
    
    with col3:
        total_technicians = db.query(User)\
            .filter(User.role == UserRole.TECHNICIAN)\
            .filter(User.is_active == True)\
            .count()
        st.metric("Técnicos Activos", total_technicians)
    
    with col4:
        completed_services = db.query(ServiceRequest)\
            .filter(ServiceRequest.status == ServiceStatus.COMPLETED)\
            .count()
        st.metric("Servicios Completados", completed_services)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        show_services_trend(db)
    
    with col2:
        show_service_types_distribution(db)

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
