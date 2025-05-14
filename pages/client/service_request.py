import streamlit as st
from database.config import get_db
from database.models import ServiceRequest, Client
from datetime import datetime
from config import SERVICE_TYPES
from utils.helpers import format_datetime

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
