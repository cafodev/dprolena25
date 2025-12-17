import os
import pickle
import numpy as np
import faiss
from openai import OpenAI
from .config import logger, OPENAI_API_KEY

# Configuración
VECTOR_STORE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vector_store")
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "index.faiss")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "index.pkl")

class RAGClient:
    """
    Cliente para consultar la base de conocimiento usando FAISS.
    """
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        if not self.api_key:
            logger.warning("OPENAI_API_KEY no encontrada. RAG no funcionará correctamente.")
        
        # Cargar índice y metadatos al inicio (lectura rápida)
        # FAISS y Pickle en modo lectura son seguros con hilos normalmente,
        # pero para máxima seguridad con reflex, cargamos solo si existen.
        self.index = None
        self.metadatas = []
        
        self.load_resources()

    def load_resources(self):
        try:
            if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
                self.index = faiss.read_index(INDEX_PATH)
                with open(METADATA_PATH, "rb") as f:
                    self.metadatas = pickle.load(f)
                logger.info(f"FAISS RAGClient cargado. {self.index.ntotal} vectores.")
            else:
                logger.warning("No se encontraron archivos de índice FAISS. Ejecute 'ingest.py'.")
        except Exception as e:
            logger.error(f"Error cargando recursos FAISS: {e}")

    def query_knowledge_base(self, query: str, n_results: int = 3) -> str:
        """
        Busca contexto relevante para la query.
        """
        if not self.api_key or not self.index:
            return ""
            
        try:
            # 1. Generar embedding de la query
            client = OpenAI(api_key=self.api_key)
            resp = client.embeddings.create(input=[query], model="text-embedding-3-small")
            query_embedding = resp.data[0].embedding
            
            # 2. Buscar en FAISS
            query_vector = np.array([query_embedding]).astype('float32')
            distances, indices = self.index.search(query_vector, k=n_results)
            
            # 3. Recuperar textos
            found_docs = []
            for idx in indices[0]:
                if idx != -1 and idx < len(self.metadatas):
                    doc_data = self.metadatas[idx]
                    found_docs.append(doc_data["text"])
            
            if not found_docs:
                return ""
            
            # Formatear el contexto
            context_str = "\n---\n".join(found_docs)
            return context_str
            
        except Exception as e:
            logger.error(f"Error consultando FAISS: {e}")
            import traceback
            # logger.error(traceback.format_exc())
            return ""

# Instancia global
rag_client = RAGClient()
