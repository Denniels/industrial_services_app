# -*- coding: utf-8 -*-
from datetime import datetime
import streamlit as st
from database.models import MonitoringDevice, MonitoredVariable
from sqlalchemy.orm import Session

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
                    st.write(f"Valor actual: {get_latest_value(var.id)} {var.unit}")
                with col3:
                    if var.alert_enabled:
                        st.write("🔔 Alertas activadas")
                    else:
                        st.write("🔕 Alertas desactivadas")
