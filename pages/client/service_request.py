# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime
import sys
import os

# Agregar el directorio raíz al path de Python
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from database.models import ServiceType, ServiceStatus, User, ServiceRequest, init_database

def request_service_page():
    st.header("Solicitar Nuevo Servicio")
    
    db = next(get_db())
    
    with st.form("service_request_form"):
        # Selección del tipo de servicio
        service_type = st.selectbox(
            "Tipo de Servicio",
            options=list(SERVICE_TYPES.keys()),
            format_func=lambda x: SERVICE_TYPES[x]
        )
        
        # Descripción del problema
        description = st.text_area(
            "Descripción del Problema",
            help="Por favor, describa el problema o servicio requerido en detalle"
        )
        
        # Fecha solicitada
        requested_date = st.date_input(
            "Fecha Deseada",
            min_value=datetime.now().date()
        )
        
        # Horario preferido
        preferred_time = st.time_input(
            "Horario Preferido",
            value=datetime.now().replace(hour=9, minute=0).time()
        )
        
        submit = st.form_submit_button("Enviar Solicitud")
        
        if submit:
            try:
                # Obtener el cliente actual
                client = db.query(Client).filter(
                    Client.id == st.session_state.user["client_id"]
                ).first()
                
                if not client:
                    st.error("Error: Cliente no encontrado")
                    return
                
                # Crear la solicitud de servicio
                requested_datetime = datetime.combine(requested_date, preferred_time)
                service_request = ServiceRequest(
                    client_id=client.id,
                    service_type=service_type,
                    description=description,
                    requested_date=requested_datetime,
                    status="PENDING"
                )
                
                db.add(service_request)
                db.commit()
                
                st.success("Solicitud de servicio enviada exitosamente")
                st.info(f"Número de solicitud: {service_request.id}")
                
            except Exception as e:
                st.error(f"Error al procesar la solicitud: {str(e)}")
                db.rollback()
            finally:
                db.close()

def client_dashboard():
    st.title("Panel de Cliente - Solicitud de Servicios")
    
    if 'user_id' not in st.session_state:
        st.error("Por favor inicia sesión primero")
        return
    
    # Inicializar la sesión de base de datos
    try:
        session = init_database()
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {str(e)}")
        return
    
    with st.container():
        st.header("Solicitar Nuevo Servicio")
        
        # Formulario de solicitud
        with st.form("service_request_form"):
            # Tipo de servicio
            service_type = st.selectbox(
                "Tipo de Servicio",
                options=[type.value for type in ServiceType],
                format_func=lambda x: x
            )
            
            # Descripción del problema
            description = st.text_area(
                "Descripción del Problema",
                help="Describa detalladamente el problema o servicio requerido"
            )
            
            # Urgencia
            urgency = st.slider(
                "Nivel de Urgencia",
                min_value=1,
                max_value=5,
                value=3,
                help="1: Baja, 5: Alta"
            )
            
            # Fecha deseada
            preferred_date = st.date_input(
                "Fecha Preferida",
                min_value=datetime.now().date()
            )
            
            # Botón de envío
            submitted = st.form_submit_button("Enviar Solicitud")
            
            if submitted:
                try:
                    # Crear nueva solicitud de servicio
                    new_request = ServiceRequest(
                        client_id=st.session_state.user_id,
                        service_type=service_type,
                        description=description,
                        urgency_level=urgency,
                        preferred_date=preferred_date,
                        status=ServiceStatus.PENDING.value
                    )
                    session.add(new_request)
                    session.commit()
                    st.success("Solicitud enviada exitosamente")
                except Exception as e:
                    session.rollback()
                    st.error(f"Error al enviar la solicitud: {str(e)}")
    
    # Historial de solicitudes
    with st.container():
        st.header("Mis Solicitudes")
        try:
            # Obtener solicitudes del cliente actual
            requests = (
                session.query(ServiceRequest)
                .filter(ServiceRequest.client_id == st.session_state.user_id)
                .order_by(ServiceRequest.created_at.desc())
                .all()
            )
            
            if not requests:
                st.info("No tienes solicitudes registradas")
            else:
                for request in requests:
                    with st.expander(f"Solicitud #{request.id} - {request.created_at.strftime('%Y-%m-%d')}"):
                        st.write(f"**Tipo de Servicio:** {request.service_type}")
                        st.write(f"**Estado:** {request.status}")
                        st.write(f"**Descripción:** {request.description}")
                        st.write(f"**Urgencia:** {request.urgency_level}")
                        st.write(f"**Fecha Preferida:** {request.preferred_date.strftime('%Y-%m-%d')}")
                        
        except Exception as e:
            st.error(f"Error al cargar el historial de solicitudes: {str(e)}")
    
    # Cerrar la sesión
    session.close()
