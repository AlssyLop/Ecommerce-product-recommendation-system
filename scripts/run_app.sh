#!/bin/bash

# Sistema de Recomendación E-commerce con Base de Datos Relacional
# Este script ejecuta la aplicación mejorada con interfaz relacional

set -e

# Obtener directorio actual
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

# Verificar que el entorno virtual existe
if [ ! -f ".venv/bin/activate" ]; then
    echo ""
    echo "========================================"
    echo "ERROR: Entorno Virtual no encontrado"
    echo "========================================"
    echo ""
    echo "Por favor, ejecuta primero:"
    echo "  python -m venv .venv"
    echo ""
    exit 1
fi

# Activar entorno virtual
source .venv/bin/activate

echo ""
echo "========================================"
echo "Sistema de Recomendación E-commerce"
echo "Base de Datos Relacional"
echo "========================================"
echo ""

# Verificar que existen las tablas de la BD relacional
if [ ! -f "data/db_usuarios.csv" ]; then
    echo "Creando tablas de la base de datos relacional..."
    python crear_base_datos_relacional.py
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: No se pudieron crear las tablas relacionales"
        exit 1
    fi
    echo "Tablas creadas exitosamente!"
    echo ""
fi

echo "Instalando dependencias..."
pip install -q -r requirements.txt

echo ""
echo "========================================"
echo "Iniciando aplicación web mejorada..."
echo "========================================"
echo ""
echo "La aplicación se abrirá en: http://localhost:8501"
echo ""
echo "Presiona Ctrl+C para detener la aplicación"
echo ""

# Ejecutar la aplicación mejorada con BD relacional
streamlit run src/app_relacional.py

exit 0


