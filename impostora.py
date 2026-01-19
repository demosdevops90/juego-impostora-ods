import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. LISTA DE ODS
ODS_LIST = [
    {"id": 1, "nombre": "ODS #1: Fin de la pobreza", "palabra": "Donación"},
    {"id": 2, "nombre": "ODS #2: Hambre cero", "palabra": "Agricultura"},
    {"id": 3, "nombre": "ODS #3: Salud y bienestar", "palabra": "Vacunas"},
    {"id": 4, "nombre": "ODS #4: Educación de calidad", "palabra": "Escuelas"},
    {"id": 5, "nombre": "ODS #5: Igualdad de género", "palabra": "Equidad"},
    {"id": 6, "nombre": "ODS #6: Agua limpia y saneamiento", "palabra": "Grifo"},
    {"id": 7, "nombre": "ODS #7: Energía asequible y no contaminante", "palabra": "Solar"},
    {"id": 8, "nombre": "ODS #8: Trabajo decente y crecimiento económico", "palabra": "Empleo"},
    {"id": 9, "nombre": "ODS #9: Industria, innovación e infraestructuras", "palabra": "Fábrica"},
    {"id": 10, "nombre": "ODS #10: Reducción de las desigualdades", "palabra": "Inclusión"},
    {"id": 11, "nombre": "ODS #11: Ciudades y comunidades sostenibles", "palabra": "Transporte"},
    {"id": 12, "nombre": "ODS #12: Producción y consumo responsables", "palabra": "Reciclaje"},
    {"id": 13, "nombre": "ODS #13: Acción por el clima", "palabra": "Reforestación"},
    {"id": 14, "nombre": "ODS #14: Vida submarina", "palabra": "Coral"},
    {"id": 15, "nombre": "ODS #15: Vida de ecosistemas terrestres", "palabra": "Bosque"},
    {"id": 16, "nombre": "ODS #16: Paz, justicia e instituciones sólidas", "palabra": "Derechos"},
    {"id": 17, "nombre": "ODS #17: Alianzas para lograr los objetivos", "palabra": "Unión"}
]

# 2. CONFIGURACIÓN
st.set_page_config(page_title="La impODStora", page_icon="🕵️‍♀️", layout="centered")

st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; }
        .titulo-container { text-align: center; margin-bottom: 0.5rem; }
        .titulo-centrado { white-space: nowrap; font-size: 2.2rem; font-weight: bold; margin: 0; }
        .emoji-subtitulo { font-size: 3rem; margin-top: -10px; display: block; text-align: center; }
        .revelacion-card {
            border: 4px solid #FF4B4B; padding: 20px; border-radius: 15px;
            text-align: center; background-color: #FFF5F5; margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

if 'game_state' not in st.session_state:
    st.session_state.game_state = 'setup'
    st.session_state.players = []
    st.session_state.impostor_idx = 0
    st.session_state.selected_ods = None
    st.session_state.current_idx = 0
    st.session_state.show_role = False

def start_new_round():
    if len(st.session_state.players) >= 3:
        random.shuffle(st.session_state.players)
        st.session_state.impostor_idx = random.randint(0, len(st.session_state.players) - 1)
        st.session_state.selected_ods = random.choice(ODS_LIST)
        st.session_state.current_idx = 0
        st.session_state.show_role = False
        st.session_state.game_state = 'playing'

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Menú")
    if st.button("⚠️ Reiniciar TODO"):
        st.session_state.game_state = 'setup'
        st.session_state.players = []
        st.rerun()
    st.divider()
    st.write("📢 **Invita a jugar**")
    url = "https://juego-impostora-ods-8lsdzkchk9wieczwmbgfcg.streamlit.app/"
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue())

# PANTALLA A: CONFIGURACIÓN
if st.session_state.game_state == 'setup':
    st.markdown('<div class="titulo-container"><h1 class="titulo-centrado">La impODStora</h1><span class="emoji-subtitulo">🕵️‍♀️</span></div>', unsafe_allow_html=True)
    with st.form("player_form", clear_on_submit=True):
        name = st.text_input("Nombre:")
        if st.form_submit_button("Añadir ➕") and name:
            if name.strip() not in st.session_state.players:
                st.session_state.players.append(name.strip())
                st.rerun()

    if st.session_state.players:
        for p in st.session_state.players:
            col1, col2 = st.columns([0.8, 0.2])
            col1.text(f"👤 {p}")
            if col2.button("❌", key=f"del_{p}"):
                st.session_state.players.remove(p)
                st.rerun()
    
    st.divider()
    if st.button("🚀 ¡COMENZAR A JUGAR!", use_container_width=True, type="primary", 
                 disabled=len(st.session_state.players) < 3):
        start_new_round()
        st.rerun()

# PANTALLA B: REPARTO DE ROLES
elif st.session_state.game_state == 'playing':
    player = st.session_state.players[st.session_state.current_idx]
    st.caption(f"Fase de roles: {st.session_state.current_idx + 1} de {len(st.session_state.players)}")
    
    with st.container(border=True):
        st.markdown(f"<h1 style='text-align: center; margin-top: -15px;'>{player}</h1>", unsafe_allow_html=True)
        if not st.session_state.show_role:
            if st.button("👁️ Ver mi rol", use_container_width=True, type="primary"):
                st.session_state.show_role = True
                st.rerun()
        else:
            if st.session_state.current_idx == st.session_state.impostor_idx:
                st.error("### 🔴 ERES LA IMPOSTORA")
            else:
                ods = st.session_state.selected_ods
                st.success(f"### 👤 TRIPULANTE\n**{ods['nombre']}**\n\nPalabra: **{ods['palabra']}**")

            if st.button("Siguiente jugadora ➡️", use_container_width=True):
                if st.session_state.current_idx < len(st.session_state.players) - 1:
                    st.session_state.current_idx += 1
                    st.session_state.show_role = False
                else:
                    st.session_state.game_state = 'debate'
                st.rerun()

# PANTALLA C: DEBATE (SIN REVELAR)
elif st.session_state.game_state == 'debate':
    st.markdown('<div class="titulo-container"><h1 class="titulo-centrado">🗣️ ¡A Debatir!</h1></div>', unsafe_allow_html=True)
    st.info("Todas las jugadoras han visto su rol. Hablad y tratad de encontrar a la impostora.")
    st.write("Cada una debe decir su palabra relacionada con la ODS oculta.")
    
    st.divider()
    if st.button("🏁 TERMINAR PARTIDA Y REVELAR", use_container_width=True, type="primary"):
        st.session_state.game_state = 'reveal'
        st.rerun()

# PANTALLA D: REVELACIÓN FINAL
elif st.session_state.game_state == 'reveal':
    st.balloons()
    st.markdown('<div class="titulo-container"><h1 class="titulo-centrado">La impODStora</h1><span class="emoji-subtitulo">🕵️‍♀️</span></div>', unsafe_allow_html=True)
    
    impostora_name = st.session_state.players[st.session_state.impostor_idx]
    ods_jugada = st.session_state.selected_ods
    
    st.markdown(f"""
    <div class="revelacion-card">
        <h2 style='color: #FF4B4B;'>🕵️‍♀️ La Impostora era:</h2>
        <h1 style='font-size: 3.5rem;'>{impostora_name}</h1>
        <hr>
        <p><b>{ods_jugada['nombre']}</b></p>
        <p>Palabra clave: <b>{ods_jugada['palabra']}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Nueva ronda", use_container_width=True, type="primary"):
        start_new_round()
        st.rerun()
    if st.button("👥 Editar jugadoras", use_container_width=True):
        st.session_state.game_state = 'setup'
        st.rerun()
