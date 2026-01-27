"""
Sistema de Recomendación de Productos E-commerce
Interfaz Web basada en Streamlit
"""

import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from pathlib import Path

# Importar funciones de sklearn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Recomendación E-commerce",
    page_icon="🛍️",
    layout="wide"
)

# Título principal
st.title("🛍️ Sistema de Recomendación de Productos E-commerce")
st.markdown("---")

# Función para cargar datos
@st.cache_data
def load_data():
    """Carga el dataset de ratings"""
    try:
        # Intentar cargar desde la ruta del proyecto
        data_path = Path(__file__).parent / 'ratings_Electronics.csv'
        if not data_path.exists():
            st.error(f"❌ No se encontró el archivo en: {data_path}")
            st.info("Por favor, asegúrate de que el archivo ratings_Electronics.csv esté en la carpeta del proyecto")
            return None, None, None, None, None
        
        df = pd.read_csv(data_path, header=None)
        df.columns = ['user_id', 'prod_id', 'rating', 'timestamp']
        df = df.drop('timestamp', axis=1)
        
        # Filtrar usuarios con 50+ ratings
        counts = df['user_id'].value_counts()
        df_final = df[df['user_id'].isin(counts[counts >= 50].index)]
        
        # Crear matriz de ratings
        final_ratings_matrix = df_final.pivot(
            index='user_id', 
            columns='prod_id', 
            values='rating'
        ).fillna(0)
        
        # Guardar mapeo entre índices numéricos y user_ids reales
        user_id_mapping = final_ratings_matrix.index.tolist()  # Lista de user_ids originales
        index_to_user_id = {i: user_id for i, user_id in enumerate(user_id_mapping)}
        user_id_to_index = {user_id: i for i, user_id in enumerate(user_id_mapping)}
        
        # Crear índices numéricos para usuarios
        final_ratings_matrix['user_index'] = np.arange(0, final_ratings_matrix.shape[0])
        final_ratings_matrix.set_index(['user_index'], inplace=True)
        
        # Calcular ratings promedio por producto
        average_rating = df_final.groupby("prod_id")['rating'].mean()
        count_rating = df_final.groupby('prod_id')['rating'].count()
        final_rating = pd.DataFrame({
            'avg_rating': average_rating, 
            'rating_count': count_rating
        })
        final_rating = final_rating.sort_values(by='avg_rating', ascending=False)
        
        return df, df_final, final_ratings_matrix, final_rating, counts, index_to_user_id, user_id_to_index
        
    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {str(e)}")
        return None, None, None, None, None, None, None

# Función para recomendaciones basadas en ranking
def top_n_products(final_rating, n, min_interaction):
    """Obtiene los top n productos basados en rating promedio y mínimo de interacciones"""
    recommendations = final_rating[final_rating['rating_count'] > min_interaction]
    recommendations = recommendations.sort_values('avg_rating', ascending=False)
    return recommendations.index[:n].tolist()

# Función para encontrar usuarios similares
def similar_users(user_index, interactions_matrix):
    """Encuentra usuarios similares usando similitud coseno"""
    similarity = []
    for user in range(0, interactions_matrix.shape[0]):
        sim = cosine_similarity(
            [interactions_matrix.loc[user_index]], 
            [interactions_matrix.loc[user]]
        )
        similarity.append((user, sim[0][0]))
    
    similarity.sort(key=lambda x: x[1], reverse=True)
    most_similar_users = [tup[0] for tup in similarity]
    similarity_score = [tup[1] for tup in similarity]
    
    most_similar_users.remove(user_index)
    similarity_score.remove(similarity_score[0])
    
    return most_similar_users, similarity_score

# Función para recomendaciones basadas en usuarios similares
def recommendations(user_index, num_of_products, interactions_matrix):
    """Recomienda productos basándose en usuarios similares"""
    most_similar_users = similar_users(user_index, interactions_matrix)[0]
    prod_ids = set(list(interactions_matrix.columns[
        np.where(interactions_matrix.loc[user_index] > 0)
    ]))
    recommendations_list = []
    observed_interactions = prod_ids.copy()
    
    for similar_user in most_similar_users:
        if len(recommendations_list) < num_of_products:
            similar_user_prod_ids = set(list(interactions_matrix.columns[
                np.where(interactions_matrix.loc[similar_user] > 0)
            ]))
            recommendations_list.extend(
                list(similar_user_prod_ids.difference(observed_interactions))
            )
            observed_interactions = observed_interactions.union(similar_user_prod_ids)
        else:
            break
    
    return recommendations_list[:num_of_products]

# Función para recomendaciones basadas en SVD
@st.cache_data
def get_svd_recommendations(final_ratings_matrix, k=50):
    """Calcula recomendaciones usando SVD"""
    final_ratings_sparse = csr_matrix(final_ratings_matrix.values)
    U, s, Vt = svds(final_ratings_sparse, k=k)
    sigma = np.diag(s)
    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt)
    preds_df = pd.DataFrame(
        abs(all_user_predicted_ratings), 
        columns=final_ratings_matrix.columns
    )
    preds_matrix = csr_matrix(preds_df.values)
    return final_ratings_sparse, preds_matrix

def recommend_items_svd(user_index, interactions_matrix, preds_matrix, num_recommendations):
    """Recomienda productos usando SVD"""
    user_ratings = interactions_matrix[user_index, :].toarray().reshape(-1)
    user_predictions = preds_matrix[user_index, :].toarray().reshape(-1)
    
    temp = pd.DataFrame({
        'user_ratings': user_ratings, 
        'user_predictions': user_predictions
    })
    temp['Recommended Products'] = np.arange(len(user_ratings))
    temp = temp.set_index('Recommended Products')
    temp = temp.loc[temp.user_ratings == 0]
    temp = temp.sort_values('user_predictions', ascending=False)
    
    return temp['user_predictions'].head(num_recommendations)

# Cargar datos
with st.spinner("🔄 Cargando datos..."):
    df, df_final, final_ratings_matrix, final_rating, counts, index_to_user_id, user_id_to_index = load_data()

if df is not None:
    # Sidebar para navegación
    st.sidebar.title("📊 Navegación")
    page = st.sidebar.selectbox(
        "Selecciona una sección:",
        ["🏠 Inicio", "📈 Estadísticas", "⭐ Recomendaciones por Ranking", 
         "👥 Recomendaciones por Usuarios Similares", "🤖 Recomendaciones SVD"]
    )
    
    if page == "🏠 Inicio":
        st.header("Bienvenido al Sistema de Recomendación")
        st.markdown("""
        Este sistema utiliza tres métodos diferentes para recomendar productos:
        
        1. **Recomendaciones por Ranking**: Productos más populares basados en ratings promedio
        2. **Recomendaciones por Usuarios Similares**: Basado en filtrado colaborativo
        3. **Recomendaciones SVD**: Usando descomposición de valores singulares
        
        ### 📊 Datos del Sistema
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Ratings", f"{len(df):,}")
        with col2:
            st.metric("Usuarios Activos", f"{df_final['user_id'].nunique():,}")
        with col3:
            st.metric("Productos", f"{df_final['prod_id'].nunique():,}")
    
    elif page == "📈 Estadísticas":
        st.header("📈 Estadísticas del Dataset")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribución de Ratings")
            rating_dist = df['rating'].value_counts().sort_index()
            st.bar_chart(rating_dist)
        
        with col2:
            st.subheader("Resumen Estadístico")
            st.dataframe(df['rating'].describe())
        
        st.subheader("Top 10 Usuarios con Más Ratings")
        top_users = df.groupby('user_id').size().sort_values(ascending=False)[:10]
        st.dataframe(top_users.reset_index().rename(columns={0: 'Número de Ratings'}))
        
        st.subheader("Top 10 Productos Mejor Calificados")
        st.dataframe(final_rating.head(10))
    
    elif page == "⭐ Recomendaciones por Ranking":
        st.header("⭐ Recomendaciones Basadas en Popularidad")
        st.markdown("Obtén los productos más populares basados en su rating promedio")
        
        col1, col2 = st.columns(2)
        with col1:
            n_products = st.number_input("Número de productos a recomendar", 
                                       min_value=1, max_value=50, value=5)
        with col2:
            min_interactions = st.number_input("Mínimo de interacciones requeridas", 
                                             min_value=1, max_value=500, value=50)
        
        if st.button("🔍 Obtener Recomendaciones"):
            recommendations_list = top_n_products(final_rating, n_products, min_interactions)
            if recommendations_list:
                st.success(f"✅ Se encontraron {len(recommendations_list)} productos")
                for i, prod_id in enumerate(recommendations_list, 1):
                    rating_info = final_rating.loc[prod_id]
                    st.markdown(f"""
                    **{i}. Producto: {prod_id}**
                    - Rating Promedio: {rating_info['avg_rating']:.2f} ⭐
                    - Número de Ratings: {int(rating_info['rating_count'])}
                    """)
            else:
                st.warning("⚠️ No se encontraron productos con los criterios especificados")
    
    elif page == "👥 Recomendaciones por Usuarios Similares":
        st.header("👥 Recomendaciones Basadas en Usuarios Similares")
        st.markdown("Encuentra productos recomendados basándote en usuarios con gustos similares")
        
        max_user_index = final_ratings_matrix.shape[0] - 1
        
        # Mostrar información sobre el usuario seleccionado
        col1, col2 = st.columns(2)
        with col1:
            user_index = st.number_input(
                "Índice de Usuario", 
                min_value=0, 
                max_value=max_user_index, 
                value=3,
                help=f"Selecciona un índice de usuario entre 0 y {max_user_index}"
            )
            if index_to_user_id:
                current_user_id = index_to_user_id.get(user_index, "N/A")
                st.info(f"**ID de Usuario Real:** {current_user_id}")
        
        with col2:
            num_products = st.number_input(
                "Número de productos a recomendar", 
                min_value=1, 
                max_value=20, 
                value=5
            )
        
        if st.button("🔍 Obtener Recomendaciones"):
            with st.spinner("Calculando usuarios similares..."):
                recommendations_list = recommendations(
                    user_index, 
                    num_products, 
                    final_ratings_matrix
                )
            
            if recommendations_list:
                # Mostrar información del usuario actual
                if index_to_user_id:
                    current_user_id = index_to_user_id.get(user_index, "N/A")
                    st.info(f"👤 **Usuario Actual:** ID = {current_user_id} (Índice = {user_index})")
                
                st.success(f"✅ Se encontraron {len(recommendations_list)} productos recomendados")
                st.subheader("🛍️ Productos Recomendados")
                for i, prod_id in enumerate(recommendations_list, 1):
                    if prod_id in final_rating.index:
                        rating_info = final_rating.loc[prod_id]
                        st.markdown(f"""
                        **{i}. Producto ID: {prod_id}**
                        - Rating Promedio: {rating_info['avg_rating']:.2f} ⭐
                        - Número de Ratings: {int(rating_info['rating_count'])}
                        """)
                    else:
                        st.markdown(f"**{i}. Producto ID: {prod_id}**")
                
                # Mostrar usuarios similares con IDs reales
                st.subheader("👥 Usuarios Similares")
                similar_users_list, similarity_scores = similar_users(
                    user_index, 
                    final_ratings_matrix
                )
                
                # Crear DataFrame con IDs reales
                similar_data = []
                for idx, (similar_index, score) in enumerate(zip(similar_users_list[:10], similarity_scores[:10])):
                    real_user_id = index_to_user_id.get(similar_index, "N/A") if index_to_user_id else similar_index
                    similar_data.append({
                        'Índice': similar_index,
                        'ID de Usuario Real': real_user_id,
                        'Similitud': float(score)
                    })
                
                similar_df = pd.DataFrame(similar_data)
                st.dataframe(similar_df, use_container_width=True)
                
                # Información adicional
                with st.expander("ℹ️ Información sobre los IDs"):
                    st.markdown("""
                    - **Índice**: Número de posición en la matriz (0, 1, 2, ...)
                    - **ID de Usuario Real**: Identificador único del usuario en el dataset original
                    - **ID de Producto**: Identificador único del producto (se muestra directamente)
                    - **Similitud**: Valor entre 0 y 1, donde 1 = usuarios idénticos
                    """)
            else:
                st.warning("⚠️ No se encontraron recomendaciones para este usuario")
    
    elif page == "🤖 Recomendaciones SVD":
        st.header("🤖 Recomendaciones usando SVD (Descomposición de Valores Singulares)")
        st.markdown("Recomendaciones avanzadas usando técnicas de reducción de dimensionalidad")
        
        max_user_index = final_ratings_matrix.shape[0] - 1
        
        col1, col2 = st.columns(2)
        with col1:
            user_index = st.number_input(
                "Índice de Usuario", 
                min_value=0, 
                max_value=max_user_index, 
                value=100,
                help=f"Selecciona un índice de usuario entre 0 y {max_user_index}"
            )
            if index_to_user_id:
                current_user_id = index_to_user_id.get(user_index, "N/A")
                st.info(f"**ID de Usuario Real:** {current_user_id}")
        
        with col2:
            num_products = st.number_input(
                "Número de productos a recomendar", 
                min_value=1, 
                max_value=20, 
                value=10
            )
        
        num_products = st.number_input(
            "Número de productos a recomendar", 
            min_value=1, 
            max_value=20, 
            value=10
        )
        
        if st.button("🔍 Obtener Recomendaciones SVD"):
            # Mostrar información del usuario actual
            if index_to_user_id:
                current_user_id = index_to_user_id.get(user_index, "N/A")
                st.info(f"👤 **Usuario Actual:** ID = {current_user_id} (Índice = {user_index})")
            
            with st.spinner("Calculando recomendaciones con SVD (esto puede tomar unos momentos)..."):
                final_ratings_sparse, preds_matrix = get_svd_recommendations(final_ratings_matrix)
                recommendations_svd = recommend_items_svd(
                    user_index, 
                    final_ratings_sparse, 
                    preds_matrix, 
                    num_products
                )
            
            if len(recommendations_svd) > 0:
                st.success(f"✅ Se encontraron {len(recommendations_svd)} productos recomendados")
                st.subheader("🛍️ Productos Recomendados (ordenados por score predicho)")
                
                for idx, (prod_idx, score) in enumerate(recommendations_svd.items(), 1):
                    prod_id = final_ratings_matrix.columns[int(prod_idx)]
                    if prod_id in final_rating.index:
                        rating_info = final_rating.loc[prod_id]
                        st.markdown(f"""
                        **{idx}. Producto ID: {prod_id}**
                        - Score Predicho: {score:.4f}
                        - Rating Promedio: {rating_info['avg_rating']:.2f} ⭐
                        - Número de Ratings: {int(rating_info['rating_count'])}
                        """)
                    else:
                        st.markdown(f"""
                        **{idx}. Producto ID: {prod_id}**
                        - Score Predicho: {score:.4f}
                        """)
            else:
                st.warning("⚠️ No se encontraron recomendaciones para este usuario")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
    Sistema de Recomendación E-commerce | Desarrollado con Streamlit
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ No se pudieron cargar los datos. Por favor, verifica la ruta del archivo.")


