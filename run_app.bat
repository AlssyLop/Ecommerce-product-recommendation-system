@echo off
echo ========================================
echo Sistema de Recomendacion E-commerce
echo ========================================
echo.
echo Instalando dependencias...
pip install -r requirements.txt
echo.
echo Iniciando aplicacion web...
streamlit run app.py
pause


