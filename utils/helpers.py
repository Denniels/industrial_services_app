# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

def format_datetime(dt):
    """Formatea una fecha y hora para mostrar en la interfaz"""
    if not dt:
        return ""
    return dt.strftime("%d/%m/%Y %H:%M")

def create_calendar_dates(start_date=None, days=7):
    """Crea un rango de fechas para el calendario"""
    if not start_date:
        start_date = datetime.now()
    dates = [start_date + timedelta(days=x) for x in range(days)]
    return dates

def create_time_slots(start_hour=8, end_hour=18, interval_minutes=30):
    """Crea slots de tiempo para el calendario"""
    slots = []
    current = datetime.now().replace(hour=start_hour, minute=0, second=0, microsecond=0)
    end = current.replace(hour=end_hour, minute=0)
    
    while current < end:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=interval_minutes)
    
    return slots

def create_data_table(data, key=None):
    """Crea una tabla de datos interactiva"""
    if not data:
        st.write("No hay datos disponibles")
        return
    
    df = pd.DataFrame(data)
    st.dataframe(df, key=key)

def show_status_badge(status):
    """Muestra un badge con el estado del servicio"""
    colors = {
        'PENDING': 'orange',
        'IN_PROGRESS': 'blue',
        'COMPLETED': 'green',
        'CANCELLED': 'red'
    }
    
    return f'<span style="background-color: {colors.get(status, "gray")}; padding: 0.2rem 0.5rem; border-radius: 0.25rem; color: white;">{status}</span>'

def format_currency(amount):
    """Formatea un monto como moneda"""
    return f"${amount:,.2f}"
