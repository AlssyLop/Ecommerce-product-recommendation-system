# LUXE ESSENCE - Documentación Final del Proyecto

## Introducción

LUXE ESSENCE es un sistema inteligente de recomendación de productos de moda. Utiliza algoritmos de aprendizaje automático para ofrecer sugerencias personalizadas a cada usuario.

---

## Requisitos Técnicos

- Python 3.9+
- Streamlit: Para la interfaz web
- Pandas/NumPy: Procesamiento de datos
- Scikit-Learn: Algoritmos de recomendación
- Groq API: Inteligencia artificial para chat

---

## Instalación y Ejecución

### 1. Configurar Entorno Virtual
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar API Key
Crear archivo `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "tu_clave_aqui"
```

### 4. Ejecutar Aplicación
```bash
# Opción 1: Usando script
./scripts/run_app.sh  # Linux/Mac
# o
scripts\run_app.bat   # Windows

# Opción 2: Manual
streamlit run src/app_relacional.py
```

Accede a: `http://localhost:8501`

---

## Estructura de Datos

### Base de Datos

data/db_usuarios.csv (1,540 usuarios)
- user_id: Identificador único
- nombre: Nombre del usuario
- email: Correo electrónico
- país: País de residencia

data/db_productos.csv (50 prendas)
- prod_id: ID del producto
- nombre: Nombre del artículo
- marca: Marca/fabricante
- precio: Precio en centavos (USD)
- imagen_url: URL de imagen
- cantidad_resenas: Total de reseñas
- categoria: Categoría de la prenda

data/db_calificaciones_completo.csv (1,017+ reseñas)
- usuario_id: ID del usuario
- prod_id: ID del producto
- calificacion: Puntuación 1-5
- fecha: Fecha de reseña

---

## Características Principales

### 1. Página de Inicio
- Bienvenida con estadísticas en tiempo real
- Métricas principales (usuarios, productos, reseñas)
- Descripción de características
- Categorías de moda

### 2. Búsqueda de Productos
- Búsqueda por nombre o marca
- Desplegable con 50 productos
- Ordenamiento flexible (precio, popularidad)
- Visualización en grid premium

### 3. Estadísticas
- Rating promedio del catálogo
- Distribución de precios
- Análisis de reseñas
- Top 8 productos más vendidos

### 4. Top Productos
- Filtros dinámicos (cantidad, mínimo de reseñas)
- Visualización mejorada con detalles
- Información completa de cada artículo

### 5. Recomendaciones Personalizadas
- Sistema basado en usuarios similares
- Análisis de patrones de compra
- Sugerencias exclusivas por perfil

### 6. IA Insights
Análisis profundo con 4 apartados:
- Tendencias de Ventas: Evolución y patrones
- Análisis de Ratings: Satisfacción por producto
- Análisis de Precios: Rango y distribución
- Recomendaciones Smart: Insights personalizados

### 7. Chat IA Flotante
- Asistente disponible 24/7
- Responde preguntas sobre moda, productos y tendencias
- Interfaz conversacional natural
- Histórico de conversación

---

## Algoritmos de Recomendación

### 1. Filtrado Colaborativo Basado en Usuarios
```
Encuentra usuarios similares → Recomienda items que ellos compraron
```
- Similitud por coseno en la matriz usuario-producto
- Top 5 usuarios similares
- Filtra items ya comprados

### 2. Filtrado Colaborativo Basado en Modelos
```
Descomposición SVD → Factores latentes → Predicciones
```
- Matriz de factorización (30 dimensiones)
- Mayor precisión en datos dispersos
- Mejora con dataset completo

---

## Guía de Uso

### Para Usuarios Finales

1. Explorar Productos
   - Inicio: Ver estadísticas y categorías
   - Búsqueda: Filtrar por nombre, marca o categoría

2. Analizar Tendencias
   - Estadísticas: Gráficos y métricas del catálogo
   - Top Productos: Ver éxitos de ventas

3. Obtener Recomendaciones
   - Mis Recomendaciones: Ver sugerencias personalizadas
   - IA Insights: Análisis profundos e inteligentes

4. Conversar con IA
   - Usa el botón en la esquina inferior derecha
   - Pregunta sobre moda, productos o recomendaciones
   - La IA responde con contexto sobre tu perfil

### Para Administradores

1. Actualizar Datos
   - Modificar CSVs en la carpeta data/
   - La app carga automáticamente los nuevos datos

2. Agregar Productos
   - Añadir filas a data/db_productos.csv
   - Incluir imagen_url (puede ser URL externa)

3. Gestionar Reseñas
   - Importar calificaciones a data/db_calificaciones_completo.csv
   - Formato: usuario_id, prod_id, calificacion (1-5), fecha

---

## Diseño y Tema

- Color Principal: Oro Premium (#d4af37)
- Fondo: Gradiente oscuro (#0f0f0f → #1a1a1a)
- Tipografía: Segoe UI, elegante y moderna
- Animaciones: Transiciones suaves y efectos hover
- Diseño Responsivo: Funciona en desktop y tablets

---

## Configuración Técnica

### Archivo Principal: src/app_relacional.py

Funciones Clave:
- load_data(): Carga las 3 bases de datos CSV desde data/
- responder_con_groq(): Procesa preguntas con IA Groq
- get_user_recommendations(): Calcula recomendaciones personalizadas
- mostrar_producto_grid(): Renderiza tarjetas de productos

Flujo Principal:
1. Cargar datos
2. Inicializar estado de sesión
3. Mostrar sidebar con navegación
4. Renderizar página según selección
5. Mostrar chat flotante (si está abierto)

### Variables de Sesión
```python
st.session_state.chat_history    # Historial de chat
st.session_state.chat_abierto    # Si el chat está visible
st.session_state.selected_product # Producto seleccionado
```

---

## Troubleshooting

### "API Key no configurada"
- Crear .streamlit/secrets.toml con tu clave de Groq
- Formato: GROQ_API_KEY = "gsk_..."

### Chat no responde
- Verificar conexión a internet
- Comprobar validez de API Key
- Revisar logs en terminal

### Datos no se cargan
- Verificar que CSVs están en el directorio data/
- Nombres deben ser exactos (case-sensitive)
- Formato CSV debe estar correcto

---

## Estadísticas del Sistema

- Usuarios Registrados: 1,540
- Productos Disponibles: 50
- Reseñas Totales: 1,017+
- Promedio de Rating: 4.3/5.0
- Rango de Precios: $10 - $299

---

## Seguridad y Privacidad

- Los datos se procesan localmente
- API Key almacenada en secrets.toml (no versionado)
- Sin almacenamiento de datos en servidores externos
- Solo conexión a Groq para procesar lenguaje natural

---

## Cambios Recientes

### v2.0 - Premium Redesign
- Nuevo tema oscuro con acentos dorados
- Chat flotante en esquina inferior derecha
- Branding "LUXE ESSENCE"
- Mejora en velocidad de respuesta
- Interface más intuitiva

---

## Soporte

Para problemas o sugerencias:
1. Revisar esta documentación
2. Verificar logs en la terminal
3. Consultar archivos CSV de datos
4. Comprobar conexión a internet y API

---

Desarrollado con ❤️ usando Python, Streamlit e IA Groq