# -*- coding: utf-8 -*-
import os
import streamlit as st
from auth.login import login_page
from database.config import engine
from database.models import Base
import config
from dotenv import load_dotenv

# Asegurar que las variables de entorno estén cargadas
load_dotenv()

# Inicializar la base de datos
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    st.error(f"Error al inicializar la base de datos: {str(e)}")
    st.stop()

# Configuración de la página
try:
    st.set_page_config(
        page_title=config.APP_NAME,
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception as e:
    st.error(f"Error en la configuración de la página: {str(e)}")
    st.stop()

def main():
    # Verificar autenticación
    if "user" not in st.session_state or st.session_state.user is None:
        login_page()
        return

    # Sidebar con navegación
    st.sidebar.title("Menú Principal")
    user_role = st.session_state.user["role"]

    if user_role == "admin":
        page = st.sidebar.selectbox(
            "Seleccione una página",
            ["Dashboard", "Clientes", "Servicios", "Técnicos", "Facturación"]
        )
    elif user_role == "technician":
        page = st.sidebar.selectbox(
            "Seleccione una página",
            ["Mis Servicios", "Informes Técnicos", "Mi Calendario"]
        )
    else:  # cliente
        page = st.sidebar.selectbox(
            "Seleccione una página",
            ["Solicitar Servicio", "Mis Servicios", "Facturas"]
        )

    # Mostrar la página seleccionada
    st.title(page)
    
    # Aquí irá la lógica de enrutamiento a las diferentes páginas
    if page == "Dashboard":
        show_dashboard()
    elif page == "Clientes":
        show_clients()
    # ... (más páginas se agregarán después)

def show_dashboard():
    st.header("Dashboard")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Servicios Pendientes", value="10")
    with col2:
        st.metric(label="Servicios en Proceso", value="5")
    with col3:
        st.metric(label="Servicios Completados", value="15")

def show_clients():
    st.header("Gestión de Clientes")
    # Aquí irá la lógica de gestión de clientes

if __name__ == "__main__":
    main()
