"""
Punto de entrada principal de la aplicación Reflex.
"""
import reflex as rx
from .ui import layout_principal
from .state import EstadoChat

# Crear la aplicación
app = rx.App(
    theme=rx.theme(appearance="light") # Forzar tema claro por simplicidad
)


# Agregar la página principal
app.add_page(
    layout_principal,
    route="/",
    title="Experto en Lengua Guaraní",
    description="Asistente virtual potenciado por OpenAI"
)
