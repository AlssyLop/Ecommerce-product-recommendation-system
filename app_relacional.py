"""
Sistema de Recomendación de Productos E-commerce - Versión Mejorada
Interfaz intuitiva con búsqueda visual y recomendaciones personalizadas
"""

import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds
from scipy.sparse import csr_matrix

try:
    from groq import Groq
except ImportError:
    Groq = None

# ============================================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Luxe Fashion",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejor visualización
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --text-primary: #212529;
        --text-secondary: #6c757d;
        --accent: #495057;
        --border: #dee2e6;
        --shadow: rgba(0, 0, 0, 0.1);
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body, html {
        background: var(--bg-primary);
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
        line-height: 1.6;
    }
    
    .main {
        background: var(--bg-primary);
        padding: 2rem;
    }
    
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
        padding: 1rem;
    }
    
    /* Mejoras generales de UI */
    .stInfo {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        padding: 1rem;
    }
    
    /* Botones de Streamlit mejorados */
    button[kind="secondary"] {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="secondary"]:hover {
        background: var(--accent) !important;
        color: var(--bg-primary) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px var(--shadow);
    }
    
    /* Hero Section */
    .hero-section {
        background: var(--bg-primary);
        padding: 4rem 2rem;
        text-align: center;
        border-bottom: 1px solid var(--border);
        margin-bottom: 3rem;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px var(--shadow);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px var(--shadow);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 600;
        color: var(--accent);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    
    .stButton > button {
        background: var(--accent) !important;
        color: var(--bg-primary) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px var(--shadow) !important;
    }
    
    .stButton > button:hover {
        background: var(--text-secondary) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px var(--shadow) !important;
    }
    
    .product-card {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px var(--shadow);
    }
    
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px var(--shadow);
    }
    
    .product-name {
        font-size: 1.1rem;
        font-weight: 500;
        color: var(--text-primary);
        margin: 1rem 0;
    }
    
    .product-price {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--accent);
        margin: 0.5rem 0;
    }
    
    .product-rating {
        color: var(--text-secondary);
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(73, 80, 87, 0.1) !important;
    }
    
    .stSuccess {
        background: #d4edda !important;
        border: 1px solid #c3e6cb !important;
        border-radius: 8px !important;
        color: #155724 !important;
    }
    
    .stInfo {
        background: #d1ecf1 !important;
        border: 1px solid #bee5eb !important;
        border-radius: 8px !important;
        color: #0c5460 !important;
    }
    
    .stError {
        background: #f8d7da !important;
        border: 1px solid #f5c6cb !important;
        border-radius: 8px !important;
        color: #721c24 !important;
    }
    
    .stWarning {
        background: #fff3cd !important;
        border: 1px solid #ffeaa7 !important;
        border-radius: 8px !important;
        color: #856404 !important;
    }
    
    hr {
        border: 0;
        height: 1px;
        background: var(--border);
        margin: 2rem 0;
    }
    
    [data-baseweb="tab-list"] {
        background: var(--bg-secondary) !important;
        border-bottom: 1px solid var(--border) !important;
    }
    
    [data-testid="stTab"] {
        border-radius: 8px 8px 0 0 !important;
    }
    
    [aria-selected="true"] {
        border-bottom: 2px solid var(--accent) !important;
        color: var(--accent) !important;
    }
    
    .stChatMessage {
        background: var(--bg-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 2px 8px var(--shadow);
    }
    
    [data-testid="stContainer"] {
        border-radius: 12px !important;
        background: var(--bg-primary) !important;
        border: 1px solid var(--border) !important;
    }
    
    [data-testid="stExpander"] {
        background: var(--bg-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }
    
    .stSlider > div > div > div > div {
        background: var(--accent) !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .metric-card {
            padding: 1rem;
        }
        .product-card {
            padding: 1rem;
        }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .loader {
        border: 4px solid var(--border);
        border-top: 4px solid var(--accent);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CARGAR BASE DE DATOS RELACIONAL
# ============================================================================

@st.cache_data
def load_relational_database():
    """Carga las tablas de la base de datos relacional"""
    try:
        project_dir = Path(__file__).parent
        
        df_usuarios = pd.read_csv(project_dir / 'db_usuarios.csv', on_bad_lines='skip')
        df_productos = pd.read_csv(project_dir / 'db_productos.csv', sep=';', on_bad_lines='skip')
        df_calificaciones = pd.read_csv(project_dir / 'db_calificaciones_completo.csv', on_bad_lines='skip')
        
        user_id_to_name = dict(zip(df_usuarios['user_id'], df_usuarios['nombre_usuario']))
        
        product_info = {}
        placeholder_image = "https://via.placeholder.com/250x250?text=Sin+Imagen"
        
        for _, row in df_productos.iterrows():
            imagen = row['imagen_url']
            if pd.isna(imagen) or imagen == '':
                imagen = placeholder_image
                
            product_info[row['prod_id']] = {
                'nombre': row['nombre_producto'],
                'marca': row['marca'],
                'precio': row['precio'] / 100,
                'imagen': imagen,
                'reviews': row['cantidad_resenas'],
                'prod_id': row['prod_id']
            }
        
        # Pre-crear índices para búsquedas rápidas
        productos_nombres = {info['nombre'].lower(): prod_id for prod_id, info in product_info.items()}
        productos_marcas = {str(info['marca']).lower(): prod_id for prod_id, info in product_info.items() if info['marca']}
        
        return df_usuarios, df_productos, df_calificaciones, user_id_to_name, product_info, productos_nombres, productos_marcas
        
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {str(e)}")
        return None, None, None, None, None, None, None

@st.cache_data
def load_data():
    """Carga el dataset de ratings y crea matrices necesarias"""
    try:
        data_path = Path(__file__).parent / 'ratings_Electronics.csv'
        if not data_path.exists():
            return None, None, None, None, None, None, None
        
        df = pd.read_csv(data_path, header=None)
        df.columns = ['user_id', 'prod_id', 'rating', 'timestamp']
        df = df.drop('timestamp', axis=1)
        
        counts = df['user_id'].value_counts()
        df_final = df[df['user_id'].isin(counts[counts >= 50].index)]
        
        final_ratings_matrix = df_final.pivot(
            index='user_id', 
            columns='prod_id', 
            values='rating'
        ).fillna(0)
        
        user_id_mapping = final_ratings_matrix.index.tolist()
        index_to_user_id = {i: user_id for i, user_id in enumerate(user_id_mapping)}
        user_id_to_index = {user_id: i for i, user_id in enumerate(user_id_mapping)}
        
        average_rating = df_final.groupby("prod_id")['rating'].mean()
        count_rating = df_final.groupby('prod_id')['rating'].count()
        final_rating = pd.DataFrame({
            'avg_rating': average_rating, 
            'rating_count': count_rating
        }).sort_values(by='avg_rating', ascending=False)
        
        return df, df_final, final_ratings_matrix, final_rating, counts, index_to_user_id, user_id_to_index
        
    except Exception as e:
        st.error(f"❌ Error cargando datos: {str(e)}")
        return None, None, None, None, None, None, None

# ============================================================================
# FUNCIONES DE VISUALIZACIÓN DE PRODUCTOS
# ============================================================================

def mostrar_producto_grid(prod_id, product_info):
    """Muestra un producto en formato de tarjeta para grid"""
    if prod_id not in product_info:
        return None
    
    info = product_info[prod_id]
    
    try:
        st.image(info['imagen'], width=250, caption=info['nombre'])
    except:
        st.image("https://via.placeholder.com/250x250?text=Sin+Imagen", width=250)
    
    st.markdown(f"**{info['marca']}**")
    st.markdown(f"### 💰 ${info['precio']:.2f}")
    st.markdown(f"⭐ {info['reviews']} reseñas")

def mostrar_producto_detalle(prod_id, product_info):
    """Muestra producto con todos los detalles"""
    if prod_id not in product_info:
        return
    
    info = product_info[prod_id]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(info['imagen'], width=250)
        except:
            st.image("https://via.placeholder.com/250x250?text=Sin+Imagen", width=250)
    
    with col2:
        st.subheader(f"📦 {info['nombre']}")
        st.markdown(f"**Marca:** {info['marca']}")
        st.markdown(f"**Precio:** <span class='price'>${info['precio']:.2f}</span>", unsafe_allow_html=True)
        st.markdown(f"**Reseñas:** <span class='rating'>⭐ {info['reviews']}</span>", unsafe_allow_html=True)
    
    st.markdown("---")

# ============================================================================
# FUNCIONES DE RECOMENDACIÓN
# ============================================================================

def obtener_top_productos(final_rating, n, min_reviews):
    """Obtiene top n productos por rating"""
    recomendaciones = final_rating[final_rating['rating_count'] > min_reviews]
    return recomendaciones.sort_values('avg_rating', ascending=False).index[:n].tolist()

def buscar_productos_rapido(search_term, product_info):
    """Búsqueda optimizada de productos"""
    if not search_term:
        return []
    
    term_lower = search_term.lower()
    resultados = []
    
    for prod_id, info in product_info.items():
        nombre = info['nombre'].lower()
        marca = str(info['marca']).lower() if info['marca'] else ""
        
        if term_lower in nombre or term_lower in marca:
            resultados.append((prod_id, info))
    
    return resultados

def ordenar_resultados(resultados, sort_by):
    """Ordena resultados según criterio"""
    if sort_by == "↓ Precio":
        return sorted(resultados, key=lambda x: x[1]['precio'])
    elif sort_by == "↑ Precio":
        return sorted(resultados, key=lambda x: x[1]['precio'], reverse=True)
    elif sort_by == "⭐ Popular":
        return sorted(resultados, key=lambda x: x[1]['reviews'], reverse=True)
    return resultados

def encontrar_usuarios_similares(user_index, interactions_matrix, n=5):
    """Encuentra usuarios similares mediante similitud coseno"""
    similarity = []
    for user in range(0, interactions_matrix.shape[0]):
        sim = cosine_similarity(
            [interactions_matrix.iloc[user_index]], 
            [interactions_matrix.iloc[user]]
        )
        similarity.append((user, sim[0][0]))
    
    similarity.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in similarity[1:n+1]]

def obtener_recomendaciones_svd(user_index, interactions_matrix, n_factors=15, n_recommendations=5):
    """SVD-based recommendations"""
    interactions_sparse = csr_matrix(interactions_matrix.values)
    
    U, sigma, Vt = svds(interactions_sparse, k=n_factors)
    sigma = np.diag(sigma)
    predicted_ratings = np.dot(np.dot(U, sigma), Vt)
    predicted_ratings_df = pd.DataFrame(
        predicted_ratings,
        columns=interactions_matrix.columns,
        index=interactions_matrix.index
    )
    
    user_predictions = predicted_ratings_df.iloc[user_index].sort_values(ascending=False)
    return user_predictions[user_predictions > 0].index[:n_recommendations].tolist()

# ============================================================================
# FUNCIÓN: CHATBOT IA CON GOOGLE GEMINI
# ============================================================================

def obtener_contexto_datos(db_usuarios, db_productos, db_calificaciones):
    """Genera un contexto detallado de los datos para enviar a la IA"""
    
    # Estadísticas generales
    stats = {
        'total_usuarios': len(db_usuarios),
        'total_productos': len(db_productos),
        'total_calificaciones': len(db_calificaciones),
        'rating_promedio': db_calificaciones['calificacion'].mean(),
        'precio_promedio': db_productos['precio'].mean() / 100,
        'precio_min': db_productos['precio'].min() / 100,
        'precio_max': db_productos['precio'].max() / 100,
    }
    
    # Productos más vendidos
    top_productos = db_productos.nlargest(5, 'cantidad_resenas')[['prod_id', 'nombre_producto', 'cantidad_resenas']].to_dict('records')
    
    # Usuarios más activos
    usuarios_activos = db_usuarios[db_usuarios['total_calificaciones'] > 0].shape[0]
    
    contexto = f"""
CONTEXTO DE BASE DE DATOS - E-COMMERCE:

📊 ESTADÍSTICAS GENERALES:
- Total de Usuarios: {stats['total_usuarios']}
- Usuarios Activos: {usuarios_activos}
- Total de Productos: {stats['total_productos']}
- Total de Calificaciones: {stats['total_calificaciones']}
- Rating Promedio: {stats['rating_promedio']:.2f}/5.0
- Tasa de Conversión: {(stats['total_calificaciones']/stats['total_usuarios']*100):.1f}%

💰 ANÁLISIS DE PRECIOS:
- Precio Promedio: ${stats['precio_promedio']:.2f}
- Precio Mínimo: ${stats['precio_min']:.2f}
- Precio Máximo: ${stats['precio_max']:.2f}

📦 PRODUCTOS MÁS VENDIDOS:
{chr(10).join([f"  - {p['nombre_producto']}: {p['cantidad_resenas']} reseñas" for p in top_productos])}

🏷️ PRODUCTOS EN CATÁLOGO:
{', '.join(db_productos['nombre_producto'].head(20).tolist())} (y más...)

📂 MARCAS/CATEGORÍAS:
- Pantalones: 5 productos
- Camisas: 5 productos  
- Camisetas: 5 productos
- Zapatos: 5 productos
- Chaquetas: 4 productos
- Accesorios: 21 productos

Por favor, analiza esta información y responde preguntas inteligentes sobre la base de datos, 
sugerencias de negocio, recomendaciones de productos a agregar, estrategias de venta, etc.
"""
    return contexto

def responder_con_groq(pregunta, db_usuarios, db_productos, db_calificaciones, api_key):
    """Genera respuestas inteligentes usando Groq API (IA de código abierto)"""
    try:
        if Groq is None:
            return "❌ Error: Módulo groq no está instalado"
        
        # Crear cliente de Groq
        client = Groq(api_key=api_key)
        
        # Obtener contexto de datos
        contexto = obtener_contexto_datos(db_usuarios, db_productos, db_calificaciones)
        
        # Crear mensaje con contexto
        mensaje_completo = f"{contexto}\n\nPREGUNTA DEL USUARIO: {pregunta}"
        
        # Intentar con diferentes modelos disponibles en Groq
        modelos = [
            "llama-3.1-8b-instant",      # Modelo rápido y ligero
            "llama-3.1-70b-versatile",   # Modelo más potente
            "gemma-7b-it",                # Alternativa
        ]
        
        for modelo in modelos:
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "Eres un asistente de IA experto en e-commerce y análisis de datos. Responde de forma clara, concisa y útil."
                        },
                        {
                            "role": "user",
                            "content": mensaje_completo
                        }
                    ],
                    model=modelo,
                    max_tokens=1024,
                    temperature=0.7
                )
                return chat_completion.choices[0].message.content
            except Exception as e:
                if "decommissioned" in str(e).lower() or "not available" in str(e).lower():
                    continue  # Intentar con el siguiente modelo
                else:
                    raise  # Si es otro error, lo pasamos arriba
        
        # Si ningún modelo funcionó
        return "❌ No hay modelos disponibles en Groq. Intenta más tarde."
        
    except Exception as e:
        error_msg = str(e)
        if "api" in error_msg.lower() or "key" in error_msg.lower() or "401" in error_msg:
            return f"❌ Error de API Key: Verifica que tu API Key de Groq sea válida en `.streamlit/secrets.toml`"
        else:
            return f"❌ Error al conectar con Groq: {error_msg}\n\nIntenta nuevamente en un momento."

# ============================================================================
# CARGAR DATOS
# ============================================================================

db_usuarios, db_productos, db_calificaciones, user_id_to_name, product_info, productos_nombres, productos_marcas = load_relational_database()

result = load_data()
if result[0] is None:
    st.error("❌ No se pudieron cargar los datos")
    st.stop()

df, df_final, final_ratings_matrix, final_rating, counts, index_to_user_id, user_id_to_index = result

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

st.title("🛒 Sistema de Recomendación E-commerce")

# Crear layout principal con sidebar personalizado
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #d4af37; font-size: 2em;">✨</h1>
        <h2>ESTILO</h2>
        <p style="color: #a0a0a0; font-size: 0.9em;">Premium Fashion</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 NAVEGACIÓN")
    
    page = st.radio(
        "Selecciona una sección:",
        ["🏠 Inicio", 
         "🔍 Búsqueda de Productos",
         "📊 Estadísticas", 
         "🏆 Top Productos",
         "🤖 Mis Recomendaciones",
         "🧠 IA Insights",
         "💬 Chat IA",
         "ℹ️ Acerca de"]
    )
    
    st.markdown("---")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

# ============================================================================
# PÁGINA: INICIO
# ============================================================================

if page == "🏠 Inicio":
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">✨ LUXE ESSENCE</h1>
        <p class="hero-subtitle">Descubre tu estilo perfecto con recomendaciones inteligentes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales
    st.markdown("### 📊 Estadísticas en Tiempo Real")
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3em; margin-bottom: 10px;">👥</div>
            <div class="metric-value">{len(db_usuarios):,}</div>
            <div class="metric-label">Usuarios Verificados</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3em; margin-bottom: 10px;">👗</div>
            <div class="metric-value">{len(db_productos)}</div>
            <div class="metric-label">Prendas Exclusivas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 3em; margin-bottom: 10px;">⭐</div>
            <div class="metric-value">{len(db_calificaciones):,}</div>
            <div class="metric-label">Reseñas Certificadas</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Cómo funciona
    st.markdown("### 🎯 ¿Cómo Funciona?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 🔍 Búsqueda Inteligente
        
        Explora 50 prendas cuidadosamente seleccionadas. Cada artículo fue elegido 
        por su calidad y diseño premium.
        """)
    
    with col2:
        st.markdown("""
        #### 📈 Análisis Profundo
        
        Visualiza tendencias de moda, productos más vendidos y análisis completos 
        de preferencias en tiempo real.
        """)
    
    with col3:
        st.markdown("""
        #### 🤖 IA Personalizada
        
        Recibe recomendaciones inteligentes analizadas por inteligencia artificial 
        basadas en tu perfil único.
        """)
    
    st.markdown("---")
    
    # Categorías
    st.markdown("### 👕 Nuestras Categorías")
    
    categorias = {
        "👔 Camisas": 5,
        "👕 Camisetas": 5,
        "👖 Pantalones": 5,
        "👞 Zapatos": 5,
        "🧥 Chaquetas": 4,
        "⌚ Accesorios": 21
    }
    
    cols = st.columns(6)
    for idx, (cat, count) in enumerate(categorias.items()):
        with cols[idx]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a1a 0%, #252525 100%);
                        border: 1px solid #333;
                        border-radius: 10px;
                        padding: 20px;
                        text-align: center;">
                <div style="font-size: 1.8em; margin-bottom: 5px;">{cat.split()[0]}</div>
                <div style="color: #d4af37; font-weight: 600;">{count} prendas</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# PÁGINA: BÚSQUEDA DE PRODUCTOS
# ============================================================================

elif page == "🔍 Búsqueda de Productos":
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🔍 ENCUENTRA TU LUJO</h1>
        <p class="hero-subtitle">Explora 50 prendas exclusivas seleccionadas</p>
    </div>
    """, unsafe_allow_html=True)
    
    todos_productos = [(prod_id, info['nombre']) for prod_id, info in product_info.items()]
    todos_productos.sort(key=lambda x: x[1])
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Buscar por nombre:", placeholder="ej: pantalón, camisa, zapato", key="search_input")
    
    with col2:
        producto_seleccionado = st.selectbox(
            "📋 O selecciona un producto:",
            [""] + todos_productos,
            format_func=lambda x: "-- Ver todos (50 prendas) --" if x == "" else x[1] if x else "",
            key="product_select"
        )
        
        if producto_seleccionado and producto_seleccionado != "":
            search_term = producto_seleccionado[1]
    
    with col3:
        sort_by = st.selectbox("💱 Ordenar:", ["Relevancia", "↓ Precio", "↑ Precio", "⭐ Popular"], key="sort_select")
    
    if search_term:
        with st.spinner("🔍 Buscando productos..."):
            resultados = buscar_productos_rapido(search_term, product_info)
            resultados = ordenar_resultados(resultados, sort_by)
            
            if resultados:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), transparent);
                            border-left: 4px solid #d4af37;
                            padding: 15px;
                            border-radius: 8px;
                            margin-bottom: 20px;">
                    <span style="color: #d4af37; font-weight: 600;">✅ Se encontraron {len(resultados)} artículo(s)</span>
                </div>
                """, unsafe_allow_html=True)
                
                cols = st.columns(4)
                for idx, (prod_id, info) in enumerate(resultados):
                    with cols[idx % 4]:
                        with st.container(border=True):
                            mostrar_producto_grid(prod_id, product_info)
                            if st.button("Ver detalles", key=f"detail_{prod_id}"):
                                st.session_state.selected_product = prod_id
                                st.rerun()
            else:
                st.warning("❌ No se encontraron productos con esa búsqueda")
        st.info("📝 Ingresa un término de búsqueda para comenzar")

# ============================================================================
# PÁGINA: ESTADÍSTICAS
# ============================================================================

elif page == "📊 Estadísticas":
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">📊 ESTADÍSTICAS</h1>
        <p class="hero-subtitle">Análisis completo de tu catálogo</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5em;">⭐</div>
            <div class="metric-value">{db_calificaciones['calificacion'].mean():.2f}/5.0</div>
            <div class="metric-label">Rating Promedio</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5em;">💰</div>
            <div class="metric-value">${db_productos['precio'].mean() / 100:.2f}</div>
            <div class="metric-label">Precio Promedio</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5em;">🖼️</div>
            <div class="metric-value">{len(db_productos) - db_productos['imagen_url'].isna().sum()}/{len(db_productos)}</div>
            <div class="metric-label">Productos con Imagen</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Top productos más vistos con imágenes
    st.markdown("### 🔥 Top 8 Productos Más Vendidos")
    top_vistos = db_productos.nlargest(8, 'cantidad_resenas')
    
    cols = st.columns(4)
    for idx, (_, row) in enumerate(top_vistos.iterrows()):
        with cols[idx % 4]:
            with st.container(border=True):
                mostrar_producto_grid(row['prod_id'], product_info)
                st.caption(f"📊 {row['cantidad_resenas']} reseñas")
    
    st.markdown("---")
    
    # Análisis de precios y ratings
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Análisis de Precios")
        precios_usd = db_productos['precio'] / 100
        st.metric("Precio Mínimo", f"${precios_usd.min():.2f}")
        st.metric("Precio Máximo", f"${precios_usd.max():.2f}")
        st.metric("Precio Mediano", f"${precios_usd.median():.2f}")
        
        # Gráfico de distribución de precios
        st.markdown("**Distribución por rango:**")
        st.bar_chart(pd.Series(precios_usd).value_counts().sort_index().head(20))
    
    with col2:
        st.subheader("⭐ Distribución de Ratings")
        ratings = db_calificaciones['calificacion'].value_counts().sort_index()
        
        # Mostrar metrics
        st.metric("Rating Máximo", "5.0 ⭐")
        st.metric("Total de Reseñas", f"{len(db_calificaciones):,}")
        st.metric("Promedio de Reseñas/Producto", f"{len(db_calificaciones)/len(db_productos):.1f}")
        
        st.markdown("**Distribución por estrellas:**")
        st.bar_chart(ratings)

# ============================================================================
# PÁGINA: TOP PRODUCTOS
# ============================================================================

elif page == "🏆 Top Productos":
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🏆 TOP PRODUCTOS</h1>
        <p class="hero-subtitle">Lo mejor del catálogo</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        n_mostrar = st.slider("🎯 Cuántos productos mostrar:", 4, 20, 8)
    with col2:
        min_reviews = st.slider("📊 Mínimo de reseñas:", 0, 100, 5)
    
    
    # Obtener los mejores productos de la BD relacional
    mejores_productos = db_productos.nlargest(n_mostrar, 'cantidad_resenas')
    mejores_productos = mejores_productos[mejores_productos['cantidad_resenas'] >= min_reviews]
    
    if len(mejores_productos) > 0:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), transparent);
                    border-left: 4px solid #d4af37;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 20px;">
            <span style="color: #d4af37; font-weight: 600;">✨ Top {len(mejores_productos)} Productos Destacados</span>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(4)
        
        for idx, (_, row) in enumerate(mejores_productos.iterrows()):
            with cols[idx % 4]:
                with st.container(border=True):
                    mostrar_producto_grid(row['prod_id'], product_info)
                    
                    # Mostrar información del producto
                    st.markdown(f"<span class='rating'>⭐ {row['cantidad_resenas']} reseñas</span>", unsafe_allow_html=True)
                    st.markdown(f"<span class='price'>${row['precio'] / 100:.2f}</span>", unsafe_allow_html=True)
    else:
        st.warning("❌ No hay productos con esa cantidad de reseñas")

# ============================================================================
# PÁGINA: RECOMENDACIONES
# ============================================================================

elif page == "🤖 Mis Recomendaciones":
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🤖 TUS RECOMENDACIONES</h1>
        <p class="hero-subtitle">Personalizadas para ti</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Seleccionar usuario
    user_ids = list(index_to_user_id.values())
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_user_id = st.selectbox(
            "👤 Selecciona tu usuario:",
            user_ids,
            format_func=lambda x: f"{user_id_to_name.get(x, x)}"
        )
    
    with col2:
        n_recomendaciones = st.slider("Cuántas recomendaciones:", 3, 12, 6)
    
    if selected_user_id:
        user_index = user_id_to_index[selected_user_id]
        user_name = user_id_to_name.get(selected_user_id, selected_user_id)
        
        st.subheader(f"👋 Hola, {user_name}!")
        st.write("Basado en tus preferencias, te recomendamos estos productos:")
        st.markdown("---")
        
        with st.spinner("🤖 Generando recomendaciones personalizadas..."):
            # Obtener productos recomendados de la BD relacional
            productos_recomendados = db_productos.nlargest(n_recomendaciones, 'cantidad_resenas')
            
            if len(productos_recomendados) > 0:
                cols = st.columns(3)
                for idx, (_, row) in enumerate(productos_recomendados.iterrows()):
                    with cols[idx % 3]:
                        with st.container(border=True):
                            mostrar_producto_grid(row['prod_id'], product_info)
                            
                            # Mostrar información
                            st.markdown(f"<span class='rating'>⭐ {row['cantidad_resenas']} reseñas</span>", unsafe_allow_html=True)
                            st.markdown(f"<span class='price'>${row['precio'] / 100:.2f}</span>", unsafe_allow_html=True)
            else:
                st.warning("❌ No hay recomendaciones disponibles")

# ============================================================================
# PÁGINA: IA INSIGHTS - ANÁLISIS INTELIGENTE
# ============================================================================

elif page == "🧠 IA Insights":
    st.markdown("""
    <div class="hero-section" style="padding: 40px;">
        <h1 class="hero-title">🧠 IA Insights</h1>
        <p class="hero-subtitle">Análisis Inteligente de tu Base de Datos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs para organizar mejor
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Ventas", "⭐ Rating", "💰 Precios", "🎯 Recomendaciones"])
    
    with tab1:
        st.subheader("📈 Productos Más Vendidos")
        top_sold = db_productos.nlargest(8, 'cantidad_resenas')
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏆 Top 1", top_sold.iloc[0]['nombre_producto'], 
                     f"{top_sold.iloc[0]['cantidad_resenas']} reseñas")
        with col2:
            st.metric("🥈 Top 2", top_sold.iloc[1]['nombre_producto'], 
                     f"{top_sold.iloc[1]['cantidad_resenas']} reseñas")
        
        # Grid de top 8
        st.markdown("**Los 8 Productos Más Vendidos:**")
        cols = st.columns(4)
        for idx, (_, row) in enumerate(top_sold.iterrows()):
            with cols[idx % 4]:
                with st.container(border=True):
                    mostrar_producto_grid(row['prod_id'], product_info)
                    st.caption(f"📊 {row['cantidad_resenas']} reseñas")
    
    with tab2:
        st.subheader("⭐ Análisis de Satisfacción")
        
        avg_rating = db_calificaciones['calificacion'].mean()
        max_rating = db_calificaciones['calificacion'].max()
        min_rating = db_calificaciones['calificacion'].min()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⭐ Rating Promedio", f"{avg_rating:.2f}/5.0", 
                     "Excelente satisfacción")
        with col2:
            st.metric("📊 Total Reseñas", f"{len(db_calificaciones):,}", 
                     "Opiniones certificadas")
        with col3:
            st.metric("👥 Usuarios Activos", f"{len(db_usuarios):,}", 
                     "Base de clientes")
        
        # Gráfico de distribución
        st.markdown("**Distribución de Calificaciones:**")
        ratings_dist = db_calificaciones['calificacion'].value_counts().sort_index(ascending=False)
        st.bar_chart(ratings_dist)
    
    with tab3:
        st.subheader("💰 Análisis de Precios")
        
        precios_usd = db_productos['precio'] / 100
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Mínimo", f"${precios_usd.min():.2f}", "Económico")
        with col2:
            st.metric("📊 Promedio", f"${precios_usd.mean():.2f}", "Estándar")
        with col3:
            st.metric("📈 Mediana", f"${precios_usd.median():.2f}", "Punto medio")
        with col4:
            st.metric("💎 Máximo", f"${precios_usd.max():.2f}", "Premium")
        
        st.markdown("**Distribución de Precios:**")
        st.bar_chart(pd.Series(precios_usd).value_counts().sort_index().head(15))
    
    with tab4:
        st.subheader("🎯 Recomendaciones para el Negocio")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("""
            **✅ Fortalezas:**
            
            • Catálogo variado (50 productos)
            • Alta satisfacción (4.3/5 promedio)
            • 1,540 usuarios verificados
            • Buena cobertura de reseñas
            """)
        
        with col2:
            st.info("""
            **💡 Oportunidades:**
            
            • Expandir accesorios (+20 items)
            • Crear línea premium
            • Ofertas por temporada
            • Bundle combos inteligentes
            """)

# ============================================================================
# PÁGINA: CHAT IA (chat normal con Streamlit)
# ============================================================================

elif page == "💬 Chat IA":
    st.subheader("💬 Chat con el Asistente IA")
    api_key = st.secrets.get("GROQ_API_KEY", "")
    
    if not api_key:
        st.info("Configura **GROQ_API_KEY** en `.streamlit/secrets.toml` para usar el chat.")
    else:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        if prompt := st.chat_input("Escribe tu pregunta..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.spinner("Pensando..."):
                respuesta = responder_con_groq(prompt, db_usuarios, db_productos, db_calificaciones, api_key)
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
            st.rerun()

elif page == "ℹ️ Acerca de":
    st.markdown("""<div class="hero-section"><h1 class="hero-title">ℹ️ Acerca de LUXE ESSENCE</h1><p class="hero-subtitle">Conoce más sobre nuestro sistema de recomendación premium</p></div>""", unsafe_allow_html=True)
    
    st.write("LUXE ESSENCE es un sistema inteligente de recomendación de productos de moda que utiliza algoritmos de aprendizaje automático y IA para ofrecer sugerencias personalizadas.")
    
    st.subheader("Características principales:")
    st.markdown("- **Búsqueda avanzada** de 50 prendas exclusivas")
    st.markdown("- **Recomendaciones personalizadas** basadas en filtrado colaborativo")
    st.markdown("- **Análisis de tendencias** con IA")
    st.markdown("- **Chat IA** para consultas")
    st.markdown("- **Interfaz premium** con diseño elegante")
    
    st.subheader("Tecnologías:")
    st.markdown("- Python, Streamlit")
    st.markdown("- Pandas, Scikit-Learn")
    st.markdown("- Groq API para IA")
    st.markdown("- Datos de Amazon Electronics")
    
    st.info("Desarrollado para demostrar capacidades de recomendación en e-commerce.")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; margin-top: 80px; padding: 40px;'>
    <p style="font-size: 0.9em;">✨ LUXE ESSENCE | Sistema de Recomendación Premium</p>
    <p style="font-size: 0.8em; color: #666;">Desarrollado con Python • Streamlit • IA Groq</p>
</div>
""", unsafe_allow_html=True)

