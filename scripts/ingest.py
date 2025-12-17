import os
import pickle
import numpy as np
import faiss
import tiktoken
from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno (API KEY)
load_dotenv()

# Configuración
DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
VECTOR_STORE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vector_store")
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "index.faiss")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "index.pkl")

def get_chunks(text, chunk_size=500, overlap=50):
    """Divide el texto en chunks basados en tokens usando tiktoken."""
    try:
        enc = tiktoken.get_encoding("cl100k_base")
    except Exception:
        enc = tiktoken.get_encoding("cl100k_base")

    tokens = enc.encode(text)
    chunks = []
    
    start = 0
    tokens_len = len(tokens)
    
    while start < tokens_len:
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += (chunk_size - overlap)
        
    return chunks

def get_embedding(client, text, model="text-embedding-3-small"):
    """Genera embedding para un texto usando OpenAI."""
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def ingest_docs():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY no encontrada en .env")
        return

    client = OpenAI(api_key=api_key)

    print(f"📂 Buscando PDFs en: {DOCS_DIR}")
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        print(f"⚠️ Directorio {DOCS_DIR} creado. Agregue PDFs y reintente.")
        return

    files = [f for f in os.listdir(DOCS_DIR) if f.endswith('.pdf')]
    if not files:
        print("⚠️ No se encontraron archivos PDF.")
        return

    # Verificar directorio de salida
    if not os.path.exists(VECTOR_STORE_DIR):
        os.makedirs(VECTOR_STORE_DIR)

    all_chunks = []
    all_metadatas = []
    
    for filename in files:
        file_path = os.path.join(DOCS_DIR, filename)
        print(f"📄 Procesando: {filename}")
        
        try:
            reader = PdfReader(file_path)
            full_text = ""
            for page in reader.pages:
                txt = page.extract_text()
                if txt:
                    full_text += txt + "\n"
            
            chunks = get_chunks(full_text)
            print(f"   Cortando en {len(chunks)} chunks...")

            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadatas.append({"source": filename, "chunk_index": i, "text": chunk})
                
        except Exception as e:
            print(f"   ❌ Error procesando {filename}: {e}")

    if not all_chunks:
        print("⚠️ No se generaron chunks.")
        return

    print(f"🧠 Generando embeddings para {len(all_chunks)} chunks... (esto puede tardar)")
    
    # Generar embeddings en lote (o uno por uno si es muy grande, aquí simple)
    # Para producción, hacer batches de 10-100.
    embeddings = []
    batch_size = 50
    total = len(all_chunks)
    
    for i in range(0, total, batch_size):
        batch = all_chunks[i:i+batch_size]
        try:
            resp = client.embeddings.create(input=batch, model="text-embedding-3-small")
            embeddings.extend([d.embedding for d in resp.data])
            print(f"   Procesados {min(i+batch_size, total)}/{total}")
        except Exception as e:
            print(f"   ❌ Error en batch {i}: {e}")

    if not embeddings:
        return

    # Convertir a numpy array para FAISS
    dimension = len(embeddings[0]) # 1536 para text-embedding-3-small
    np_embeddings = np.array(embeddings).astype('float32')

    # Crear índice FAISS
    index = faiss.IndexFlatL2(dimension)
    index.add(np_embeddings)
    
    # Guardar índice y metadatos
    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(all_metadatas, f)

    print(f"\n✨ Ingestión completada.")
    print(f"   Índice guardado en: {INDEX_PATH}")
    print(f"   Metadatos guardados en: {METADATA_PATH}")
    print(f"   Total vectores: {index.ntotal}")

if __name__ == "__main__":
    ingest_docs()
