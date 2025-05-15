# -*- coding: utf-8 -*-
import streamlit as st
import sys
import os
import locale
import io

# Configuración de codificación para Windows
if sys.platform.startswith('win'):
    try:
        # Intentar configurar la localización en español con UTF-8
        locale.setlocale(locale.LC_ALL, 'es-ES.UTF-8')
    except locale.Error:
        try:
            # Intentar configurar la localización en español con codificación Windows
            locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
        except locale.Error:
            # Si todo falla, usar la localización por defecto del sistema
            locale.setlocale(locale.LC_ALL, '')
    
    # Forzar UTF-8 en Windows
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Configurar la codificación de entrada/salida estándar
    if hasattr(sys, 'frozen'):
        # Manejo especial para ejecutables compilados
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    else:
        try:
            # Para entornos de desarrollo
            if hasattr(sys.stdout, 'buffer'):
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            if hasattr(sys.stderr, 'buffer'):
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except Exception as e:
            st.warning(f"Advertencia: No se pudo configurar la codificación UTF-8: {str(e)}")

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Gestión - Integral Service",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importaciones del proyecto
from auth.login import login_page
from database.models import init_database
from pages.admin.dashboard import admin_dashboard
from pages.technician.dashboard import technician_dashboard
from pages.client.service_request import client_dashboard

def main():
    try:
        # Inicializar la base de datos
        session = init_database()
        
        # Configurar estado de la sesión
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False

        if not st.session_state.logged_in:
            login_page()
        else:
            if st.session_state.user_role == 'admin':
                admin_dashboard()
            elif st.session_state.user_role == 'technician':
                technician_dashboard()
            else:
                client_dashboard()
                
    except Exception as e:
        st.error(f"Error en la aplicación: {str(e)}")
        
if __name__ == "__main__":
    main()
