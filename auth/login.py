# -*- coding: utf-8 -*-
import streamlit as st
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from database.config import get_db
from database.models import User
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(username: str, password: str):
    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return False
    return user

def login_page():
    st.title("Iniciar Sesión")
    
    if "user" not in st.session_state:
        st.session_state.user = None
    
    if st.session_state.user is None:
        with st.form("login_form"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Iniciar Sesión")
            
            if submit:
                user = authenticate_user(username, password)
                if user:
                    token = create_access_token({"sub": username, "role": user.role})
                    st.session_state.user = {
                        "username": user.username,
                        "role": user.role,
                        "token": token
                    }
                    st.success("¡Inicio de sesión exitoso!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")
    else:
        st.write(f"Bienvenido, {st.session_state.user['username']}")
        if st.button("Cerrar Sesión"):
            st.session_state.user = None
            st.rerun()
