import streamlit as st
import random
import qrcode
from io import BytesIO

# --- 1. DATOS: LISTA DE ODS ---
ODS_LIST = [
    {"id": 1, "nombre": "ODS 1: Fin de la pobreza", "palabra": "Donación"},
    {"id": 2, "nombre": "ODS 2: Hambre cero", "palabra": "Agricultura"},
    {"id": 3, "nombre": "ODS 3: Salud y bienestar", "palabra": "Vacunas"},
    {"id": 4, "nombre": "ODS 4: Educación de calidad", "palabra": "Escuelas"},
    {"id": 5, "nombre": "ODS 5: Igualdad de género", "palabra": "Equidad"},
    {"id": 6, "nombre": "ODS 6: Agua limpia y saneamiento", "palabra": "Grifo"},
    {"id": 7, "nombre": "ODS 7: Energía asequible", "palabra": "Solar"},
    {"id": 8, "nombre": "ODS 8: Trabajo decente", "palabra": "Empleo"},
    {"id": 9, "nombre": "ODS 9: Industria e innovación", "palabra": "Internet"},
    {"id": 10, "nombre": "ODS 10: Reducción de desigualdades", "palabra": "Inclusión"},
    {"id": 11, "nombre": "ODS 11: Ciudades sostenibles", "palabra": "Bicicleta"},
    {"id": 12, "nombre": "ODS 12: Producción responsable", "palabra": "Reciclaje"},
    {"id": 13, "nombre": "ODS 13: Acción por el clima", "palabra": "Calentamiento"},
    {"id": 14, "nombre": "ODS 14: Vida submarina", "palabra": "Peces"},
    {"id": 15, "nombre": "ODS 15: Vida de ecosistemas terrestres", "palabra": "Árboles"},
    {"id": 16, "nombre": "ODS 16: Paz y justicia", "palabra": "Leyes"},
    {"id": 17, "nombre": "ODS 17: Alianzas", "palabra": "Equipo"}
]

# Iconos y colores para avatares
AVATAR_COLORS = ["#B5E7E0", "#FFB3D9", "#FFF4B3", "#D4C5F9", "#FFCBA4"]
AVATAR_ICONS = ["🌱", "🔍", "⭐", "🌸", "🚀", "💡", "🎯", "✨"]

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="LA IMPODSTORA", page_icon="🕵️‍♀️", layout="centered")

# Estilos CSS modernos
st.markdown("""
    <style>
        /* Fondo gradiente */
        .stApp {
            background: linear-gradient(135deg, #FFE5F1 0%, #E5F5F5 50%, #F0E5FF 100%);
        }
        
        /* Header */
        .main-header {
            background: linear-gradient(90deg, #FF69B4, #FF1493);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: 900;
            text-align: center;
            margin: 20px 0;
            letter-spacing: 2px;
        }
        
        .subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 30px;
        }
        
        /* Botones principales */
        .stButton>button {
            background: linear-gradient(135deg, #FF1493, #FF69B4);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 15px 30px;
            font-size: 1.1rem;
            font-weight: bold;
            width: 100%;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(255, 20, 147, 0.3);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 20, 147, 0.4);
        }
        
        /* Input personalizado */
        .stTextInput>div>div>input {
            border-radius: 20px;
            border: 2px solid #FFB3D9;
            padding: 15px;
            font-size: 1rem;
        }
        
        /* Cards de jugadores */
        .player-card {
            background: white;
            border-radius: 20px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin: 10px 0;
            position: relative;
        }
        
        .player-avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            margin: 0 auto 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
        }
        
        .player-name {
            font-weight: bold;
            font-size: 1.1rem;
            color: #333;
        }
        
        .remove-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #FFB3D9;
            border-radius: 50%;
            width: 25px;
            height: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 1rem;
        }
        
        /* Counter badge */
        .counter-badge {
            background: #FF69B4;
            color: white;
            border-radius: 20px;
            padding: 5px 15px;
            display: inline-block;
            font-weight: bold;
            margin: 10px 0;
        }
        
        /* Tarjetas de rol */
        .role-card-impostor {
            background: linear-gradient(135deg, #FFE5E5, #FFCCCC);
            border: 4px solid #FF4B4B;
            border-radius: 25px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 8px 20px rgba(255, 75, 75, 0.3);
        }
        
        .role-card-crew {
            background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
            border: 4px solid #4CAF50;
            border-radius: 25px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
        }
        
        .role-title {
            font-size: 2rem;
            font-weight: 900;
            margin: 10px 0;
        }
        
        .keyword-highlight {
            background: white;
            border: 3px dashed #4CAF50;
            border-radius: 15px;
            padding: 15px 25px;
            font-size: 1.5rem;
            font-weight: bold;
            display: inline-block;
            margin: 15px 0;
            color: #2E7D32;
        }
        
        /* Debate card */
        .debate-card {
            background: linear-gradient(135deg, #FFF9C4, #FFF59D);
            border: 4px solid #FBC02D;
            border-radius: 25px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 8px 20px rgba(251, 192, 45, 0.3);
        }
        
        /* Reveal card */
        .reveal-card {
            background: linear-gradient(135deg, #E1BEE7, #CE93D8);
            border: 4px dashed #9C27B0;
            border-radius: 25px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 8px 20px rgba(156, 39, 176, 0.3);
        }
        
        .impostor-name {
            font-size: 3rem;
            font-weight: 900;
            color: #C62828;
            margin: 20px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Progress bar custom */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #FF69B4, #FF1493);
        }
        
        /* Ajustes generales */
        .block-container {
            padding-top: 2rem;
            max-width: 800px;
        }
        
        /* Info boxes */
        .stAlert {
            border-radius: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. GESTIÓN DE ESTADO ---
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'stage' not in st.session_state:
    st.session_state.stage = 'setup'
if 'players' not in st.session_state:
    st.session_state.players = []
if 'player_avatars' not in st.session_state:
    st.session_state.player_avatars = {}
if 'impostor_name' not in st.session_state:
    st.session_state.impostor_name = "Nadie"
if 'target_ods' not in st.session_state:
    st.session_state.target_ods = {}
if 'turn_idx' not in st.session_state:
    st.session_state.turn_idx = 0
if 'card_revealed' not in st.session_state:
    st.session_state.card_revealed = False

# --- 4. FUNCIONES ---
def get_random_avatar():
    return {
        'icon': random.choice(AVATAR_ICONS),
        'color': random.choice(AVATAR_COLORS)
    }

def iniciar_partida():
    if len(st.session_state.players) < 3:
        st.error("Se necesitan mínimo 3 jugadores.")
        return

    lista_juego = st.session_state.players.copy()
    random.shuffle(lista_juego)
    st.session_state.players = lista_juego
    
    idx_impostor = random.randint(0, len(lista_juego) - 1)
    st.session_state.impostor_name = lista_juego[idx_impostor]
    st.session_state.target_ods = random.choice(ODS_LIST)
    
    st.session_state.turn_idx = 0
    st.session_state.card_revealed = False
    st.session_state.stage = 'playing'
    st.session_state.game_active = True

def reset_total():
    st.session_state.players = []
    st.session_state.player_avatars = {}
    st.session_state.stage = 'setup'
    st.session_state.game_active = False
    st.rerun()

# --- 5. INTERFAZ ---

# Sidebar
with st.sidebar:
    st.title("⚙️ Opciones")
    if st.button("🔄 Reiniciar Todo"):
        reset_total()
    
    st.divider()
    st.write("**Escanea para jugar:**")
    url = "https://juego-impostora-ods-8lsdzkchk9wieczwmbgfcg.streamlit.app/"
    qr = qrcode.make(url)
    img_buffer = BytesIO()
    qr.save(img_buffer, format="PNG")
    st.image(img_buffer.getvalue())

# Header
st.markdown("<h1 class='main-header'>LA IMPODSTORA</h1>", unsafe_allow_html=True)

# --- SETUP ---
if st.session_state.stage == 'setup':
    st.markdown("<p class='subtitle'>Añade a las jugadoras para comenzar la misión y salvar el planeta.</p>", unsafe_allow_html=True)
    
    # Formulario para agregar jugadores
    st.markdown("### 🆕 NUEVA AGENTE")
    col1, col2 = st.columns([4, 1])
    with col1:
        new_name = st.text_input("", placeholder="Escribe el nombre...", label_visibility="collapsed")
    with col2:
        if st.button("➕", key="add_btn"):
            if new_name and new_name not in st.session_state.players:
                st.session_state.players.append(new_name)
                st.session_state.player_avatars[new_name] = get_random_avatar()
                st.rerun()
            elif new_name in st.session_state.players:
                st.warning("Ya existe ese agente")

    # Lista de jugadores
    if st.session_state.players:
        st.markdown(f"### Tripulación Actual <span class='counter-badge'>{len(st.session_state.players)}/10 AGENTES</span>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for idx, player in enumerate(st.session_state.players):
            with cols[idx % 3]:
                avatar = st.session_state.player_avatars.get(player, get_random_avatar())
                st.markdown(f"""
                <div class='player-card'>
                    <div class='player-avatar' style='background-color: {avatar["color"]};'>
                        {avatar["icon"]}
                    </div>
                    <div class='player-name'>{player}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("❌", key=f"remove_{idx}"):
                    st.session_state.players.remove(player)
                    st.session_state.player_avatars.pop(player, None)
                    st.rerun()

    st.write("")
    st.markdown("*Minimum 3 players needed to start the mystery.*")
    st.write("")
    
    if st.button("START GAME 🚀", type="primary", disabled=len(st.session_state.players) < 3):
        iniciar_partida()
        st.rerun()

# --- PLAYING ---
elif st.session_state.stage == 'playing':
    current_player = st.session_state.players[st.session_state.turn_idx]
    avatar = st.session_state.player_avatars.get(current_player, get_random_avatar())
    
    st.markdown(f"<p class='subtitle'>Agent {st.session_state.turn_idx + 1} of {len(st.session_state.players)}</p>", unsafe_allow_html=True)
    st.progress((st.session_state.turn_idx + 1) / len(st.session_state.players))

    with st.container():
        st.markdown(f"""
        <div class='player-card' style='padding: 25px;'>
            <div class='player-avatar' style='background-color: {avatar["color"]}; width: 100px; height: 100px; font-size: 3rem;'>
                {avatar["icon"]}
            </div>
            <h2 style='margin: 15px 0;'>{current_player}</h2>
            <p style='color: #666;'>Pass the device to this player. Nobody else should look.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.card_revealed:
            if st.button("👁️ TAP TO REVEAL ROLE", type="primary"):
                st.session_state.card_revealed = True
                st.rerun()
        else:
            es_impostor = (current_player == st.session_state.impostor_name)
            
            if es_impostor:
                st.markdown("""
                <div class="role-card-impostor">
                    <p class="role-title" style="color: #D32F2F;">🔴 YOU ARE THE IMPOSTOR</p>
                    <p style="font-size: 1.2rem; margin: 15px 0;">You don't know the secret topic.</p>
                    <p style="font-size: 1.1rem; color: #666;">Blend in and follow along!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                nombre_ods = st.session_state.target_ods['nombre']
                palabra_ods = st.session_state.target_ods['palabra']
                
                st.markdown(f"""
                <div class="role-card-crew">
                    <p class="role-title" style="color: #1B5E20;">👤 YOU ARE A CREW MEMBER</p>
                    <p style="font-size: 1.2rem; margin: 15px 0;">The secret topic is:</p>
                    <p style="font-size: 1.3rem; font-weight: bold; color: #2E7D32;">{nombre_ods}</p>
                    <p style="font-size: 1.1rem; margin-top: 20px;">Your keyword:</p>
                    <div class="keyword-highlight">{palabra_ods}</div>
                </div>
                """, unsafe_allow_html=True)

            if st.button("Hide and Continue ➡️", type="primary"):
                if st.session_state.turn_idx < len(st.session_state.players) - 1:
                    st.session_state.turn_idx += 1
                    st.session_state.card_revealed = False
                    st.rerun()
                else:
                    st.session_state.stage = 'debate'
                    st.rerun()

# --- DEBATE ---
elif st.session_state.stage == 'debate':
    st.markdown("""
    <div class="debate-card">
        <h2 style="margin: 0; font-size: 2rem;">🗣️ TIME TO DEBATE</h2>
        <p style="font-size: 1.2rem; margin: 20px 0;">Everyone has seen their role. Discuss and vote!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("🏁 END GAME & REVEAL IMPOSTOR", type="primary"):
        st.session_state.stage = 'reveal'
        st.rerun()

# --- REVEAL ---
elif st.session_state.stage == 'reveal':
    st.balloons()
    
    real_impostor = st.session_state.impostor_name
    real_ods_name = st.session_state.target_ods['nombre']
    real_ods_word = st.session_state.target_ods['palabra']
    avatar = st.session_state.player_avatars.get(real_impostor, get_random_avatar())

    st.markdown(f"""
    <div class="reveal-card">
        <h2 style="color: #6A1B9A; margin: 0;">THE IMPOSTOR WAS:</h2>
        <div class='player-avatar' style='background-color: {avatar["color"]}; width: 120px; height: 120px; font-size: 4rem; margin: 20px auto;'>
            {avatar["icon"]}
        </div>
        <p class="impostor-name">{real_impostor}</p>
        <hr style="border: 2px solid #9C27B0; margin: 20px 0;">
        <div style="text-align: left; background: white; border-radius: 15px; padding: 20px; margin-top: 20px;">
            <p style="font-size: 1.2rem; margin: 10px 0;"><b>🌍 Topic:</b> {real_ods_name}</p>
            <p style="font-size: 1.2rem; margin: 10px 0;"><b>🔑 Keyword:</b> {real_ods_word}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Play Again"):
            iniciar_partida()
            st.rerun()
    with col2:
        if st.button("✏️ Change Players"):
            st.session_state.stage = 'setup'
            st.rerun()
