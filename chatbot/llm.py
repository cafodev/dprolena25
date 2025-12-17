from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL, logger

class LLMClient:
    """
    Clase para manejar la interacción con OpenAI.
    Centraliza la lógica para facilitar cambios futuros (modelos locales, otros proveedores).
    """
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL

    def obtener_respuesta(self, historial_mensajes: list[dict], system_prompt: str) -> str:
        """
        Envía el historial de chat a OpenAI y obtiene la respuesta.
        
        Args:
            historial_mensajes: Lista de diccionarios {'role': '...', 'content': '...'}
            system_prompt: El prompt del sistema actual.
            
        Returns:
            str: El contenido de la respuesta del asistente.
        """
        try:
            # --- RAG INTEGRATION ---
            # Recuperar contexto relevante siempre
            contexto = ""
            # Asumimos que el último mensaje es el del usuario actual
            last_user_msg = next((m["content"] for m in reversed(historial_mensajes) if m["role"] == "user"), None)
            
            if last_user_msg:
                try:
                    # Import dinámico para evitar errores circulares o de ini
                    from .rag_client import rag_client
                    # Consulta protegida
                    logger.info("Consultando RAG...")
                    # Aumentamos top_k a 8 para tener mas contexto
                    contexto = rag_client.query_knowledge_base(last_user_msg, n_results=8)
                    logger.info(f"RAG recuperó {len(contexto)} caracteres.")
                except Exception as e:
                    logger.error(f"⚠️ Error crítico recuperando contexto RAG (se omite): {e}", exc_info=True)
                    contexto = ""

            # Si hay contexto, lo inyectamos en el system prompt para esta llamada
            system_prompt_final = system_prompt
            if contexto:
                block_context = f"\n\n### INFORMACIÓN DE CONTEXTO (RAG)\nUse esta información SOLO si es relevante:\n{contexto}\n### FIN CONTEXTO\n"
                system_prompt_final += block_context
                logger.info("Contexto RAG inyectado en el prompt.")

            # Preparamos los mensajes incluyendo el sistema al principio
            mensajes_api = [{"role": "system", "content": system_prompt_final}] + historial_mensajes
            
            logger.info(f"Enviando request a OpenAI. Modelo: {self.model}")
            
            # --- ZONA DE EXTENSIÓN FUTURA: TOOLS ---
            # Aquí se podrían definir 'tools' para function calling si fuera necesario.
            # tools = [...]
            # response = self.client.chat.completions.create(..., tools=tools)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=mensajes_api,
                temperature=0, # Creatividad balanceada
            )
            
            contenido = response.choices[0].message.content
            
            # --- ZONA DE EXTENSIÓN FUTURA: RAG ---
            # Antes de llamar a OpenAI, aquí se podría consultar una Vector DB (pgvector/Pinecone)
            # para inyectar contexto relevante en el system_prompt o en los mensajes.
            
            return contenido

        except Exception as e:
            logger.error(f"Error al llamar a OpenAI: {e}")
            return "Lo siento, hubo un error al procesar tu solicitud. Por favor intentá nuevamente más tarde."

    # --- ZONA DE EXTENSIÓN FUTURA: MULTIAGENTE ---
    # Se podrían agregar métodos para delegar tareas a otros agentes especializados.
    # def consultar_agente_sql(self, query): ...
