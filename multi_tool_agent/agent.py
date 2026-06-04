import os
import json
import fitz
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent

# Cargar variables de entorno del archivo .env de forma segura
load_dotenv()

# ==========================================
# TOOL 1: VERIFICACIÓN SEGURA DE PÓLIZA
# ==========================================
def verificar_dot_cliente(dot: str) -> dict:
    """Busca en la base de datos si el número DOT ingresado tiene una póliza activa.
    
    Args:
        dot (str): El número de registro DOT de la compañía de transporte.
        
    Returns:
        dict: Estado de la búsqueda y el nombre de la empresa si existe.
    """
    try:
        with open('database.json', 'r') as f:
            db = json.load(f)
        
        if dot in db:
            return {
                "status": "success",
                "mensaje": "Póliza activa verificada.",
                "empresa_nombre": db[dot]['nombre']
            }
        else:
            return {
                "status": "error",
                "mensaje": f"El número DOT {dot} no se encuentra registrado en el sistema de Venus Ins Group."
            }
    except Exception as e:
        return {"status": "error", "mensaje": f"Fallo en la consulta de base de datos: {str(e)}"}

# ==========================================
# TOOL 2: GENERACIÓN Y ESTAMPADO DE PDF
# ==========================================
def crear_certificado_pdf(dot: str, holder_nombre: str, holder_direccion: str, holder_ciudad_estado_zip: str) -> dict:
    """Genera el archivo PDF ACORD 25 estampando la fecha y los datos del Certificate Holder.
    
    Args:
        dot (str): Número DOT del cliente para localizar su PDF base.
        holder_nombre (str): Nombre de la empresa o entidad Broker del Holder.
        holder_direccion (str): Dirección física del Holder.
        holder_ciudad_estado_zip (str): Ciudad, Estado y Código Postal del Holder.
        
    Returns:
        dict: Estado de la creación física del archivo.
    """
    try:
        with open('database.json', 'r') as f:
            db = json.load(f)
            
        ruta_pdf_base = db[dot]['pdf_base']
        doc = fitz.open(ruta_pdf_base)
        pagina = doc[0]
        
        fecha_hoy = datetime.now().strftime("%m/%d/%Y")
        texto_holder = f"{holder_nombre}\n{holder_direccion}\n{holder_ciudad_estado_zip}"
        
        # Coordenadas calibradas con tus pruebas visuales exitosas
        pagina.insert_text(fitz.Point(520, 45), fecha_hoy, fontsize=10, color=(0, 0, 0))
        pagina.insert_text(fitz.Point(55, 690), texto_holder, fontsize=10, color=(0, 0, 0))
        
        nombre_archivo = f"Certificado_Generado_{dot}.pdf"
        doc.save(nombre_archivo)
        doc.close()
        
        return {
            "status": "success",
            "mensaje": "Archivo PDF generado de forma segura en el almacenamiento local.",
            "archivo_ruta": nombre_archivo
        }
    except Exception as e:
        return {"status": "error", "mensaje": f"Fallo al estampar capas en el PDF: {str(e)}"}

# ==========================================
# TOOL 3: DESPACHO AUTOMÁTICO SMTP
# ==========================================
def enviar_correo_smtp(dot: str, email_cliente: str, email_broker: str) -> dict:
    """Realiza la conexión SMTP segura para enviar el certificado generado a los destinatarios.
    
    Args:
        dot (str): Número DOT para identificar el documento a adjuntar.
        email_cliente (str): Correo del asegurado (ej. Elizabeth).
        email_broker (str): Correo del intermediario o broker.
        
    Returns:
        dict: Confirmación de envío del protocolo de comunicación.
    """
    try:
        with open('database.json', 'r') as f:
            db = json.load(f)
            
        # Extracción segura y dinámica desde las variables de entorno (.env)
        remitente = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASSWORD")
        
        if not remitente or not password:
            return {
                "status": "error",
                "mensaje": "Faltan las credenciales SMTP de entorno (EMAIL_USER o EMAIL_PASSWORD)."
            }
        
        nombre_archivo = f"Certificado_Generado_{dot}.pdf"
        
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = f"{email_cliente}, {email_broker}"
        msg['Subject'] = f"Certificado de Seguro COI - {db[dot]['nombre']}"
        
        cuerpo = f"Hola,\n\nAdjunto encontrarás el Certificado de Seguro automático para {db[dot]['nombre']}.\n\nEste documento ha sido generado de forma automatizada por el Asistente Inteligente de Venus Ins Group."
        msg.attach(MIMEText(cuerpo, 'plain'))
        
        with open(nombre_archivo, "rb") as f:
            adjunto = MIMEApplication(f.read(), _subtype="pdf")
            adjunto.add_header('Content-Disposition', 'attachment', filename=nombre_archivo)
            msg.attach(adjunto)
            
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.send_message(msg)
        server.quit()
        
        return {
            "status": "success",
            "mensaje": "Protocolo SMTP completado. Mensaje enviado a las bandejas de entrada."
        }
    except Exception as e:
        return {"status": "error", "mensaje": f"Fallo en la conexión o autenticación SMTP: {str(e)}"}

# ==========================================
# CEREBRO AGENTE MULTI-HERRAMIENTAS
# ==========================================
root_agent = Agent(
    name="Asistente_Seguros_Venus",
    model="gemini-2.5-flash",
    description="Agente comercial autónomo para procesar y despachar Certificados de Seguro de Camiones.",
    instruction="""
    Eres el agente de IA de producción de Venus Ins Group. Tu labor es automatizar la emisión de Certificados de Seguro.
    
    Sigue estrictamente estas reglas de negocio interactivas:
    1. Saluda y solicita el Número DOT de la empresa de transporte.
    2. Cuando te den el número, invoca inmediatamente la herramienta `verificar_dot_cliente`. 
       - Si el estado es 'error', infórmale al usuario y pídele verificar el número.
       - Si el estado es 'success', confírmale el nombre de su empresa y continúa al paso 3.
    3. Solicita de forma clara la información del Certificate Holder: Nombre legal, Dirección, Ciudad, Estado y Código Postal.
    4. Solicita los dos correos electrónicos a donde se enviará el documento (Asegurado/Cliente y Broker).
    5. Ejecuta de forma consecutiva la herramienta `crear_certificado_pdf` para estampar los datos, y luego la herramienta `enviar_correo_smtp` para despacharlo a las direcciones dadas.
    6. Entrega un mensaje final de éxito muy profesional confirmando el envío.
    """,
    tools=[verificar_dot_cliente, crear_certificado_pdf, enviar_correo_smtp]
)