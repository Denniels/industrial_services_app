# -*- coding: utf-8 -*-
import streamlit as st
import sys
import os
import locale
import io
import warnings
from auth.login import login_page
from pages.admin.dashboard import admin_dashboard
from pages.client.monitoring import show_monitoring_dashboard
from pages.technician.dashboard import technician_dashboard
from pages.supervisor.dashboard import supervisor_dashboard
from database.models import init_database

# Suprimir advertencias específicas de codificación
warnings.filterwarnings('ignore', category=RuntimeWarning, module='streamlit')

# Configuración de codificación para Windows
if sys.platform.startswith('win'):
    try:
        locale.setlocale(locale.LC_ALL, 'es-ES.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')
    
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['LANG'] = 'es_ES.UTF-8'

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Servicios Industriales",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Sistema de Servicios Industriales - Versión 1.0",
        'Report a bug': "https://github.com/tu-repo/issues",
        'Get help': "https://docs.tu-sistema.com"
    }
)

# Inicializar la base de datos
try:
    init_database()
except Exception as e:
    st.error(f"Error al inicializar la base de datos: {str(e)}")
    st.stop()

# Inicializar estado de la sesión
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'

# Manejo de cerrar sesión en el sidebar
if st.sidebar.button('Cerrar Sesión') and 'authenticated' in st.session_state:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Enrutamiento basado en el estado de la sesión
if not st.session_state.get('authenticated', False):
    login_page()
else:
    # Mostrar información del usuario
    st.sidebar.info(f"Usuario: {st.session_state.user['username']}")
    
    # Menú de navegación según el rol
    if st.session_state.user['role'] == 'ADMIN':
        pages = {
            'Panel de Control': 'admin_dashboard',
            'Gestión de Usuarios': 'user_management',
            'Gestión de Servicios': 'service_management',
            'Reportes': 'reports',
            'Configuración': 'settings'
        }
    elif st.session_state.user['role'] == 'SUPERVISOR':
        pages = {
            'Panel de Supervisor': 'supervisor_dashboard',
            'Gestión de Servicios': 'service_management',
            'Reportes': 'reports'
        }
    elif st.session_state.user['role'] == 'TECHNICIAN':
        pages = {
            'Mis Servicios': 'technician_dashboard',
            'Reportes Técnicos': 'technical_reports'
        }
    else:  # CLIENT
        pages = {
            'Monitor de Variables': 'monitoring_dashboard',
            'Solicitudes de Servicio': 'service_requests',
            'Historial': 'service_history'
        }
    
    # Selector de página en el sidebar
    if len(pages) > 1:  # Solo mostrar selector si hay más de una página
        selected_page = st.sidebar.selectbox('Navegación', list(pages.keys()))
        st.session_state.current_page = pages[selected_page]
    
    # Enrutamiento a la página correspondiente
    try:
        if st.session_state.current_page == 'admin_dashboard':
            admin_dashboard()
        elif st.session_state.current_page == 'supervisor_dashboard':
            supervisor_dashboard()
        elif st.session_state.current_page == 'technician_dashboard':
            technician_dashboard()
        elif st.session_state.current_page == 'monitoring_dashboard':
            show_monitoring_dashboard()
        elif st.session_state.current_page == 'service_requests':
            from pages.client.service_request import show_service_requests
            show_service_requests()
        # ... más páginas según sea necesario
    except Exception as e:
        st.error(f"Error al cargar la página: {str(e)}")
        st.error("Por favor, intente recargar la página o contacte al administrador.")
