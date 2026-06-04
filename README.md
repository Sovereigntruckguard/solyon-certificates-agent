# Asistente de Seguros Venus — Emisión Autónoma de COI (ACORD 25) 🚀
### *Proyecto desarrollado para el Google for Startups AI Agents Challenge 2026*

Venus es un agente de IA autónomo de nivel de producción diseñado para solucionar uno de los cuellos de botella más críticos en la industria del transporte por carretera de EE. UU.: la emisión manual de Certificados de Seguro (COI - ACORD 25). 

Utilizando el **Google Agent Development Kit (ADK)** y **Gemini 2.5 Flash**, el asistente transforma una solicitud comercial compleja que normalmente toma horas, en un proceso automatizado, seguro y declarativo que se ejecuta en **menos de 40 segundos**.

---

## 🎯 El Problema y la Solución
Las empresas de logística (Brokers) exigen certificados de seguro actualizados a las compañías de transporte antes de asignarles carga. Este proceso manual genera retrasos operativos masivos.

**Venus automatiza todo el ciclo de vida:**
1. Valida de forma interactiva el número de registro **DOT** del cliente.
2. Consulta de manera segura el estado de la póliza en el backend (simulado mediante almacenamiento seguro).
3. Recopila los datos del *Certificate Holder* y direcciones.
4. Genera físicamente el archivo **PDF ACORD 25** estampando los datos en coordenadas milimétricas utilizando capas vectoriales con `PyMuPDF`.
5. Despacha de forma autónoma el documento vía **protocolo SMTP seguro** a las bandejas de entrada del Asegurado y del Broker en tiempo real.

---

## 🛠️ Arquitectura Multi-Herramienta (Pista 1: Creación)
En lugar de un modelo monolítico o un script estático, el proyecto fue refactorizado siguiendo los estándares más estrictos del ADK, migrando toda la lógica hacia una **intención declarativa** distribuida en tres herramientas independientes mapeadas por el orquestador:

* **`verificar_dot_cliente`**: Microservicio encargado del aislamiento de datos y verificación de estado activo de la póliza.
* **`crear_certificado_pdf`**: Motor de renderizado de documentos que inyecta la fecha actualizada y los metadatos del titular en la plantilla base del formato ACORD.
* **`enviar_correo_smtp`**: Módulo de comunicación cifrada TLS encargado del procesamiento de adjuntos y despacho masivo.

### Estructura del Proyecto conforme al ADK:
```text
mi_agente_certificados/
│
├── database.json              # Backend local de pólizas seguras
├── certificados_base/         # Plantillas originales ACORD 25
├── multi_tool_agent/          # Módulo de Producción del Agente
│   ├── __init__.py            # Inicializador de módulo del framework
│   ├── agent.py               # Cerebro del agente e instrucciones de negocio
│   ├── .env                   # Credenciales y variables de entorno del LLM
│   └── Pruebas_Certificados_Venus.evalset.json  # Set de pruebas nativas
└── test_pdf.py                # Script de Testing de Entorno Local

📈 Control de Calidad y Evaluación (ADK Evals)
Para cumplir con los requisitos rigurosos de ingeniería de software exigidos en el Challenge, implementamos la suite de pruebas nativa google-adk[eval] y el motor de análisis de datos pandas.

El agente cuenta con un Evaluation Set (Pruebas_Certificados_Venus) extraído directamente de sesiones reales de producción para validar de forma automática las siguientes métricas de confiabilidad:

Tool Trajectory Quality: Garantiza que el LLM ejecute la secuencia exacta de microservicios sin desviaciones de lógica.

Response Match & Hallucination Prevention: Mitiga las alucinaciones del modelo asegurando que solo se procesen datos autorizados por el backend.

🚀 Instalación y Despliegue Local
Clonar el repositorio y activar el entorno virtual:

Bash
cd mi_agente_certificados
.venv\Scripts\activate
Instalar dependencias globales y suite de evaluación:

Bash
pip install google-adk[eval] PyMuPDF
Configurar variables de entorno (multi_tool_agent/.env):

Plaintext
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=TU_GEMINI_API_KEY
Lanzar la interfaz Dev UI del ADK:

Bash
adk web --port 8000
Acceda a http://localhost:8000 y seleccione el módulo multi_tool_agent para interactuar con el ecosistema visual del agente.