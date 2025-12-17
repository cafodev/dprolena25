import reflex as rx
from .state import EstadoChat

def mensaje_burbuja(mensaje: dict) -> rx.Component:
    """
    Renderiza un único mensaje como una burbuja de chat.
    Estilos diferenciados para usuario y asistente.
    """
    es_usuario = mensaje["role"] == "user"
    
    return rx.box(
        rx.box(
            rx.text(mensaje["content"]),
            bg=rx.cond(es_usuario, "#3b82f6", "#f3f4f6"), # Azul para user, Gris para asistente
            color=rx.cond(es_usuario, "white", "black"),
            padding_x="1em",
            padding_y="0.5em",
            border_radius="lg",
            max_width="80%",
        ),
        display="flex",
        justify_content=rx.cond(es_usuario, "flex-end", "flex-start"),
        margin_y="0.5em",
        width="100%",
    )

def area_chat() -> rx.Component:
    """
    Contenedor principal de los mensajes.
    """
    return rx.vstack(
        rx.foreach(EstadoChat.mensajes, mensaje_burbuja),
        rx.cond(
            EstadoChat.procesando,
            rx.text("Pensando...", color="gray", font_style="italic", font_size="sm"),
        ),
        width="100%",
        height="70vh",
        overflow_y="auto",
        padding="1em",
        border="1px solid #e5e7eb",
        border_radius="md",
        bg="white",
    )

def barra_acciones() -> rx.Component:
    """
    Barra inferior con input y botones.
    """
    return rx.hstack(
        rx.input(
            value=EstadoChat.entrada_usuario,
            on_change=EstadoChat.set_entrada_usuario,
            placeholder="Escribí tu mensaje aquí...",
            width="100%",
            on_key_down=EstadoChat.manejar_tecla,

        ),
        rx.button(
            "Enviar",
            on_click=EstadoChat.enviar_mensaje,
            loading=EstadoChat.procesando,
            bg="black",
            color="white",
            _hover={"bg": "#333"},
        ),
        rx.button(
            "Limpiar",
            on_click=EstadoChat.limpiar_conversacion,
            variant="outline",
            color_scheme="red",
        ),
        width="100%",
        padding_top="1em",
    )

def layout_principal() -> rx.Component:
    """
    Ensambla la página completa.
    """
    return rx.container(
        rx.vstack(
            rx.heading("🤖 Chatbot Experto en Lengua Guaraní", size="6", margin_bottom="1em"),
            area_chat(),
            barra_acciones(),
            width="100%",
            max_width="800px",  # Ancho máximo estilo chat moderno
            margin_x="auto",    # Centrado
            padding_y="2em",
        ),
        height="100vh",
        bg="#fafafa", # Fondo gris muy claro
    )
