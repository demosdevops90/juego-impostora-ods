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

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La impODStora", page_icon="🕵️‍♀️", layout="centered")

# Estilos CSS
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; }
        .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
        .titulo { text-align: center; font-size: 2.5rem; font-weight: 800; margin-bottom: 0; }
        .subtitulo { text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 20px; }
        
        /* Tarjeta Impostora */
        .card-red {
            background-color: #FFEDED; border: 3px solid #FF4B4B; 
            border-radius: 15px; padding: 20px; text-align: center; margin: 10px 0;
            color: #333333; /* Forzamos color de texto oscuro */
        }
        
        /* Tarjeta Tripulante */
        .card-green {
            background-color: #E8F5E9; border: 3px solid #2E7D32; 
            border-radius: 15px; padding: 20px; text-align: center; margin: 10px 0;
            color: #333333; /* Forzamos color de texto oscuro */
        }
        
        .role-title { font-size: 1.8rem; font-weight: bold; margin: 0; }
        .info-text { font-size: 1.2rem; margin: 10px 0; }
        .keyword-box { 
            background: white; padding: 10px; border-radius: 8px; 
            border: 1px solid #ccc; display: inline-block; margin-top: 5px;
            font-weight: bold; font-size: 1.4rem; color: black;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. GESTIÓN DE ESTADO (SESSION STATE) ---
# Inicializamos TODAS las variables necesarias si no existen
if 'game_active' not in st.session_state:
    st.session_state.game_active = False # Para saber si estamos en partida
if 'stage' not in st.session_state:
    st.session_state.stage = 'setup' # setup, playing, debate, reveal
if 'players' not in st.session_state:
    st.session_state.players = []
if 'impostor_name' not in st.session_state:
    st.session_state.impostor_name = "Nadie"
if 'target_ods' not in st.session_state:
    st.session_state.target_ods = {} # Diccionario vacío
if 'turn_idx' not in st.session_state:
    st.session_state.turn_idx = 0
if 'card_revealed' not in st.session_state:
    st.session_state.card_revealed = False

# --- 4. FUNCIONES LÓGICAS ---
def iniciar_partida():
    if len(st.session_state.players) < 3:
        st.error("Se necesitan mínimo 3 jugadores.")
        return

    # 1. Mezclar jugadores
    lista_juego = st.session_state.players.copy()
    random.shuffle(lista_juego)
    st.session_state.players = lista_juego # Guardamos el orden mezclado
    
    # 2. Elegir índice de impostor
    idx_impostor = random.randint(0, len(lista_juego) - 1)
    
    # 3. GUARDAR EL NOMBRE DEL IMPOSTOR (Crucial)
    st.session_state.impostor_name = lista_juego[idx_impostor]
    
    # 4. Elegir ODS
    st.session_state.target_ods = random.choice(ODS_LIST)
    
    # 5. Configurar estado
    st.session_state.turn_idx = 0
    st.session_state.card_revealed = False
    st.session_state.stage = 'playing'
    st.session_state.game_active = True

def reset_total():
    st.session_state.players = []
    st.session_state.stage = 'setup'
    st.session_state.game_active = False
    st.rerun()

# --- 5. INTERFAZ DE USUARIO ---

# Sidebar
with st.sidebar:
    st.title("Opciones")
    if st.button("⚠️ Borrar todo y Reiniciar"):
        reset_total()
    
    st.divider()
    st.write("Juega escaneando:")
    url = "https://juego-impostora-ods-8lsdzkchk9wieczwmbgfcg.streamlit.app/"
    qr = qrcode.make(url)
    img_buffer = BytesIO()
    qr.save(img_buffer, format="PNG")
    st.image(img_buffer.getvalue())

# CABECERA COMÚN
st.markdown("<h1 class='titulo'>La impODStora 🕵️‍♀️</h1>", unsafe_allow_html=True)

# --- FASE 1: CONFIGURACIÓN (SETUP) ---
if st.session_state.stage == 'setup':
    st.markdown("<p class='subtitulo'>Añade a los jugadores para empezar</p>", unsafe_allow_html=True)
    
    with st.form("add_player"):
        new_name = st.text_input("Nombre del jugador:")
        col_btn1, col_btn2 = st.columns([1,1])
        submitted = st.form_submit_button("Añadir")
        
        if submitted and new_name:
            if new_name not in st.session_state.players:
                st.session_state.players.append(new_name)
                st.rerun()
            else:
                st.warning("Ese nombre ya existe.")

    # Lista de jugadores
    if st.session_state.players:
        st.write(f"**Jugadores ({len(st.session_state.players)}):**")
        cols = st.columns(3)
        for i, p in enumerate(st.session_state.players):
            cols[i % 3].info(p)

    st.divider()
    if st.button("🚀 COMENZAR PARTIDA", type="primary", disabled=len(st.session_state.players) < 3):
        iniciar_partida()
        st.rerun()

# --- FASE 2: JUEGO (PLAYING) ---
elif st.session_state.stage == 'playing':
    current_player = st.session_state.players[st.session_state.turn_idx]
    
    st.markdown(f"<p class='subtitulo'>Turno {st.session_state.turn_idx + 1} de {len(st.session_state.players)}</p>", unsafe_allow_html=True)
    st.progress((st.session_state.turn_idx + 1) / len(st.session_state.players))

    # Caja principal
    with st.container(border=True):
        st.subheader(f"Le toca a: {current_player}")
        st.info("Pasa el móvil a este jugador. Nadie más debe mirar.")
        
        if not st.session_state.card_revealed:
            if st.button("👁️ TOCAR PARA VER ROL"):
                st.session_state.card_revealed = True
                st.rerun()
        else:
            # Lógica de visualización
            es_impostor = (current_player == st.session_state.impostor_name)
            
            if es_impostor:
                st.markdown("""
                <div class="card-red">
                    <p class="role-title" style="color:#D32F2F;">🔴 ERES LA IMPOSTORA</p>
                    <p class="info-text">No conoces el tema.</p>
                    <p>¡Disimula y sigue la corriente!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Recuperamos datos del ODS seguro
                nombre_ods = st.session_state.target_ods['nombre']
                palabra_ods = st.session_state.target_ods['palabra']
                
                st.markdown(f"""
                <div class="card-green">
                    <p class="role-title" style="color:#1B5E20;">👤 ERES TRIPULANTE</p>
                    <p class="info-text">El tema secreto es:</p>
                    <p><b>{nombre_ods}</b></p>
                    <p>Tu palabra clave:</p>
                    <div class="keyword-box">{palabra_ods}</div>
                </div>
                """, unsafe_allow_html=True)

            # Botón siguiente
            if st.button("Ocultar y Siguiente ➡️", type="primary"):
                if st.session_state.turn_idx < len(st.session_state.players) - 1:
                    st.session_state.turn_idx += 1
                    st.session_state.card_revealed = False
                    st.rerun()
                else:
                    st.session_state.stage = 'debate'
                    st.rerun()

# --- FASE 3: DEBATE ---
elif st.session_state.stage == 'debate':
    st.markdown("<div class='card-green' style='background-color:#FFFDE7; border-color:#FBC02D;'>🗣️ <b>TIEMPO DE DEBATE</b><br>Todos han visto su rol. Discutid.</div>", unsafe_allow_html=True)
    
    st.write(" ")
    st.write("Cuando hayáis votado quién es la impostora, pulsad el botón.")
    
    if st.button("🏁 TERMINAR PARTIDA Y VER RESULTADO", type="primary"):
        st.session_state.stage = 'reveal'
        st.rerun()

# --- FASE 4: REVELACIÓN (REVEAL) ---
elif st.session_state.stage == 'reveal':
    st.balloons()
    
    real_impostor = st.session_state.impostor_name
    real_ods_name = st.session_state.target_ods['nombre']
    real_ods_word = st.session_state.target_ods['palabra']

    st.markdown(f"""
    <div class="card-red" style="border-style: dashed;">
        <h2 style='color: #D32F2F; margin:0;'>LA IMPOSTORA ERA:</h2>
        <h1 style='font-size: 3rem; margin: 10px 0; color: #000;'>{real_impostor}</h1>
        <hr>
        <div style='text-align:left; margin-top:20px;'>
            <p>🌍 <b>Tema:</b> {real_ods_name}</p>
            <p>🔑 <b>Palabra:</b> {real_ods_word}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Jugar otra vez"):
            iniciar_partida()
            st.rerun()
    with col2:
        if st.button("
