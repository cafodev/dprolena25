# 🤖 Chatbot Experto en Lengua Guaraní

Este proyecto es un asistente virtual especializado en la lengua guaraní, construido con **Python** y **Reflex**. Utiliza Inteligencia Artificial Generativa (**OpenAI GPT-4o**) potenciada por una base de conocimiento vectorial (**RAG**) para ofrecer respuestas precisas basadas en diccionarios y gramáticas en PDF.

## 🚀 Características

*   **RAG (Retrieval-Augmented Generation):** El bot busca información relevante en documentos PDF locales antes de responder.
*   **Base de Datos Vectorial (FAISS):** Búsqueda semántica ultrarrápida y estable en Windows (reemplazo de ChromaDB).
*   **Interfaz Moderna:** UI construida con Reflex, con indicador de carga ("Pensando...") y diseño limpio.
*   **Arquitectura Robusta:** Manejo asíncrono para evitar bloqueos del servidor y desconexiones de WebSocket.
*   **Contexto Inteligente:** Inyecta fragmentos recuperados en el prompt del sistema para fundamentar las respuestas.

## 📋 Requisitos Previos

*   Python 3.8+ instalado.
*   Una API Key de OpenAI (con créditos disponibles).
*   Archivos PDF de referencia (Diccionarios, Libros de texto) en la carpeta `docs/`.

## 🛠️ Instalación en Windows

Sigue estos pasos para poner en marcha el proyecto:

1.  **Clonar o Descargar el Proyecto**
    Descarga la carpeta del proyecto en tu escritorio.

2.  **Crear un Entorno Virtual**
    Abre una terminal (PowerShell o CMD) en la carpeta del proyecto y ejecuta:
    ```powershell
    python -m venv venv
    ```

3.  **Activar el Entorno**
    ```powershell
    .\venv\Scripts\activate
    ```

4.  **Instalar Dependencias**
    ```powershell
    pip install -r requirements.txt
    ```

5.  **Configurar Variables de Entorno**
    Crea un archivo llamado `.env` en la raíz del proyecto (junto a `rxconfig.py`) y agrega tu clave de API:
    ```env
    OPENAI_API_KEY=sk-tu-clave-de-openai-aqui
    OPENAI_MODEL=gpt-4o-mini
    ```

## 📚 Carga de Conocimiento (Ingestión)

Antes de usar el chat, debes procesar los documentos PDF para crear la "memoria" del bot:

1.  Coloca tus archivos PDF (ej: `Diccionario.pdf`, `Gramatica.pdf`) en la carpeta `docs/`.
2.  Ejecuta el script de ingestión:
    ```powershell
    python scripts/ingest.py
    ```
    *Esto creará la carpeta `vector_store/` con el índice `index.faiss` y los metadatos `index.pkl`.*

## ▶️ Ejecución del Chatbot

Para iniciar la aplicación web:

```powershell
reflex run
```
*Si quieres acceder desde otros dispositivos en tu red local, usa:*
```powershell
reflex run --backend-host 0.0.0.0
```

La aplicación estará disponible en tu navegador en: `http://localhost:3000`

## 🧪 Cómo Probarlo

1.  Abre el navegador en la dirección indicada.
2.  Escribe una pregunta en guaraní o sobre el guaraní.
    *   *Ejemplo: "¿Cómo se dice 'perro' en guaraní?"*
    *   *Ejemplo: "¿Cuál es la regla de los verbos areales?"*
3.  Observa el indicador "Pensando..." mientras el bot consulta la base de datos vectorial (RAG).
4.  Recibirás una respuesta fundamentada en tus documentos PDF.

## 📁 Estructura del Proyecto

*   `chatbot/`: Código fuente de la aplicación Reflex (UI, Estado, Lógica).
    *   `llm.py`: Cliente de OpenAI y orquestador del RAG.
    *   `rag_client.py`: Cliente de búsqueda en FAISS (Thread-Safe).
    *   `state.py`: Gestión del estado del chat (Asíncrono).
*   `scripts/`: Scripts de utilidad.
    *   `ingest.py`: Script para procesar PDFs y generar vectores.
*   `docs/`: Carpeta para tus archivos PDF.
*   `vector_store/`: Almacenamiento local de la base de datos vectorial.
