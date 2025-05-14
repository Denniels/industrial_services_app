@echo off
set PYTHONIOENCODING=utf-8
set PYTHONPATH=.
call .venv\Scripts\activate.bat
streamlit run main.py
