import streamlit as st
import random

# Configuración de datos
ODS_LIST = [
    {"id": 1, "nombre": "Fin de la Pobreza", "palabra": "Donación"},
    {"id": 2, "nombre": "Hambre Cero", "palabra": "Agricultura"},
    {"id": 3, "nombre": "Salud y Bienestar", "palabra": "Vacunas"},
    {"id": 4, "nombre": "Educación de Calidad", "palabra": "Escuelas"},
    {"id": 5, "nombre": "Igualdad de Género", "palabra": "Equidad"},
    {"id": 6, "nombre": "Agua Limpia", "palabra": "Grifo"},
    {"id": 7, "nombre": "Energía Asequible", "palabra": "Solar"},
    {"id": 8, "nombre": "Trabajo Decente", "palabra": "Empleo"},
    {"id": 9, "nombre": "Industria e Innovación", "palabra": "Fábrica"},
    {"id": 10, "nombre": "Reducción de Desigualdades", "palabra": "Justicia"},
    {"id": 11, "nombre": "Ciudades Sostenibles", "palabra": "Transporte"},
    {"id": 12, "nombre": "Producción Responsable", "palabra": "Reciclaje"},
    {"id": 13, "nombre": "Acción por el Clima", "palabra": "Reforestación"},
    {"id": 14, "nombre": "Vida Submarina", "palabra": "Coral"},
    {"id": 15, "nombre": "Ecosistemas Terrestres", "palabra": "Bosque"},
    {"id": 16, "nombre": "Paz y Justicia", "palabra": "Derechos"},
    {"id": 17, "nombre": "Alianzas", "palabra": "Unión"}
]

# Inicialización del Estado
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

def hard_reset():
    st.session_state.game_state = 'setup'
    st.session_state.players = []
    st.session_state.current_idx = 0

st.set_page_config(page_title="La Impostora ODS", page_icon="🕵️‍♀️")
st.title("🕵️‍♀️ La Impostora - ODS")

if st.session_state.game_state == 'setup':
    st.subheader("Configuración")
    with st.form("add_player_form", clear_on_submit=True):
        new_player = st.text_input("Nombre de la jugadora:")
        if st.form_submit_button("Añadir"):
            if new_player.strip() and new_player.strip() not in st.session_state.players:
                st.session_state.players.append(new_player.strip())
                st.rerun()
    
    if st.session_state.players:
        st.write(f"**Jugadoras ({len(st.session_state.players)}):**")
        st.write(", ".join(st.session_state.players))
    
    st.divider()
    if st.button("🚀 ¡EMPEZAR PARTIDA!", use_container_width=True, type="primary", 
                 disabled=len(st.session_state.players) < 3):
        start_new_round()
        st.rerun()

elif st.session_state.game_state == 'playing':
    player = st.session_state.players[st.session_state.current_idx]
    st.write(f"Jugador {st.session_state.current_idx + 1} de {len(st.session_state.players)}")
    
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align: center;'>{player}</h2>", unsafe_allow_html=True)
        if not st.session_state.show_role:
            if st.button("👁️ Ver mi rol", use_container_width=True):
                st.session_state.show_role = True
                st.rerun()
        else:
            if st.session_state.current_idx == st.session_state.impostor_idx:
                st.error("### 🔴 ERES LA IMPOSTORA")
                st.write("¡No dejes que te descubran!")
            else:
                st.success("### 👤 ERES TRIPULANTE")
                ods = st.session_state.selected_ods
                st.info(f"**ODS #{ods['id']}:** {ods['nombre']}\n\n**Palabra:** {ods['palabra']}")

            if st.button("Siguiente jugador ➡️", use_container_width=True):
                if st.session_state.current_idx < len(st.session_state.players) - 1:
                    st.session_state.current_idx += 1
                    st.session_state.show_role = False
                    st.rerun()
                else:
                    st.session_state.game_state = 'finished'
                    st.rerun()

elif st.session_state.game_state == 'finished':
    st.balloons()
    st.success("¡Todos han visto su rol! Empiecen el debate.")
    if st.button("🔄 Jugar otra ronda (Mismas jugadoras)", use_container_width=True, type="primary"):
        start_new_round()
        st.rerun()
    if st.button("👥 Volver a configuración", use_container_width=True):
        st.session_state.game_state = 'setup'
        st.rerun()

if st.session_state.game_state != 'setup':
    st.sidebar.button("⚠️ Borrar todo", on_click=hard_reset)
