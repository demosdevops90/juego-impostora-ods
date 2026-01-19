import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. LISTA DE ODS (Formato: ODS #X: Nombre)
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

# 2. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="La ImpODStora", page_icon="🕵️‍♀️", layout="centered")

# Inyectar CSS para eliminar el espacio superior
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
    </style>
    """, unsafe_allow_html=True)

# 3. INICIALIZACIÓN DEL ESTADO
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'setup'
    st.session_state.players = []
    st.session_state.impostor_idx = 0
    st.session_state.selected_ods = None
    st.session_state.current_idx = 0
    st.session_state.show_role = False

# --- FUNCIONES ---
def start_new_round():
    if len(st.session_state.players) >= 3:
        random.shuffle(st.session_state.players)
        st.session_state.impostor_idx = random.randint(0, len(st.session_state.players) - 1)
        st.session_state.selected_ods = random.choice(ODS_LIST)
        st.session_state.current_idx = 0
        st.session_state.show_role = False
        st.session_state.game_state = 'playing'

def hard_reset():
    st.session_state.game_state = 'setup'
    st.session_state.players = []
    st.session_state.current_idx = 0

def remove_player(name):
    st.session_state.players.remove(name)

# --- BARRA LATERAL (Solo Opciones y QR) ---
with st.sidebar:
    st.header("Menú")
    if st.button("⚠️ Reiniciar TODO"):
        hard_reset()
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
    st.title("🕵️‍♀️ La ImpODStora")
    st.subheader("Añadir jugadoras")
    with st.form("player_form", clear_on_submit=True):
        name = st.text_input("Nombre:")
        if st.form_submit_button("Añadir ➕") and name:
            if name.strip() not in st.session_state.players:
                st.session_state.players.append(name.strip())
                st.rerun()

    if st.session_state.players:
        st.write(f"**Lista ({len(st.session_state.players)}):**")
        for p in st.session_state.players:
            col1, col2 = st.columns([0.8, 0.2])
            col1.text(f"👤 {p}")
            if col2.button("❌", key=f"del_{p}"):
                remove_player(p)
                st.rerun()
    
    st.divider()
    if st.button("🚀 ¡COMENZAR!", use_container_width=True, type="primary", 
                 disabled=len(st.session_state.players) < 3):
        start_new_round()
        st.rerun()

# PANTALLA B: EN JUEGO
elif st.session_state.game_state == 'playing':
    # NO hay st.title aquí para que todo suba
    player = st.session_state.players[st.session_state.current_idx]
    
    st.caption(f"Jugadora {st.session_state.current_idx + 1} de {len(st.session_state.players)}")
    st.progress((st.session_state.current_idx + 1) / len(st.session_state.players))
    
    with st.container(border=True):
        st.markdown(f"<h1 style='text-align: center; margin-top: -20px; color: #FF4B4B;'>{player}</h1>", unsafe_allow_html=True)
        
        if not st.session_state.show_role:
            st.write("Pulsa para ver tu rol en secreto.")
            if st.button("👁️ Ver mi rol", use_container_width=True, type="primary"):
                st.session_state.show_role = True
                st.rerun()
        else:
            if st.session_state.current_idx == st.session_state.impostor_idx:
                st.markdown("""
                <div style='border: 4px solid #FF4B4B; padding: 20px; border-radius: 15px; text-align: center; background-color: #FFF5F5;'>
                    <h1 style='color: #FF4B4B; margin: 0;'>🔴 IMPOSTORA</h1>
                    <p style='color: #333; font-size: 1.1em;'>¡No dejes que te descubran!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                ods = st.session_state.selected_ods
                st.markdown(f"""
                <div style='border: 4px solid #28A745; padding: 15px; border-radius: 15px; text-align: center; background-color: #F5FFF5;'>
                    <h2 style='color: #28A745; margin: 0;'>👤 TRIPULANTE</h2>
                    <hr style='margin: 10px 0;'>
                    <p style='color: #333; font-size: 1.2em; font-weight: bold;'>{ods['nombre']}</p>
                    <div style='background-color: white; padding: 10px; border-radius: 10px; border: 1px solid #ddd;'>
                        <small style='color: #666;'>Ejemplo:</small><br>
                        <b style='color: #000; font-size: 1.3em;'>{ods['palabra']}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.write("")
            if st.button("Siguiente jugadora ➡️", use_container_width=True):
                if st.session_state.current_idx < len(st.session_state.players) - 1:
                    st.session_state.current_idx += 1
                    st.session_state.show_role = False
                    st.rerun()
                else:
                    st.session_state.game_state = 'finished'
                    st.rerun()

# PANTALLA C: FINALIZADO
elif st.session_state.game_state == 'finished':
    st.balloons()
    st.title("🕵️‍♀️ La ImpODStora")
    st.success("### 📣 ¡Debate abierto!")
    
    if st.button("🔄 Nueva ronda", use_container_width=True, type="primary"):
        start_new_round()
        st.rerun()
    
    if st.button("👥 Editar jugadoras", use_container_width=True):
        st.session_state.game_state = 'setup'
        st.rerun()
