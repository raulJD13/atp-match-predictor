import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import time
import os

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="ATP Match Predictor Pro",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. DISEÑO AVANZADO (CSS - TEMA CLARO)
# ==========================================
st.markdown("""
<style>
    /* FORZAR TEMA CLARO Y FONDO DEGRADADO */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* ESTILO DEL HEADER */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        color: #1a2a6c; /* Navy Blue */
        text-align: center;
        margin-bottom: 0px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4b6cb7;
        text-align: center;
        margin-bottom: 30px;
        font-style: italic;
    }

    /* TARJETAS DE JUGADORES (GLASSMORPHISM) */
    .player-card {
        background: rgba(255, 255, 255, 0.90);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.3s ease;
        text-align: center;
    }
    .player-card:hover {
        transform: translateY(-5px);
    }
    
    /* TARJETA DE RESULTADO */
    .result-card {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        color: white;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        margin-top: 20px;
    }
    
    /* PERSONALIZAR MÉTRICAS */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #1a2a6c;
    }
    div[data-testid="stMetricLabel"] {
        color: #666;
    }

    /* BOTÓN PERSONALIZADO */
    div.stButton > button {
        background: linear-gradient(90deg, #1CB5E0 0%, #000851 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. DATA ENGINEERING (LOGICA CORREGIDA)
# ==========================================
@st.cache_data
def load_players_from_csv():
    """
    Carga jugadores combinando Player_1 y Player_2 para obtener el ranking más reciente.
    """
    # 1. Ruta Absoluta
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "data", "atp_tennis_2015_adelante.csv")
    
    print(f"🔍 Cargando datos desde: {csv_path}")

    if not os.path.exists(csv_path):
        st.error(f"❌ ERROR: Archivo no encontrado en {csv_path}")
        return None

    try:
        df = pd.read_csv(csv_path)
        
        # 2. Convertir Fechas
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
        else:
            df['Date'] = pd.to_datetime('2024-01-01')

        # 3. EXTRAER DATOS (CORRECCIÓN CLAVE)
        # Extraemos info del Player 1
        p1_data = df[['Player_1', 'Rank_1', 'Pts_1', 'Date']].rename(
            columns={'Player_1': 'Name', 'Rank_1': 'Rank', 'Pts_1': 'Points'}
        )
        
        # Extraemos info del Player 2
        p2_data = df[['Player_2', 'Rank_2', 'Pts_2', 'Date']].rename(
            columns={'Player_2': 'Name', 'Rank_2': 'Rank', 'Pts_2': 'Points'}
        )
        
        # 4. Unir ambos datasets (verticalmente)
        all_players = pd.concat([p1_data, p2_data])
        
        # 5. Limpieza de datos numéricos
        all_players['Rank'] = pd.to_numeric(all_players['Rank'], errors='coerce')
        all_players['Points'] = pd.to_numeric(all_players['Points'], errors='coerce')
        
        # Eliminamos filas donde no haya ranking válido
        all_players = all_players.dropna(subset=['Rank', 'Points'])
        
        # 6. Obtener la "Última Foto": Ordenar por fecha descendente y quitar duplicados por nombre
        latest_rankings = all_players.sort_values('Date', ascending=False).drop_duplicates('Name')
        
        # 7. Filtrar Top 200 y ordenar por ranking
        top_players = latest_rankings[latest_rankings['Rank'] <= 200].sort_values('Rank')
        
        # 8. Convertir a diccionario
        players_dict = {}
        for _, row in top_players.iterrows():
            players_dict[row['Name']] = {
                "rank": int(row['Rank']),
                "points": int(row['Points']),
                "country": "🎾" 
            }
            
        print(f"✅ ÉXITO: {len(players_dict)} jugadores cargados correctamente.")
        return players_dict

    except Exception as e:
        st.error(f"❌ Error procesando el CSV: {e}")
        print(e)
        return None

# Carga de datos
players_db = load_players_from_csv()

# Datos de respaldo por si falla
if not players_db:
    st.toast("⚠️ Error de CSV. Usando datos demo.", icon="🚨")
    players_db = {
        "Novak Djokovic (Demo)": {"rank": 1, "points": 11000, "country": "🇷🇸"},
        "Carlos Alcaraz (Demo)": {"rank": 2, "points": 8800, "country": "🇪🇸"},
        "Jannik Sinner (Demo)": {"rank": 3, "points": 7000, "country": "🇮🇹"}
    }

# ==========================================
# 4. INTERFAZ DE USUARIO (Layout)
# ==========================================

# Header
st.markdown('<div class="main-header">ATP ORACLE AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Advanced Match Prediction System</div>', unsafe_allow_html=True)

# Contenedor Principal
with st.container():
    col1, col2, col3 = st.columns([1, 0.2, 1])
    
    # --- JUGADOR 1 ---
    with col1:
        st.markdown('<div class="player-card">', unsafe_allow_html=True)
        st.markdown("### 👤 PLAYER 1")
        
        p1_name = st.selectbox("Select Player 1", list(players_db.keys()), index=0, key="p1_select")
        p1_data = players_db[p1_name]
        
        m1, m2 = st.columns(2)
        with m1: st.metric("ATP Rank", f"#{p1_data['rank']}")
        with m2: st.metric("Points", f"{p1_data['points']:,}")
        
        st.caption(f"Stats loaded from historical data")
        st.markdown('</div>', unsafe_allow_html=True)

    # VS separador visual
    with col2:
        st.markdown("<br><br><br><h1 style='text-align: center; color: #ccc;'>VS</h1>", unsafe_allow_html=True)

    # --- JUGADOR 2 ---
    with col3:
        st.markdown('<div class="player-card">', unsafe_allow_html=True)
        st.markdown("### 👤 PLAYER 2")
        
        opponents = [p for p in players_db.keys() if p != p1_name]
        p2_name = st.selectbox("Select Player 2", opponents, index=0, key="p2_select")
        p2_data = players_db[p2_name]
        
        m3, m4 = st.columns(2)
        with m3: st.metric("ATP Rank", f"#{p2_data['rank']}")
        with m4: st.metric("Points", f"{p2_data['points']:,}")
        
        st.caption(f"Stats loaded from historical data")
        st.markdown('</div>', unsafe_allow_html=True)

# --- CONDICIONES DEL PARTIDO ---
st.write("") 
st.write("") 

c_cond1, c_cond2, c_cond3 = st.columns([1, 2, 1])
with c_cond2:
    st.markdown("### 🏟️ Match Conditions")
    surface = st.select_slider(
        "Select Surface",
        options=["Hard", "Clay", "Grass"],
        value="Hard"
    )

# --- BOTÓN DE ACCIÓN ---
st.write("")
b1, b2, b3 = st.columns([1, 2, 1])
with b2:
    predict_btn = st.button("🔮 GENERATE PREDICTION")

# ==========================================
# 5. LÓGICA DE PREDICCIÓN Y RESULTADOS
# ==========================================
if predict_btn:
    progress_text = "🧠 AI is processing historical matchups..."
    my_bar = st.progress(0, text=progress_text)
    
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(0.5)
    my_bar.empty()

    # Preparamos Payload
    payload = {
        "diff_rank": int(p1_data["rank"] - p2_data["rank"]),
        "diff_pts": int(p1_data["points"] - p2_data["points"]),
        "surface": surface
    }
    
    try:
        # LLAMADA A LA API (BACKEND)
        api_url = "http://127.0.0.1:8000/predict"
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        result = response.json()

        winner = result["winner"]
        prob = result["probability_player_1"]
        
        # Determinar nombres y colores
        if winner == "Player 1":
            winner_name = p1_name
            loser_name = p2_name
            win_prob = prob
        else:
            winner_name = p2_name
            loser_name = p1_name
            win_prob = 1 - prob
            
        # MOSTRAR RESULTADOS
        st.markdown(f"""
        <div class="result-card">
            <h3>🏆 AI PREDICTION</h3>
            <h1 style="font-size: 3.5rem; margin: 0;">{winner_name}</h1>
            <p style="font-size: 1.2rem; opacity: 0.8;">wins against {loser_name}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # GRÁFICO DE BARRAS INTERACTIVO (Plotly)
        st.write("")
        st.markdown("### 📊 Probability Confidence")
        
        fig = go.Figure()
        
        # Barra Jugador 1
        fig.add_trace(go.Bar(
            y=['Win Probability'],
            x=[prob],
            name=p1_name,
            orientation='h',
            marker=dict(color='#1CB5E0', line=dict(color='white', width=2)),
            text=f"{p1_name}: {prob:.1%}",
            textposition='auto',
            hoverinfo='text'
        ))
        
        # Barra Jugador 2
        fig.add_trace(go.Bar(
            y=['Win Probability'],
            x=[1-prob],
            name=p2_name,
            orientation='h',
            marker=dict(color='#000851', line=dict(color='white', width=2)),
            text=f"{p2_name}: {(1-prob):.1%}",
            textposition='auto',
            hoverinfo='text'
        ))

        fig.update_layout(
            barmode='stack',
            xaxis=dict(range=[0, 1], showticklabels=False, showgrid=False),
            yaxis=dict(showticklabels=False, showgrid=False),
            height=120,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Datos Técnicos (Expandible)
        with st.expander("🛠️ View Model Inputs & JSON Response"):
            st.json(payload)
            st.json(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Error de Conexión: Asegúrate de que el Backend (FastAPI) está corriendo en el puerto 8000.")
    except Exception as e:
        st.error(f"❌ Ocurrió un error inesperado: {e}")

# Footer minimalista
st.markdown("---")
st.markdown("<p style='text-align: center; color: #aaa; font-size: 0.8rem;'>ATP Match Predictor Project • Powered by Python, Scikit-Learn & FastAPI</p>", unsafe_allow_html=True)