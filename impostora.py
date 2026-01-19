import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. LISTA ACTUALIZADA DE ODS (Formato: Objetivo X: Nombre)
ODS_LIST = [
    {"id": 1, "nombre": "Objetivo 1: Fin de la pobreza", "palabra": "Donación"},
    {"id": 2, "nombre": "Objetivo 2: Hambre cero", "palabra": "Agricultura"},
    {"id": 3, "nombre": "Objetivo 3: Salud y bienestar", "palabra": "Vacunas"},
    {"id": 4, "nombre": "Objetivo 4: Educación de calidad", "palabra": "Escuelas"},
    {"id": 5, "nombre": "Objetivo 5: Igualdad de género", "palabra": "Equidad"},
    {"id": 6, "nombre": "Objetivo 6: Agua limpia y saneamiento", "palabra": "Grifo"},
    {"id": 7, "nombre": "Objetivo 7: Energía asequible y no contaminante", "palabra": "Solar"},
    {"id": 8, "nombre": "Objetivo 8: Trabajo decente y crecimiento económico", "palabra": "Empleo"},
    {"id": 9, "nombre": "Objetivo 9: Industria, innovación e infraestructuras", "palabra": "Fábrica"},
    {"id": 10, "nombre": "Objetivo 10: Reducción de las desigualdades", "palabra": "Inclusión"},
    {"id": 11, "nombre": "Objetivo 11: Ciudades y comunidades sostenibles", "palabra": "Transporte"},
    {"id": 12, "nombre": "Objetivo 12: Producción y consumo responsables", "palabra": "Reciclaje"},
    {"id": 13, "nombre": "Objetivo 13: Acción por el clima", "palabra": "Reforestación"},
    {"id": 14, "nombre": "Objetivo 14: Vida submarina", "palabra": "Coral"},
    {"id": 15, "nombre": "Objetivo 15: Vida de ecosistemas terrestres", "palabra": "Bosque"},
    {"id": 16, "nombre": "Objetivo 16: Paz, justicia e instituciones sólidas", "palabra": "Derechos"},
    {"id": 17, "nombre": "Objetivo 17: Alianzas para lograr los objetivos", "palabra": "Unión"}
]

# 2. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="La ImpODStora", page_icon="🕵️‍♀️", layout="centered")

# 3. INICIALIZACIÓN DEL ESTADO (Session State)
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'setup'
    st.session_state.players = []
    st.session_state.impostor_idx = 0
    st.session_state.selected_ods = None
    st.session_state.current_idx = 0
    st.session_state.show_role = False

# --- FUNCIONES DE LÓGICA ---
def start_new_round():
    if len(st.session_state.players) >= 3:
        # Mezclamos la lista de jugadores para que el orden sea sorpresa
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

# --- INTERFAZ DE USUARIO ---
st.title("🕵️‍♀️ La ImpODStora")

# BARRA LATERAL (QR e INFO)
with st.sidebar:
    st.header("Opciones")
    if st.button("⚠️ Reiniciar TODO (borrar nombres)"):
        hard_reset()
        st.rerun()
    
    st.divider()
    st.write("📢 **¡Invita a jugar!**")
    url = "https://juego-impostora-ods-8lsdzkchk9wieczwmbgfcg.streamlit.app/"
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="Escanea este QR con otro móvil")

# PANTALLA A: CONFIGURACIÓN
if st.session_state.game_state == 'setup':
#    st.subheader("Añadir jugadoras")
    
    with st.form("player_form", clear_on_submit=True):
        name = st.text_input("Nombre de la jugadora:")
        if st.form_submit_button("Añadir ➕") and name:
            if name.strip() not in st.session_state.players:
                st.session_state.players.append(name.strip())
                st.rerun()

    if st.session_state.players:
        st.write(f"**Jugadoras ({len(st.session_state.players)}):**")
        for p in st.session_state.players:
            col1, col2 = st.columns([0.8, 0.2])
            col1.text(f"👤 {p}")
            if col2.button("❌", key=f"del_{p}"):
                remove_player(p)
                st.rerun()
    
    st.divider()
    if st.button("🚀 ¡COMENZAR LA PARTIDA!", use_container_width=True, type="primary", 
                 disabled=len(st.session_state.players) < 3):
        start_new_round()
        st.rerun()
    if len(st.session_state.players) < 3:
        st.caption("Necesitas al menos 3 jugadoras para empezar.")

# PANTALLA B: EN JUEGO
elif st.session_state.game_state == 'playing':
    player = st.session_state.players[st.session_state.current_idx]
    
    st.write(f"Turno de **{st.session_state.current_idx + 1}** de **{len(st.session_state.players)}**")
    st.progress((st.session_state.current_idx + 1) / len(st.session_state.players))
    
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align: center; color: #FF4B4B;'>{player}</h2>", unsafe_allow_html=True)
#        st.write("Revisa el objetivo y, porfa, pasa el móvil.")
        
        if not st.session_state.show_role:
            if st.button("👁️ Ver mi rol", use_container_width=True, type="primary"):
                st.session_state.show_role = True
                st.rerun()
        else:
            if st.session_state.current_idx == st.session_state.impostor_idx:
                st.markdown("""
                <div style='border: 4px solid #FF4B4B; padding: 20px; border-radius: 15px; text-align: center; background-color: #FFF5F5;'>
                    <h1 style='color: #FF4B4B;'>🔴 IMPOSTORA</h1>
                    <p style='color: #333;'>¡No dejes que te descubran!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                ods = st.session_state.selected_ods
                st.markdown(f"""
                <div style='border: 4px solid #28A745; padding: 20px; border-radius: 15px; text-align: center; background-color: #F5FFF5;'>
                    <h1 style='color: #28A745;'>👤 TRIPULANTE</h1>
                    <hr>
                    <p style='color: #333; font-size: 1.2em;'><b>ODS #{ods['id']}:</b> {ods['nombre']}</p>
                    <p style='background-color: white; padding: 10px; border-radius: 10px; color: #555;'>
                        Palabra clave: <b style='color: #000;'>{ods['palabra']}</b>
                    </p>
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
    st.success("### 📣 ¡Todas han visto su rol!")
    st.write("Empezad el debate. Recordad que cada una debe decir una palabra relacionada con la ODS (la impostora tendrá que improvisar).")
    
    if st.button("🔄 Jugar otra ronda (mismas jugadoras)", use_container_width=True, type="primary"):
        start_new_round()
        st.rerun()
    
    if st.button("👥 Editar lista de jugadoras", use_container_width=True):
        st.session_state.game_state = 'setup'
        st.rerun()
