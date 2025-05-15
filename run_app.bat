@echo off
SETLOCAL EnableDelayedExpansion

REM Configurar codificación y variables de entorno
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
set PYTHONPATH=.

REM Verificar si el entorno virtual existe
if not exist .venv (
    echo Creando entorno virtual...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

REM Ejecutar la aplicación
echo Iniciando la aplicación...
streamlit run main.py

ENDLOCAL
