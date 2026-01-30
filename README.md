# 💎 LUXE ESSENCE - Sistema de Recomendación Premium

## 🎯 Descripción

**LUXE ESSENCE** es un sistema inteligente de recomendación de productos de moda con interfaz premium. Utiliza algoritmos de aprendizaje automático, inteligencia artificial conversacional y análisis profundos para proporcionar recomendaciones personalizadas.

### ✨ Características Principales

- **Chat IA Flotante**: Asistente inteligente disponible 24/7 en esquina inferior derecha
- **Búsqueda Avanzada**: 50 prendas de moda seleccionadas con filtros flexibles
- **Recomendaciones Personalizadas**: Basadas en algoritmos de filtrado colaborativo
- **Análisis de Tendencias**: 4 tipos de insights inteligentes
- **Interfaz Premium**: Tema oscuro elegante con acentos dorados
- **Datos en Tiempo Real**: Estadísticas y métricas actualizadas

## 🚀 Instalación Rápida

### Opción 1: Usando Scripts Automáticos
```bash
# Para Windows
scripts\run_app.bat

# Para Linux/Mac
./scripts/run_app.sh
```

### Opción 2: Instalación Manual

#### Paso 1: Instalar dependencias
```bash
pip install -r requirements.txt
```

#### Paso 2: Configurar API Key
Crear archivo `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "tu_clave_aqui"
```

#### Paso 3: Ejecutar
```bash
streamlit run src/app_relacional.py
```

Accede a `http://localhost:8501`

## 📋 Estructura del Proyecto

```
Ecommerce-product-recommendation-system/
├── src/                    # Código fuente
│   └── app_relacional.py   # Aplicación principal
├── data/                   # Datos del sistema
│   ├── db_usuarios.csv     # 1,540 usuarios verificados
│   ├── db_productos.csv    # 50 prendas de moda exclusivas
│   └── db_calificaciones_completo.csv  # 1,017+ reseñas
├── docs/                   # Documentación
│   ├── DOCUMENTACION.md
│   └── DOCUMENTACION_FINAL.md
├── notebooks/              # Cuadernos Jupyter
│   ├── ECommerce_Product_Recommendation_System.ipynb
│   ├── Model_based_collaborative_filtering.ipynb
│   └── rank_based_product_recommendation.ipynb
├── scripts/                # Scripts de ejecución
│   ├── run_app.bat         # Para Windows
│   └── run_app.sh          # Para Linux/Mac
├── .streamlit/             # Configuración Streamlit
├── requirements.txt        # Dependencias Python
├── README.md              # Este archivo
└── LICENSE                # Licencia del proyecto
```

## 🧠 Algoritmos de Recomendación

### 1. Filtrado Colaborativo Basado en Usuarios
Encuentra usuarios similares y recomienda productos que compraron.
- Similitud por coseno
- Top 5 usuarios similares
- Filtra compras previas

### 2. Descomposición SVD (Matriz Factorización)
Predice ratings usando factores latentes.
- 30 dimensiones
- Mayor precisión
- Mejora con más datos

## 📚 Documentación

Documentación completa disponible en `docs/DOCUMENTACION_FINAL.md`.

Incluye:
- Guía de instalación detallada
- Estructura técnica
- Troubleshooting
- API Key setup

## 🎨 Tecnologías Utilizadas

- **Frontend**: Streamlit
- **Backend**: Python 3.9+
- **Machine Learning**: Scikit-Learn
- **Inteligencia Artificial**: Groq API
- **Bases de Datos**: CSV (relacional)

## 📊 Estadísticas del Sistema

| Métrica | Valor |
|---------|-------|
| Usuarios Registrados | 1,540 |
| Prendas Disponibles | 50 |
| Reseñas Totales | 1,017+ |
| Rating Promedio | 4.3/5 ⭐ |
| Rango de Precios | $10 - $299 |

## 💬 Chat IA

Presiona el botón 💬 en la esquina inferior derecha para:
- Preguntar sobre moda y tendencias
- Obtener recomendaciones personalizadas
- Analizar productos específicos
- Resolver dudas sobre el catálogo

## 🔧 Configuración Técnica

### Página Principal
**src/app_relacional.py** - Aplicación Streamlit principal (1,277 líneas)

### Funciones Clave
- `load_relational_database()`: Carga datos desde `data/`
- `responder_con_groq()`: Procesa preguntas con IA
- `obtener_recomendaciones_svd()`: Calcula recomendaciones
- `mostrar_producto_grid()`: Renderiza tarjetas

## 🔐 Seguridad

- Procesamiento local de datos
- API Key en `secrets.toml` (no versionado)
- Sin almacenamiento externo
- Conexión segura a Groq

## 📞 Soporte

1. Consulta `docs/DOCUMENTACION_FINAL.md` para detalles técnicos
2. Revisa los logs en terminal
3. Verifica la validez de tu API Key
4. Comprueba la conexión a internet

## 📝 Historial de Versiones

### v2.0 - Premium Redesign (ACTUAL)
✅ Chat flotante en esquina inferior derecha
✅ Rebranding a "LUXE ESSENCE"
✅ Código optimizado y limpio
✅ Documentación consolidada
✅ Tema premium oscuro + oro

### v1.0 - Base Original
- Algoritmos de recomendación
- Interface básica
- Integración IA Google Gemini

---

**Desarrollado con ❤️ usando Python, Streamlit e IA Groq
luis Ahumada -- Alcibiades Lopez**


*¡Disfruta tu experiencia LUXE ESSENCE!* 💎 


