# 🌐 Interfaz Web - Sistema de Recomendación E-commerce

## 📋 Descripción

Esta es una interfaz web interactiva desarrollada con **Streamlit** que permite utilizar el sistema de recomendación de productos basado en los análisis del cuaderno Jupyter.

## 🚀 Instalación y Uso

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 🎯 Funcionalidades

### 1. **Inicio** 🏠
- Vista general del sistema
- Estadísticas básicas del dataset
- Información sobre los métodos de recomendación disponibles

### 2. **Estadísticas** 📈
- Distribución de ratings
- Resumen estadístico del dataset
- Top 10 usuarios con más ratings
- Top 10 productos mejor calificados

### 3. **Recomendaciones por Ranking** ⭐
- Productos más populares basados en rating promedio
- Filtro por número mínimo de interacciones
- Ideal para nuevos usuarios (Cold Start Problem)

### 4. **Recomendaciones por Usuarios Similares** 👥
- Filtrado colaborativo basado en usuarios
- Encuentra usuarios con gustos similares
- Recomienda productos que usuarios similares han calificado positivamente

### 5. **Recomendaciones SVD** 🤖
- Descomposición de Valores Singulares
- Técnica avanzada de reducción de dimensionalidad
- Predice ratings para productos no vistos por el usuario

## 🔧 Cómo Funciona

### Arquitectura del Sistema

```
app.py
├── Carga de Datos (@st.cache_data)
│   └── Filtrado de usuarios activos (50+ ratings)
│   └── Creación de matriz de interacciones
│
├── Sistema de Recomendación por Ranking
│   └── top_n_products()
│       └── Filtra por mínimo de interacciones
│       └── Ordena por rating promedio
│
├── Sistema de Recomendación Colaborativo
│   ├── similar_users()
│   │   └── Calcula similitud coseno entre usuarios
│   └── recommendations()
│       └── Encuentra productos de usuarios similares
│
└── Sistema de Recomendación SVD
    ├── get_svd_recommendations()
    │   └── Descompone matriz en U, Σ, Vt
    │   └── Reconstruye matriz con k=50 factores latentes
    └── recommend_items_svd()
        └── Predice ratings para productos no vistos
```

### Explicación Detallada de Cada Método

#### 1. **Recomendaciones por Ranking** ⭐

**¿Cómo funciona?**
- Calcula el rating promedio de cada producto
- Cuenta cuántas veces ha sido calificado cada producto
- Filtra productos con un mínimo de interacciones (para evitar productos con solo 1 rating de 5 estrellas)
- Ordena por rating promedio descendente

**Ventajas:**
- ✅ Simple y rápido
- ✅ Funciona para nuevos usuarios (Cold Start)
- ✅ No requiere historial del usuario

**Desventajas:**
- ❌ No personalizado
- ❌ Todos los usuarios ven las mismas recomendaciones

**Código clave:**
```python
def top_n_products(final_rating, n, min_interaction):
    recommendations = final_rating[final_rating['rating_count'] > min_interaction]
    recommendations = recommendations.sort_values('avg_rating', ascending=False)
    return recommendations.index[:n].tolist()
```

#### 2. **Recomendaciones por Usuarios Similares** 👥

**¿Cómo funciona?**
1. **Cálculo de Similitud:**
   - Compara el vector de ratings del usuario objetivo con todos los demás usuarios
   - Usa similitud coseno: `cos(θ) = (A·B) / (||A|| × ||B||)`
   - Valores cercanos a 1 = usuarios muy similares

2. **Selección de Usuarios Similares:**
   - Ordena usuarios por similitud descendente
   - Selecciona los más similares

3. **Generación de Recomendaciones:**
   - Encuentra productos que usuarios similares han calificado
   - Excluye productos que el usuario ya ha visto
   - Retorna los productos más relevantes

**Ventajas:**
- ✅ Personalizado para cada usuario
- ✅ Descubre productos nuevos basados en gustos similares
- ✅ Funciona bien con suficiente historial

**Desventajas:**
- ❌ No funciona para nuevos usuarios (Cold Start)
- ❌ Computacionalmente costoso con muchos usuarios
- ❌ Puede crear "burbujas de filtro"

**Código clave:**
```python
def similar_users(user_index, interactions_matrix):
    # Calcula similitud coseno entre usuarios
    sim = cosine_similarity(
        [interactions_matrix.loc[user_index]], 
        [interactions_matrix.loc[user]]
    )
    return most_similar_users, similarity_scores
```

#### 3. **Recomendaciones SVD** 🤖

**¿Cómo funciona?**
1. **Descomposición SVD:**
   - Descompone la matriz de ratings (usuarios × productos) en tres matrices:
     - **U**: Representación de usuarios en espacio latente
     - **Σ**: Valores singulares (importancia de cada factor)
     - **Vt**: Representación de productos en espacio latente
   - Usa k=50 factores latentes (dimensiones reducidas)

2. **Reconstrucción:**
   - Multiplica U × Σ × Vt para obtener predicciones
   - Esto "completa" los ratings faltantes

3. **Recomendaciones:**
   - Para cada usuario, predice ratings de productos no vistos
   - Ordena por rating predicho descendente

**Ventajas:**
- ✅ Maneja bien matrices dispersas (muchos valores faltantes)
- ✅ Captura patrones complejos en los datos
- ✅ Eficiente computacionalmente después del entrenamiento
- ✅ Puede funcionar mejor que filtrado colaborativo simple

**Desventajas:**
- ❌ Requiere tiempo de procesamiento inicial
- ❌ Menos interpretable (factores latentes no tienen significado claro)
- ❌ Puede requerir ajuste de hiperparámetros (k)

**Código clave:**
```python
# Descomposición SVD
U, s, Vt = svds(final_ratings_sparse, k=50)
sigma = np.diag(s)

# Reconstrucción y predicción
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt)
```

### Flujo de Datos

```
Dataset CSV
    ↓
Carga y Preprocesamiento
    ↓
Matriz de Interacciones (usuarios × productos)
    ↓
┌─────────────────┬──────────────────┬──────────────┐
│ Ranking         │ Colaborativo     │ SVD          │
│ (Popularidad)   │ (Usuarios Sim.)  │ (Factores)   │
└─────────────────┴──────────────────┴──────────────┘
    ↓                    ↓                    ↓
Recomendaciones    Recomendaciones    Recomendaciones
```

## 📊 Estructura de Datos

### Matriz de Interacciones
```
        Producto1  Producto2  Producto3  ...
Usuario1    5.0       0.0       4.0
Usuario2    0.0       3.0       0.0
Usuario3    4.0       5.0       0.0
...
```
- Valores: Ratings (1-5) o 0 si no hay interacción
- Muy dispersa: La mayoría de valores son 0

### DataFrame de Ratings Final
```
prod_id    avg_rating    rating_count
B001...       4.8            150
B002...       4.5            89
...
```

## 🎨 Características de la Interfaz

- **Streamlit**: Framework Python para crear aplicaciones web rápidamente
- **Caché de Datos**: `@st.cache_data` acelera la carga de datos
- **Interfaz Interactiva**: Widgets para seleccionar parámetros
- **Visualizaciones**: Gráficos y tablas para entender los datos
- **Diseño Responsivo**: Se adapta a diferentes tamaños de pantalla

## 🔍 Parámetros Importantes

### Recomendaciones por Ranking
- **Número de productos**: Cuántos productos mostrar
- **Mínimo de interacciones**: Filtra productos con pocos ratings (evita sesgo)

### Recomendaciones Colaborativas
- **ID de Usuario**: Índice del usuario (0 a número de usuarios - 1)
- **Número de productos**: Cuántos productos recomendar

### Recomendaciones SVD
- **ID de Usuario**: Índice del usuario
- **Número de productos**: Cuántos productos recomendar
- **k (factores latentes)**: Fijado en 50 (puede ajustarse en el código)

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo"
- Verifica que `ratings_Electronics.csv` esté en la ruta correcta
- Actualiza la ruta en `app.py` línea 30

### Error: "Memory Error"
- El dataset es grande, considera usar un subconjunto
- Reduce el número de usuarios activos (cambia el umbral de 50)

### La aplicación es lenta
- SVD toma tiempo en calcularse la primera vez
- Usa `@st.cache_data` para cachear resultados
- Considera pre-calcular modelos y guardarlos

## 📈 Mejoras Futuras

- [ ] Guardar modelos pre-entrenados (pickle)
- [ ] Agregar búsqueda de productos por nombre
- [ ] Visualización de gráficos de similitud
- [ ] Sistema de evaluación de recomendaciones
- [ ] Soporte para nuevos usuarios (Cold Start mejorado)
- [ ] Integración con base de datos
- [ ] Sistema de autenticación de usuarios

## 📚 Referencias

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Collaborative Filtering](https://en.wikipedia.org/wiki/Collaborative_filtering)
- [Singular Value Decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition)


