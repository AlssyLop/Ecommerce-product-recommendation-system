#!/bin/bash

echo "========================================"
echo "Sistema de Recomendación E-commerce"
echo "========================================"
echo ""
echo "Instalando dependencias..."
pip install -r requirements.txt
echo ""
echo "Iniciando aplicación web..."
streamlit run app.py


