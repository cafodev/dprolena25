"""
Módulo de Prompts
=================

Este módulo define las plantillas de prompts utilizadas por los modelos de lenguaje.
Incluye prompts para generación de respuestas (RAG), reformulación de consultas
y extracción de información.
"""

# ==========================================
# Prompt Principal del Sistema RAG
# ==========================================
# Instruye al modelo para actuar como experto en idioma guaraní.
RAG_TEMPLATE = """Eres un asistente experto en lengua guaraní (traducción, gramática y cultura).
Basándote ÚNICAMENTE en los siguientes fragmentos del Diccionario y Gramática, responde a la pregunta del usuario.

CONTEXTO (DICCIONARIO / GRAMÁTICA):
{context}

PREGUNTA: {question}

INSTRUCCIONES:
- Proporciona una respuesta clara, educativa y precisa.
- Si es una traducción, proporciona el término en guaraní y su uso contextual si está disponible.
- Si es una duda gramatical, explica la regla basándote en el texto.
- Si encuentras ejemplos en el texto, inclúyelos.
- Si la información no está en el contexto, indícalo claramente.

RESPUESTA:"""

# ==========================================
# Prompt para MultiQuery Retriever
# ==========================================
# Genera variaciones de la pregunta para mejorar la búsqueda vectorial en temas lingüísticos.
MULTI_QUERY_PROMPT = """Eres un experto en lingüística guaraní.
Tu tarea es generar múltiples versiones de la consulta del usuario para recuperar información relevante del diccionario o gramática.

Al generar variaciones de la consulta, considera:
- Posibles variaciones ortográficas del guaraní (uso de 'y', 'j', 'h', tildes nasales).
- Sinónimos en español o guaraní.
- Preguntas relacionadas con gramática, conjugación o vocabulario.

Consulta original: {question}

Genera exactamente 3 versiones alternativas de esta consulta, una por línea, sin numeración ni viñetas:"""

# ==========================================
# Prompt para Análisis de Relevancia
# ==========================================
# Evalúa si un fragmento es lingüísticamente relevante.
RELEVANCE_PROMPT = """Analiza si el siguiente fragmento de texto es relevante para responder la consulta sobre el idioma guaraní.

FRAGMENTO:
{document}

CONSULTA: {question}

¿Es este fragmento relevante? Responde solo con "SÍ" o "NO" y una breve justificación."""

# ==========================================
# Prompt para Extracción de Entidades
# ==========================================
# Extrae términos lingüísticos y definiciones.
ENTITY_EXTRACTION_PROMPT = """Extrae los términos clave del siguiente texto sobre guaraní:

TEXTO:
{text}

Identifica y extrae:
- Términos en Guaraní
- Traducciones al Español
- Categoría Gramatical (sustantivo, verbo, adjetivo, etc.)
- Ejemplos de uso

Formato de respuesta:
TÉRMINOS_GUARANÍ: [lista]
TRADUCCIONES: [lista]
GRAMÁTICA: [lista de reglas/categorías]
EJEMPLOS: [lista de ejemplos]"""