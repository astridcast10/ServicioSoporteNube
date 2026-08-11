import streamlit as st
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(
    page_title="Soporte Técnico",
    page_icon="🛠️",
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


def correo_valido(correo):
    patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(patron, correo) is not None


def enviar_correo(nombre, correo, tipo_problema, prioridad, descripcion):
    servidor = st.secrets["SMTP_SERVER"]
    puerto = int(st.secrets["SMTP_PORT"])
    usuario = st.secrets["SMTP_USER"]
    clave = st.secrets["SMTP_PASSWORD"]
    correo_admin = st.secrets["ADMIN_EMAIL"]

    mensaje = MIMEMultipart()
    mensaje["From"] = usuario
    mensaje["To"] = correo_admin
    mensaje["Subject"] = f"Nuevo reporte de soporte técnico - Prioridad {prioridad}"

    cuerpo = f"""Se ha recibido un nuevo reporte de soporte técnico.

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


st.title("🛠️ Sistema de Soporte Técnico")
st.write("Reporta una incidencia y el equipo de soporte la recibirá directamente por correo.")

with st.form("formulario_reporte"):
    nombre = st.text_input("Nombre del usuario")
    correo = st.text_input("Correo electrónico")
    tipo_problema = st.selectbox("Tipo de problema", TIPOS_PROBLEMA)
    prioridad = st.selectbox("Nivel de prioridad", PRIORIDADES)
    descripcion = st.text_area("Descripción detallada del problema", height=150)

    enviado = st.form_submit_button("Enviar reporte")

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
            enviar_correo(nombre.strip(), correo.strip(), tipo_problema, prioridad, descripcion.strip())
            st.success("¡Reporte enviado correctamente! Su reporte ha sido enviado al administrador.")
        except Exception as e:
            st.error(f"No se pudo enviar el reporte. Intenta de nuevo más tarde. ({e})")
