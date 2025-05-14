# -*- coding: utf-8 -*-
import streamlit as st
import sys
import os

# Configuración de codificación para Windows
if sys.platform.startswith('win'):
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'es-ES.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')
    
    # Forzar UTF-8 en Windows
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if sys.stdout.encoding != 'utf-8':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')

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
        init_database()
        
        # Resto del código de la aplicación
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
        st.error(f"Error al inicializar la base de datos: {str(e)}")

if __name__ == '__main__':
    main()
