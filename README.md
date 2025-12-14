# 🇵🇾 Asistente de Lengua Guaraní

Este proyecto es una aplicación interactiva desarrollada en Python que actúa como un **Asistente de Lengua Guaraní**. Utiliza Inteligencia Artificial Generativa y técnicas de RAG (Retrieval-Augmented Generation) para responder consultas sobre vocabulario y gramática guaraní, basándose en documentos de referencia confiables (Diccionario y Gramática).

## 📋 Descripción

El sistema permite a los usuarios interactuar a través de un chat amigable para resolver dudas lingüísticas. A diferencia de un chatbot genérico, este asistente **basa sus respuestas estrictamente en la documentación proporcionada** (PDFs de diccionario y gramática), citando las fuentes y fragmentos específicos utilizados para cada respuesta.

### Funcionalidades Principales
- **Chat Interactivo:** Interfaz tipo chat para realizar preguntas naturales.
- **Respuestas Basadas en Evidencia:** Utiliza RAG para buscar información relevante antes de responder.
- **Citas de Fuentes:** Muestra qué fragmentos del diccionario o gramática se utilizaron.
- **Búsqueda Avanzada:** Implementa búsqueda híbrida (Semántica + Palabras clave) para asegurar precisión.
- **Soporte Multimedia:** (Estructura lista para soportar imágenes/tablas si el contenido lo permite).

---

## 🏗️ Estructura del Código

El proyecto está modularizado para separar la interfaz, la lógica de negocio y la configuración.

```
agente_rag/
│
├── app.py                 # 🖥️ Punto de entrada. Interfaz de usuario con Streamlit.
├── rag_system.py          # 🧠 Lógica del sistema RAG (LangChain, Retrievers).
├── config.py              # ⚙️ Configuración (Modelos, Rutas, Parámetros).
├── prompts.py             # 📝 Plantillas de Prompts para la IA.
├── requirements.txt       # 📦 Dependencias del proyecto.
├── .env                   # 🔐 Variables de entorno (API Keys).
└── chroma_db/             # 💾 Base de datos vectorial persistente (se genera al ejecutar).
```

### Detalles de Componentes

1.  **`app.py`**:
    *   Maneja la interfaz gráfica usando **Streamlit**.
    *   Gestiona el historial de chat (`session_state`).
    *   Muestra los documentos recuperados en una barra lateral o expansores.
    *   Invoca a `query_rag` para procesar las preguntas.

2.  **`rag_system.py`**:
    *   **Core del sistema**. Configura la cadena RAG.
    *   Inicializa la base de datos vectorial (**ChromaDB**) con embeddings de OpenAI.
    *   Implementa un **Ensemble Retriever** que combina:
        *   **MMR (Maximal Marginal Relevance):** Para diversidad en los resultados.
        *   **Similarity Search:** Para relevancia directa.
        *   **MultiQueryRetriever:** Reformula la pregunta del usuario para cubrir más matices.
    *   Genera la respuesta final usando GPT-4o.

3.  **`config.py`**:
    *   Centraliza constantes como nombres de modelos (`gpt-4o`, `gpt-4o-mini`), rutas de archivos y parámetros de búsqueda (`k`, `lambda`). Esto facilita el ajuste de hiperparámetros sin tocar el código lógico.

---

## 🛠️ Tecnologías y Requerimientos

### Tecnologías Clave
*   **Python 3.10+**
*   **Streamlit:** Framework para la UI.
*   **LangChain:** Orquestación de IA y RAG.
*   **OpenAI API:** Modelos de Embeddings y Chat (GPT-4o).
*   **ChromaDB:** Base de datos vectorial local.

### Librerías (requirements.txt)
*   `langchain`, `langchain-community`, `langchain-openai`
*   `streamlit`
*   `python-dotenv`
*   `chromadb`
*   `openai`
*   `tiktoken`

---

## 🚀 Guía de Instalación (Windows)

Sigue estos pasos para instalar y ejecutar el proyecto en un entorno Windows.

### Paso 1: Prerrequisitos
Asegúrate de tener instalado **Python** y **Git**.
*   Para verificar Python: Abre una terminal (PowerShell o CMD) y escribe `python --version`.

### Paso 2: Clonar el Repositorio
Si tienes el código en un zip, descomprímelo. Si es un repositorio git:
```powershell
git clone <url-del-repositorio>
cd agente_rag
```

### Paso 3: Crear un Entorno Virtual
Es recomendable usar un entorno virtual para no afectar tu instalación global de Python.

```powershell
# Crear el entorno virtual llamado "venv"
python -m venv venv

# Activar el entorno virtual
.\venv\Scripts\Activate
```
*(Deberías ver `(venv)` al inicio de tu línea de comandos)*

### Paso 4: Instalar Dependencias
Instala las librerías necesarias listadas en `requirements.txt`.

```powershell
pip install -r requirements.txt
```

### Paso 5: Configurar Variables de Entorno
1.  Crea un archivo llamado `.env` en la misma carpeta que `app.py`.
2.  Abre el archivo `.env` con un editor de texto (Notepad, VS Code).
3.  Agrega tu API Key de OpenAI:

```env
OPENAI_API_KEY=sk-tuclavedeapi...
```
*(Asegúrate de guardar el archivo)*

### Paso 6: Ejecutar la Aplicación
Una vez configurado todo, inicia la aplicación con Streamlit:

```powershell
streamlit run app.py
```

El navegador debería abrirse automáticamente en `http://localhost:8501` mostrando el Asistente de Lengua Guaraní.

---

## 💡 Uso
1.  Escribe tu pregunta en el campo de chat (ej: *"¿Cómo se dice 'perro' en guaraní?"* o *"Explícame la regla de nasalidad"*).
2.  El sistema buscará en los documentos PDF indexados (Diccionario/Gramática).
3.  Te responderá citando los fragmentos encontrados.
