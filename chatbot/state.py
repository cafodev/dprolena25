import reflex as rx
import asyncio
from typing import List, Dict
from .llm import LLMClient
from .prompts import SYSTEM_PROMPT
from .config import logger

# Instancia global del cliente LLM (Singleton simple)
llm_client = LLMClient()

class EstadoChat(rx.State):
    """
    Gestiona el estado de la aplicación: historial de mensajes, input del usuario y estado de carga.
    """
    # El prompt del sistema (podría ser editable desde la UI en el futuro)
    system_prompt: str = SYSTEM_PROMPT
    
    # Historial de conversación. 
    # Formato: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    mensajes: List[Dict[str, str]] = []
    
    # Input actual del usuario
    entrada_usuario: str = ""
    
    # Indicador de "Pensando..." / Cargando
    procesando: bool = False

    async def enviar_mensaje(self):
        """Maneja el evento de enviar mensaje."""
        if not self.entrada_usuario.strip():
            return

        # 1. Guardar mensaje del usuario y limpiar input
        nuevo_mensaje = {"role": "user", "content": self.entrada_usuario}
        self.mensajes.append(nuevo_mensaje)
        self.entrada_usuario = ""
        self.procesando = True
        
        # Yield para actualizar la UI inmediatamente (mostrar mensaje usuario y loader)
        yield
        # FORCE UI UPDATE: Give the event loop time to send the 'yield' message to the frontend.
        await asyncio.sleep(0.1)

        # 2. Llamada asíncrona (simulada en estructura) al LLM
        # Reflex maneja handlers asíncronos para no bloquear.
        try:
            # --- ZONA DE EXTENSIÓN FUTURA: MEMORIA LARGA ---
            # Aquí guardaríamos el mensaje en Postgres antes de procesar.
            
            # Ejecutar la llamada bloqueante en un hilo separado para no bloquear el loop de eventos
            respuesta_texto = await asyncio.to_thread(
                llm_client.obtener_respuesta, 
                self.mensajes, 
                self.system_prompt
            )
            
            # --- ZONA DE EXTENSIÓN FUTURA: AUTH ---
            # Verificar si el usuario tiene permisos para ejecutar ciertas acciones (si hubiera tools).

            self.mensajes.append({"role": "assistant", "content": respuesta_texto})
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}", exc_info=True)
            self.mensajes.append({"role": "assistant", "content": "Ocurrió un error inesperado."})
        finally:
            self.procesando = False
            logger.info("Proceso finalizado. UI desbloqueada.")

    def limpiar_conversacion(self):
        """Reinicia el chat."""
        self.mensajes = []
        self.procesando = False

    def set_entrada_usuario(self, valor: str):
        """Setter explícito para el input (a veces necesario en Reflex para control fino)."""
        self.entrada_usuario = valor

    def manejar_tecla(self, key: str):
        """Detecta si se presionó Enter para enviar."""
        if key == "Enter":
            return EstadoChat.enviar_mensaje
