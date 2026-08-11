# Sistema de Soporte Técnico en la Nube

## Objetivo

Aplicación web que permite reportar una incidencia de soporte técnico mediante un formulario. La app valida la información antes de procesarla y, si todo está correcto, envía automáticamente un correo al administrador con los datos del reporte. No se guarda ninguna información: el reporte solo se usa para validar y enviar el correo.

## Integrantes del equipo

- (nombre del integrante 1)
- (nombre del integrante 2)
- (nombre del integrante 3)

## Funcionamiento de la aplicación

1. El usuario llena el formulario: nombre, correo electrónico, tipo de problema, nivel de prioridad y descripción del problema.
2. Al presionar "Enviar reporte", la app valida que:
   - Todos los campos obligatorios estén completos.
   - El correo tenga un formato válido.
   - Se haya seleccionado un tipo de problema real (no la opción por defecto).
   - Haya una descripción del problema.
3. Si hay errores, se muestran en pantalla y no se envía ningún correo.
4. Si todo es válido, la app arma el correo y lo envía al administrador usando SMTP.
5. Si el envío es exitoso, se muestra el mensaje de confirmación al usuario.

## Tecnologías empleadas

- Python
- Streamlit (interfaz y formulario)
- smtplib y email (librerías estándar de Python para el envío de correo por SMTP)
- Streamlit Community Cloud (despliegue)

## Cómo se gestionan las credenciales de forma segura

Las credenciales del correo (servidor SMTP, usuario, contraseña y correo del administrador) **no están escritas en el código**. Se leen desde `st.secrets`, que en Streamlit Community Cloud se configura en *Settings → Secrets* del proyecto desplegado, y en local se define en un archivo `.streamlit/secrets.toml` que **no se sube al repositorio** (debe estar en `.gitignore`).

El archivo `secrets.toml` debe tener este formato:

```toml
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "tu_correo@gmail.com"
SMTP_PASSWORD = "tu_contraseña_de_aplicación"
ADMIN_EMAIL = "correo_del_administrador@ejemplo.com"
```

> Si usas Gmail, `SMTP_PASSWORD` debe ser una "contraseña de aplicación" generada desde la configuración de seguridad de la cuenta de Google, no la contraseña normal de la cuenta.

## Procedimiento de ejecución

1. Clonar el repositorio.
2. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Crear el archivo `.streamlit/secrets.toml` con las credenciales del correo (ver formato arriba).
4. Correr la aplicación:

   ```bash
   streamlit run app.py
   ```

## Despliegue

La aplicación está pensada para desplegarse en Streamlit Community Cloud: se conecta el repositorio, se agregan las 5 variables de `secrets.toml` en la sección de Secrets del proyecto en la nube, y Streamlit instala `requirements.txt` y corre `app.py` automáticamente.

## Restricción de almacenamiento

Esta aplicación no utiliza base de datos ni guarda los reportes en ningún archivo. Los datos ingresados por el usuario existen únicamente durante el procesamiento del formulario y se descartan una vez enviado (o no enviado) el correo.
