import os
import logging
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ChatbotReflex")

# Variables de Configuración
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Validación simple
if not OPENAI_API_KEY:
    logger.warning("⚠️ No se encontró OPENAI_API_KEY en las variables de entorno. El chat no responderá correctamente.")
