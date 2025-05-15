# -*- coding: utf-8 -*-
import streamlit as st
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from database.config import get_db
from database.models import User, UserRole
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import base64
import binascii
import logging
import os

# Asegurar que el directorio de logs existe
os.makedirs('logs', exist_ok=True)

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/auth.log', encoding='utf-8', mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_access_token(data: dict):
    """Crear token JWT de acceso"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def hash_password(password: str) -> str:
    """Genera un hash seguro de la contraseña"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return base64.b64encode(hashed).decode('ascii')

def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Verifica la contraseña contra el hash almacenado"""
    try:
        logger.debug(f"Verificando contraseña para hash: {stored_hash[:20]}...")
        
        # Convertir contraseña a bytes usando UTF-8
        password_bytes = plain_password.encode('utf-8')
        logger.debug(f"Contraseña convertida a bytes: {len(password_bytes)} bytes")
        
        # Decodificar el hash de base64 a bytes
        try:
            hash_bytes = base64.b64decode(stored_hash.encode('ascii'))
            logger.debug(f"Hash decodificado exitosamente: {len(hash_bytes)} bytes")
        except (binascii.Error, UnicodeEncodeError) as e:
            logger.error(f"Error al decodificar hash base64: {str(e)}")
            return False
            
        # Verificar la contraseña
        try:
            result = bcrypt.checkpw(password_bytes, hash_bytes)
            logger.debug(f"Resultado de verificación: {result}")
            return result
        except Exception as e:
            logger.error(f"Error en bcrypt.checkpw: {str(e)}")
            return False
            
    except Exception as e:
        logger.error(f"Error durante autenticación: {str(e)}")
        return False

def authenticate_user(username: str, password: str):
    """Autenticar usuario"""
    try:
        logger.info(f"Intento de autenticación para usuario: {username}")
        
        db = next(get_db())
        user = db.query(User).filter_by(username=username).first()
        
        if not user:
            logger.warning(f"Usuario no encontrado: {username}")
            return False
        
        logger.debug(f"Usuario encontrado - ID: {user.id}, Activo: {user.is_active}")
        
        if not user.is_active:
            logger.warning(f"Usuario inactivo: {username}")
            return False
            
        if verify_password(password, user.password):
            logger.info(f"Autenticación exitosa para: {username}")
            return user
        else:
            logger.warning(f"Contraseña incorrecta para: {username}")
            return False
            
    except Exception as e:
        logger.error(f"Error durante autenticación: {e}")
        return False
    finally:
        db.close()

def init_session_state():
    """Inicializar el estado de la sesión"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'

def login_page():
    """Página de inicio de sesión"""
    init_session_state()
    
    st.title("Iniciar sesión")
    
    # Campos de entrada
    username = st.text_input("Usuario").strip()
    password = st.text_input("Contraseña", type="password").strip()
    
    if st.button("Iniciar sesión"):
        try:
            if not username or not password:
                st.error("Por favor ingrese usuario y contraseña")
                return
                
            logger.debug(f"Iniciando proceso de autenticación para: {username}")
            user = authenticate_user(username, password)
            
            if user:
                # Guardar información del usuario en la sesión
                st.session_state.user = {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role.value,
                    "email": user.email,
                    "is_active": user.is_active
                }
                st.session_state.user_id = user.id
                st.session_state.authenticated = True
                
                # Redirigir según el rol del usuario
                if user.role == UserRole.ADMIN:
                    st.session_state.current_page = "admin_dashboard"
                elif user.role == UserRole.TECHNICIAN:
                    st.session_state.current_page = "technician_dashboard"
                elif user.role == UserRole.SUPERVISOR:
                    st.session_state.current_page = "supervisor_dashboard"
                else:  # Cliente
                    st.session_state.current_page = "client_dashboard"
                
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrecta")
                
        except Exception as e:
            logger.error(f"Error en login_page: {e}")
            st.error("Error durante el inicio de sesión. Por favor intente nuevamente.")
