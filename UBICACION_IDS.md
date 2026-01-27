# 📍 Ubicación de IDs de Usuarios y Productos

## 🔍 Resumen

En la página de **"Recomendaciones por Usuarios Similares"**, ahora se muestran tanto los **índices numéricos** como los **IDs reales** de usuarios y productos.

---

## 👥 IDs de Usuarios

### Dónde se encuentran:

1. **En el Dataset Original (`ratings_Electronics.csv`):**
   - Columna: `user_id`
   - Ejemplos: `"A100UD67AHFODS"`, `"A100WO06OQR8BQ"`, `"A5JLAU2ARJ0BO"`

2. **En la Interfaz Web:**
   - **Índice de Usuario**: Número que seleccionas (0, 1, 2, 3, ...)
   - **ID de Usuario Real**: Se muestra automáticamente cuando seleccionas un índice
   - **Tabla de Usuarios Similares**: Muestra ambos (Índice e ID Real)

### Mapeo Índice → ID Real:

```
Índice 0  →  ID: "A100UD67AHFODS"
Índice 1  →  ID: "A100WO06OQR8BQ"
Índice 2  →  ID: "A105S56ODHGJEK"
Índice 3  →  ID: "A105TOJ6LTVMBG"
...
```

### Cómo se crea el mapeo:

```python
# En load_data():
user_id_mapping = final_ratings_matrix.index.tolist()  # Lista de user_ids originales
index_to_user_id = {i: user_id for i, user_id in enumerate(user_id_mapping)}
```

---

## 🛍️ IDs de Productos

### Dónde se encuentran:

1. **En el Dataset Original (`ratings_Electronics.csv`):**
   - Columna: `prod_id`
   - Ejemplos: `"B001TH7GUU"`, `"B003ES5ZUU"`, `"0594451647"`

2. **En la Interfaz Web:**
   - Se muestran **directamente** en las recomendaciones
   - Formato: `Producto ID: B001TH7GUU`

### Estructura:

Los IDs de productos se mantienen como están en el dataset original:
- No hay conversión a índices
- Se muestran directamente en las recomendaciones
- Están en las columnas de `final_ratings_matrix`

---

## 📊 Visualización en la Interfaz

### Sección: "Recomendaciones por Usuarios Similares"

```
👤 Usuario Actual: ID = A105TOJ6LTVMBG (Índice = 3)

🛍️ Productos Recomendados:
1. Producto ID: B001TAAVP4
   - Rating Promedio: 4.50 ⭐
   - Número de Ratings: 120

👥 Usuarios Similares:
┌─────────┬──────────────────────┬────────────┐
│ Índice  │ ID de Usuario Real   │ Similitud  │
├─────────┼──────────────────────┼────────────┤
│   320   │ A3OXHLG6DIBRW8       │   0.8562   │
│   12    │ ADLVFFE4VBT8         │   0.8549   │
│  793    │ A6FIAB28IS79         │   0.8509   │
└─────────┴──────────────────────┴────────────┘
```

---

## 🔧 Cómo Acceder a los IDs en el Código

### Obtener ID de Usuario desde Índice:

```python
# Si tienes el índice (ej: 3)
user_index = 3
real_user_id = index_to_user_id[user_index]
# Resultado: "A105TOJ6LTVMBG"
```

### Obtener Índice desde ID de Usuario:

```python
# Si tienes el ID real
user_id = "A105TOJ6LTVMBG"
user_index = user_id_to_index[user_id]
# Resultado: 3
```

### Obtener IDs de Productos:

```python
# Los IDs de productos están en las columnas de la matriz
product_ids = final_ratings_matrix.columns.tolist()
# O directamente desde las recomendaciones
recommendations_list = recommendations(user_index, 5, final_ratings_matrix)
# recommendations_list contiene los prod_ids directamente
```

---

## 📝 Notas Importantes

1. **Índices vs IDs:**
   - Los **índices** (0, 1, 2...) son para uso interno del algoritmo
   - Los **IDs reales** son los identificadores originales del dataset
   - La interfaz muestra ambos para mayor claridad

2. **Filtrado de Usuarios:**
   - Solo se incluyen usuarios con **50+ ratings**
   - Esto significa que no todos los usuarios del dataset original están disponibles
   - El mapeo solo incluye usuarios activos

3. **Productos:**
   - Todos los productos están disponibles
   - No hay filtrado de productos
   - Los IDs se muestran directamente

---

## 🗂️ Estructura de Datos

### Variables Clave:

```python
# Mapeo Índice → ID Real
index_to_user_id = {
    0: "A100UD67AHFODS",
    1: "A100WO06OQR8BQ",
    2: "A105S56ODHGJEK",
    ...
}

# Mapeo ID Real → Índice
user_id_to_index = {
    "A100UD67AHFODS": 0,
    "A100WO06OQR8BQ": 1,
    "A105S56ODHGJEK": 2,
    ...
}

# IDs de Productos (en columnas)
final_ratings_matrix.columns
# Index(['0594451647', '0594481813', '0970407998', ..., 'B00LKG1MC8'])
```

---

## 💡 Ejemplo de Uso

Si quieres buscar un usuario específico:

1. **Por ID Real:**
   ```python
   user_id = "A5JLAU2ARJ0BO"
   if user_id in user_id_to_index:
       user_index = user_id_to_index[user_id]
       # Usar user_index para obtener recomendaciones
   ```

2. **Por Índice:**
   ```python
   user_index = 3
   real_user_id = index_to_user_id[user_index]
   # Obtener recomendaciones para este usuario
   ```

---

## 🔍 Verificación

Para verificar qué usuarios están disponibles:

```python
# Ver todos los IDs de usuarios disponibles
print("Total de usuarios:", len(index_to_user_id))
print("Primeros 10 usuarios:")
for idx in range(10):
    print(f"Índice {idx}: {index_to_user_id[idx]}")
```

---

¡Ahora puedes ver claramente tanto los índices como los IDs reales en la interfaz! 🎉

