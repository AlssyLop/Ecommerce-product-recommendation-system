@echo off
REM Sistema de Recomendación E-commerce con Base de Datos Relacional
REM Este script ejecuta la aplicación mejorada con interfaz relacional

setlocal enabledelayedexpansion

REM Obtener la ruta del directorio actual
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Verificar que el entorno virtual existe
if not exist ".venv\Scripts\activate.bat" (
    echo.
    echo ========================================
    echo ERROR: Entorno Virtual no encontrado
    echo ========================================
    echo.
    echo Por favor, ejecuta primero:
    echo   python -m venv .venv
    echo.
    pause
    exit /b 1
)

REM Activar entorno virtual
call .venv\Scripts\activate.bat

echo.
echo ========================================
echo Sistema de Recomendacion E-commerce
echo Base de Datos Relacional
echo ========================================
echo.

REM Verificar que existen las tablas de la BD relacional
if not exist "db_usuarios.csv" (
    echo Creando tablas de la base de datos relacional...
    python crear_base_datos_relacional.py
    if errorlevel 1 (
        echo.
        echo ERROR: No se pudieron crear las tablas relacionales
        pause
        exit /b 1
    )
    echo Tablas creadas exitosamente!
    echo.
)

echo Instalando dependencias...
pip install -r requirements.txt --quiet

echo.
echo ========================================
echo Iniciando aplicacion web mejorada...
echo ========================================
echo.
echo La aplicacion se abrira en: http://localhost:8501
echo.
echo Presiona Ctrl+C para detener la aplicacion
echo.

REM Ejecutar la aplicación mejorada con BD relacional
streamlit run app_relacional.py

pause
exit /b 0


