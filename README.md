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

### Paso 1: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Configurar API Key
Crear archivo `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "tu_clave_aqui"
```

### Paso 3: Ejecutar
```bash
streamlit run app_relacional.py
```

Accede a `http://localhost:8501`

## 📋 Estructura de Datos

**Base de Datos Relacional:**
- `db_usuarios.csv`: 1,540 usuarios verificados
- `db_productos.csv`: 50 prendas de moda exclusivas
- `db_calificaciones_completo.csv`: 1,017+ reseñas certificadas

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

Documentación completa disponible en **DOCUMENTACION.md**.

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
**app_relacional.py** - Aplicación Streamlit principal (1,277 líneas)

### Funciones Clave
- `load_relational_database()`: Carga datos
- `responder_con_groq()`: Procesa preguntas con IA
- `obtener_recomendaciones_svd()`: Calcula recomendaciones
- `mostrar_producto_grid()`: Renderiza tarjetas

## 🔐 Seguridad

- Procesamiento local de datos
- API Key en `secrets.toml` (no versionado)
- Sin almacenamiento externo
- Conexión segura a Groq

## 📞 Soporte

1. Consulta **DOCUMENTACION.md** para detalles técnicos
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

**Desarrollado con ❤️ usando Python, Streamlit e IA Groq**

*¡Disfruta tu experiencia LUXE ESSENCE!* 💎 

### **3) Model based Collaborative filtering**
Objective -
* Provide personalized recommendations to users based on their past behavior and preferences, while also addressing the challenges of sparsity and scalability that can arise in other collaborative filtering techniques.

Outputs -
* Recommend top 5 products for a particular user.

Approach -
* Taking the matrix of product ratings and converting it to a CSR(compressed sparse row) matrix. This is done to save memory and computational time, since only the non-zero values need to be stored.
* Performing singular value decomposition (SVD) on the sparse or csr matrix. SVD is a matrix decomposition technique that can be used to reduce the dimensionality of a matrix. In this case, the SVD is used to reduce the dimensionality of the matrix of product ratings to 50 latent features.
* Calculating the predicted ratings for all users using SVD. The predicted ratings are calculated by multiplying the U matrix, the sigma matrix, and the Vt matrix.
* Storing the predicted ratings in a DataFrame. The DataFrame has the same columns as the original matrix of product ratings. The rows of the DataFrame correspond to the users. The values in the DataFrame are the predicted ratings for each user.
* A funtion is written to recommend products based on the rating predictions made : 
  1. It gets the user's ratings from the interactions_matrix.
  2. It gets the user's predicted ratings from the preds_matrix.
  3. It creates a DataFrame with the user's actual and predicted ratings.
  4. It adds a column to the DataFrame with the product names.
  5. It filters the DataFrame to only include products that the user has not rated.
  6. It sorts the DataFrame by the predicted ratings in descending order.
  7. It prints the top num_recommendations products.
* Evaluating the model :
  1. Calculate the average rating for all the movies by dividing the sum of all the ratings by the number of ratings.
  2, Calculate the average rating for all the predicted ratings by dividing the sum of all the predicted ratings by the number of ratings.
  3. Create a DataFrame called rmse_df that contains the average actual ratings and the average predicted ratings.
  4. Calculate the RMSE of the SVD model by taking the square root of the mean of the squared errors between the average actual ratings and the average predicted ratings.

> The squared parameter in the mean_squared_error function determines whether to return the mean squared error (MSE) or the root mean squared error (RMSE). When squared is set to False, the function returns the RMSE, which is the square root of the MSE. In this case, you are calculating the RMSE, so you have set squared to False. This means that the errors are first squared, then averaged, and finally square-rooted to obtain the RMSE.
     

| ⚠️  This project is solely for learning how recommedation systems work. ⚠️ |
|-----------------------------------------------------------------------------|
