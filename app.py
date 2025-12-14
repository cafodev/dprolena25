"""
Interfaz de Usuario (Streamlit)
===============================

Este script define la interfaz gráfica de usuario para el Asistente de Lengua Guaraní.
Utiliza Streamlit para crear una aplicación web interactiva que permite a los usuarios
consultar el diccionario y gramática guaraní.
"""

import streamlit as st
from rag_system import query_rag, get_retriever_info

# ==========================================
# Configuración Inicial de la Página
# ==========================================
st.set_page_config(
    page_title="Asistente de Lengua Guaraní",
    page_icon="🇵🇾",
    layout="wide"
)

# Título principal de la aplicación
st.title("🇵🇾 Asistente de Lengua Guaraní: Diccionario y Gramática")
st.divider()

# ==========================================
# Gestión del Estado de la Sesión
# ==========================================
# Inicializamos el historial de chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# Sidebar (Barra Lateral)
# ==========================================
with st.sidebar:
    st.header("📋 Información del Sistema")
    
    # Obtenemos y mostramos detalles técnicos del retriever configurado
    retriever_info = get_retriever_info()
    
    st.markdown("**🔍 Retriever:**")
    st.info(f"Tipo: {retriever_info['tipo']}")
    
    st.markdown("**🤖 Modelos:**")
    st.info("Consultas: GPT-4o-mini\nRespuestas: GPT-4o")
    
    st.divider()
    
    # Botón para reiniciar la conversación
    if st.button("🗑️ Limpiar Chat", type="secondary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# Layout Principal (Columnas)
# ==========================================
# Columna 1 (Izquierda): Chat (2/3 del ancho)
# Columna 2 (Derecha): Documentos (1/3 del ancho)
col1, col2 = st.columns([2, 1])

# --- Columna Izquierda: Historial de Chat ---
with col1:
    st.markdown("### 💬 Chat")
    
    # Iteramos sobre el historial para mostrar mensajes anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- Columna Derecha: Vista de Documentos ---
with col2:
    st.markdown("### 📄 Referencias")
    
    # Mostramos los documentos utilizados para generar la ÚLTIMA respuesta del asistente
    if st.session_state.messages:
        last_message = st.session_state.messages[-1]
        # Solo mostramos documentos si el último mensaje es del asistente y tiene docs adjuntos
        if last_message["role"] == "assistant" and "docs" in last_message:
            docs = last_message["docs"]
            
            if docs:
                for doc in docs:
                    # Usamos expanders para no saturar la vista
                    with st.expander(f"📖 Fragmento {doc['fragmento']}", expanded=False):
                        st.markdown(f"**Fuente:** {doc['fuente']}")
                        st.markdown(f"**Página:** {doc['pagina']}")
                        st.markdown("**Contenido:**")
                        st.text(doc['contenido'])

# ==========================================
# Interacción con el Usuario (Input)
# ==========================================
# Capturamos la entrada del usuario
if prompt := st.chat_input("Escribe tu consulta (ej. ¿Cómo se dice 'Buen día en guaraní'?)..."):
    # 1. Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2. Generar respuesta (mostrando spinner de carga)
    with st.spinner("🔍 Buscando en diccionario y gramática..."):
        # Llamada al sistema RAG
        response, docs = query_rag(prompt)
        # Guardamos respuesta y documentos asociados en el historial
        st.session_state.messages.append({"role": "assistant", "content": response, "docs": docs})
    
    # 3. Recargar la página para actualizar la interfaz
    st.rerun()

# ==========================================
# Pie de Página
# ==========================================
st.divider()
st.markdown(
    "<div style='text-align: center; color: #666;'>🇵🇾 Agente Guaraní con RAG</div>", 
    unsafe_allow_html=True
)