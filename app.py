import streamlit as st
import smtplib
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(
    page_title="Mesa de Ayuda",
    page_icon="🎫",
    layout="centered"
)

TIPOS_PROBLEMA = [
    "Selecciona una opción",
    "Hardware",
    "Software",
    "Red / Conectividad",
    "Acceso o cuenta de usuario",
    "Correo electrónico",
    "Otro",
]

PRIORIDADES = ["Baja", "Media", "Alta", "Crítica"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
    --bg: #E7EBEF;
    --panel: #FDFDFC;
    --ink: #1C2733;
    --muted: #5C6773;
    --line: #C7CFD8;
    --accent: #29527A;
    --baja: #4C8C6B;
    --media: #B8901F;
    --alta: #C2570C;
    --critica: #B3261E;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--ink);
}

.stApp {
    background-color: var(--bg);
    background-image:
        linear-gradient(180deg, rgba(41,82,122,0.04), transparent 220px);
}

.block-container {
    max-width: 680px;
    padding-top: 2.4rem;
}

.mesa-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.3rem;
}
.mesa-titulo {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 2.1rem;
    line-height: 1.1;
    color: var(--ink);
    margin-bottom: 0.3rem;
}
.mesa-subtitulo {
    font-size: 0.95rem;
    color: var(--muted);
    max-width: 48ch;
    margin-bottom: 1.6rem;
}

.ticket-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 2px solid var(--ink);
    padding-bottom: 0.6rem;
    margin-bottom: 1.4rem;
}
.ticket-numero {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.05em;
    color: var(--muted);
}
.ticket-numero strong {
    color: var(--ink);
}
.ticket-estado {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid var(--accent);
    border-radius: 3px;
    padding: 0.15rem 0.5rem;
}

.panel {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 1.8rem 1.9rem 1.5rem;
    box-shadow: 0 1px 2px rgba(28,39,51,0.04), 0 10px 24px -18px rgba(28,39,51,0.5);
}

.campo-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 1.1rem;
    margin-bottom: 0.15rem;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: transparent;
    border: none;
    border-bottom: 1.5px solid var(--line);
    border-radius: 0;
    padding: 0.4rem 0.1rem;
    font-family: 'Inter', sans-serif;
    color: var(--ink);
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-bottom: 1.5px solid var(--accent);
    box-shadow: none;
}

div[data-baseweb="select"] > div {
    background: transparent;
    border: none;
    border-bottom: 1.5px solid var(--line);
    border-radius: 0;
}

div[role="radiogroup"] {
    gap: 0.5rem;
}
div[role="radiogroup"] > label {
    border: 1.5px solid var(--line);
    border-radius: 4px;
    padding: 0.3rem 0.8rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.03em;
    transition: all 0.15s ease;
}
div[role="radiogroup"] > label:nth-of-type(1) { border-color: var(--baja); }
div[role="radiogroup"] > label:nth-of-type(2) { border-color: var(--media); }
div[role="radiogroup"] > label:nth-of-type(3) { border-color: var(--alta); }
div[role="radiogroup"] > label:nth-of-type(4) { border-color: var(--critica); }
div[role="radiogroup"] > label:nth-of-type(1):has(input:checked) { background: var(--baja); color: #fff; }
div[role="radiogroup"] > label:nth-of-type(2):has(input:checked) { background: var(--media); color: #fff; }
div[role="radiogroup"] > label:nth-of-type(3):has(input:checked) { background: var(--alta); color: #fff; }
div[role="radiogroup"] > label:nth-of-type(4):has(input:checked) { background: var(--critica); color: #fff; }

.stButton > button, .stFormSubmitButton > button {
    background-color: var(--ink);
    color: var(--panel);
    border: none;
    border-radius: 4px;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-size: 0.8rem;
    padding: 0.65rem 1.4rem;
    width: 100%;
    margin-top: 1.4rem;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background-color: var(--accent);
    color: #fff;
}

.mesa-pie {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: var(--muted);
    text-align: center;
    margin-top: 1.6rem;
}
</style>
""", unsafe_allow_html=True)


def correo_valido(correo):
    patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(patron, correo) is not None


def enviar_correo(nombre, correo, tipo_problema, prioridad, descripcion, ticket_id):
    servidor = st.secrets["SMTP_SERVER"]
    puerto = int(st.secrets["SMTP_PORT"])
    usuario = st.secrets["SMTP_USER"]
    clave = st.secrets["SMTP_PASSWORD"]
    correo_admin = st.secrets["ADMIN_EMAIL"]

    mensaje = MIMEMultipart()
    mensaje["From"] = usuario
    mensaje["To"] = correo_admin
    mensaje["Subject"] = f"[{ticket_id}] Nuevo reporte de soporte técnico - Prioridad {prioridad}"

    cuerpo = f"""Se ha recibido un nuevo reporte de soporte técnico.

Ticket: {ticket_id}
Nombre del usuario: {nombre}
Correo del usuario: {correo}
Tipo de problema: {tipo_problema}
Prioridad: {prioridad}

Descripción del problema:
{descripcion}
"""
    mensaje.attach(MIMEText(cuerpo, "plain"))

    with smtplib.SMTP(servidor, puerto) as server:
        server.starttls()
        server.login(usuario, clave)
        server.sendmail(usuario, correo_admin, mensaje.as_string())


if "ticket_id" not in st.session_state:
    st.session_state.ticket_id = "ST-" + datetime.now().strftime("%y%m%d-%H%M")

st.markdown('<div class="mesa-eyebrow">Mesa de Ayuda · TI</div>', unsafe_allow_html=True)
st.markdown('<div class="mesa-titulo">Reportar una incidencia</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="mesa-subtitulo">Completa el formulario con el detalle del problema. '
    'El equipo de soporte recibe el reporte de inmediato por correo.</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown(
    f'<div class="ticket-header">'
    f'<div class="ticket-numero">TICKET <strong>{st.session_state.ticket_id}</strong></div>'
    f'<div class="ticket-estado">Sin enviar</div>'
    f'</div>',
    unsafe_allow_html=True
)

with st.form("formulario_reporte"):
    st.markdown('<div class="campo-label">Nombre del usuario</div>', unsafe_allow_html=True)
    nombre = st.text_input("Nombre del usuario", label_visibility="collapsed")

    st.markdown('<div class="campo-label">Correo electrónico</div>', unsafe_allow_html=True)
    correo = st.text_input("Correo electrónico", label_visibility="collapsed")

    st.markdown('<div class="campo-label">Tipo de problema</div>', unsafe_allow_html=True)
    tipo_problema = st.selectbox("Tipo de problema", TIPOS_PROBLEMA, label_visibility="collapsed")

    st.markdown('<div class="campo-label">Nivel de prioridad</div>', unsafe_allow_html=True)
    prioridad = st.radio("Nivel de prioridad", PRIORIDADES, horizontal=True, label_visibility="collapsed")

    st.markdown('<div class="campo-label">Descripción detallada del problema</div>', unsafe_allow_html=True)
    descripcion = st.text_area("Descripción del problema", height=140, label_visibility="collapsed")

    enviado = st.form_submit_button("Enviar reporte")

st.markdown('</div>', unsafe_allow_html=True)

if enviado:
    errores = []

    if not nombre.strip():
        errores.append("El nombre del usuario es obligatorio.")
    if not correo.strip():
        errores.append("El correo electrónico es obligatorio.")
    elif not correo_valido(correo.strip()):
        errores.append("El correo electrónico no tiene un formato válido.")
    if tipo_problema == "Selecciona una opción":
        errores.append("Debes seleccionar un tipo de problema.")
    if not descripcion.strip():
        errores.append("La descripción del problema es obligatoria.")

    if errores:
        for error in errores:
            st.error(error)
    else:
        try:
            enviar_correo(
                nombre.strip(), correo.strip(), tipo_problema, prioridad,
                descripcion.strip(), st.session_state.ticket_id
            )
            st.success("¡Reporte enviado correctamente! Su reporte ha sido enviado al administrador.")
        except Exception as e:
            st.error(f"No se pudo enviar el reporte. Intenta de nuevo más tarde. ({e})")

st.markdown(
    f'<div class="mesa-pie">Ticket {st.session_state.ticket_id} · '
    f'Esta información no se almacena, solo se usa para enviar el reporte</div>',
    unsafe_allow_html=True
)
