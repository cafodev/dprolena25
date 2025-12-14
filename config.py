"""
Módulo de Configuración
=======================

Este módulo contiene todas las constantes y configuraciones para el sistema RAG.
Incluye modelos, rutas de archivos y parámetros para el recuperador (Retriever).
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# ==========================================
# Configuración de Modelos de IA
# ==========================================
# Modelo para generar embeddings (text-embedding-3-large es más preciso)
EMBEDDING_MODEL = "text-embedding-3-large"
# Modelo para reformular consultas (más rápido y económico)
QUERY_MODEL = "gpt-4o-mini"
# Modelo para generar la respuesta final (más capaz)
GENERATION_MODEL = "gpt-4o"

# ==========================================
# Configuración de Base de Datos Vectorial
# ==========================================
# Ruta base del proyecto para referencias relativas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ruta donde se persiste la base de datos ChromaDB
CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")

# ==========================================
# Configuración del Mecanismo de Recuperación
# ==========================================
# Tipo de búsqueda: 'mmr' (Maximal Marginal Relevance) para diversidad
SEARCH_TYPE = "mmr"
# Lambda para MMR: 0.5 = balance, 1.0 = solo relevancia. 0.7 favorece diversidad.
MMR_DIVERSITY_LAMBDA = 0.7
# Cantidad de documentos candidatos a buscar inicialmente
MMR_FETCH_K = 20
# Cantidad final de documentos a retornar al LLM
SEARCH_K = 2

# Configuracion alternativa para retriever hibrido
ENABLE_HYBRID_SEARCH = True
SIMILARITY_THRESHOLD = 0.70