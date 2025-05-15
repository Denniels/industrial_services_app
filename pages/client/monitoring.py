# -*- coding: utf-8 -*-

from datetime import datetime
import streamlit as st
from database.models import MonitoringDevice, MonitoredVariable
from sqlalchemy.orm import Session
from database.config import get_session
import logging

# Configurar logging
logger = logging.getLogger(__name__)

def get_latest_value(variable_id: int, session: Session) -> float:
    """Obtener el último valor registrado para una variable"""
    try:
        variable = session.query(MonitoredVariable).get(variable_id)
        if not variable or not variable.readings:
            return 0.0
        return variable.readings[-1].value
    except Exception as e:
        logger.error(f"Error al obtener último valor: {str(e)}")
        return 0.0

def add_monitoring_device(session: Session, client_id: int, device_serial: str):
    """Agregar un nuevo dispositivo de monitoreo"""
    device = MonitoringDevice(
        client_id=client_id,
        device_serial=device_serial
    )
    session.add(device)
    session.commit()
    return device

def add_monitored_variable(
    session: Session,
    device_id: int,
    name: str,
    description: str,
    unit: str,
    min_value: float = None,
    max_value: float = None
):
    """Agregar una nueva variable a monitorear"""
    # Verificar si el dispositivo tiene espacio para más variables
    device = session.query(MonitoringDevice).get(device_id)
    if device.variables_count >= device.max_variables:
        raise ValueError("Dispositivo ha alcanzado el máximo de variables permitidas")
    
    variable = MonitoredVariable(
        device_id=device_id,
        name=name,
        description=description,
        unit=unit,
        min_value=min_value,
        max_value=max_value
    )
    session.add(variable)
    device.variables_count += 1
    session.commit()
    return variable

def show_monitoring_dashboard():
    """Mostrar el dashboard de monitoreo"""
    st.title("Panel de Monitoreo")
    
    if 'user_id' not in st.session_state:
        st.error("Por favor inicia sesión primero")
        return
        
    session = get_session()
    try:
        # Mostrar dispositivos del cliente
        devices = session.query(MonitoringDevice)\
            .filter(MonitoringDevice.client_id == st.session_state.user_id)\
            .all()
        
        if not devices:
            st.info("No tienes dispositivos de monitoreo configurados")
            return
        
        for device in devices:
            with st.expander(f"Dispositivo: {device.device_serial}"):
                st.write(f"Variables monitoreadas: {device.variables_count}/{device.max_variables}")
                
                # Mostrar variables
                for var in device.variables:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**{var.name}**")
                    with col2:
                        st.write(f"Valor actual: {get_latest_value(var.id, session)} {var.unit}")
                    with col3:
                        if var.alert_enabled:
                            st.write("🔔 Alertas activadas")
                        else:
                            st.write("🔕 Alertas desactivadas")
                            
                # Botón para agregar variable
                if device.variables_count < device.max_variables:
                    if st.button(f"Agregar Variable a {device.device_serial}"):
                        st.session_state.selected_device = device.id
                        st.session_state.show_add_variable = True
                
        # Formulario para agregar variable
        if 'show_add_variable' in st.session_state and st.session_state.show_add_variable:
            with st.form("add_variable_form"):
                st.subheader("Agregar Nueva Variable")
                name = st.text_input("Nombre de la Variable")
                description = st.text_area("Descripción")
                unit = st.text_input("Unidad de Medida")
                min_value = st.number_input("Valor Mínimo", value=0.0)
                max_value = st.number_input("Valor Máximo", value=100.0)
                
                if st.form_submit_button("Guardar"):
                    try:
                        add_monitored_variable(
                            session,
                            st.session_state.selected_device,
                            name,
                            description,
                            unit,
                            min_value,
                            max_value
                        )
                        st.success("Variable agregada exitosamente")
                        st.session_state.show_add_variable = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al agregar variable: {str(e)}")
                        
    except Exception as e:
        logger.error(f"Error al cargar el panel de monitoreo: {str(e)}")
        st.error("Error al cargar el panel de monitoreo. Por favor, inténtalo de nuevo más tarde.")
    finally:
        session.close()

if __name__ == "__main__":
    show_monitoring_dashboard()

