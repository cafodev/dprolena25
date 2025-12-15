from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st
import os

from config import *
from prompts import *

@st.cache_resource
def initialize_rag_system():

    # Vector Store
    vectorestore = Chroma(
        embedding_function=OpenAIEmbeddings(model=EMBEDDING_MODEL),\
        persist_directory=CHROMA_DB_PATH
    )

    # Verificar si la DB esta vacia e ingerir documentos si es necesario
    try:
        if vectorestore._collection.count() == 0:
            with st.spinner("🚀 Inicializando base de conocimientos (esto puede tardar unos minutos)..."):
                ingest_documents(vectorestore)
    except Exception as e:
        st.error(f"Error accediendo a la base de datos: {e}")

    # Modelos
    llm_queries = ChatOpenAI(model=QUERY_MODEL, temperature=0)
    llm_generation = ChatOpenAI(model=GENERATION_MODEL, temperature=0)

    # Retriever MMR (Maximal Margin Relevance)
    base_retriever = vectorestore.as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs={
            "k": SEARCH_K,
            "lambda_mult": MMR_DIVERSITY_LAMBDA,
            "fetch_k": MMR_FETCH_K
        }
    )

    # Retriever adicional con similarity para comparar
    similarity_retriever = vectorestore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": SEARCH_K}
    )

    # Prompt personalizado para MultiQueryRetriever
    multi_query_prompt = PromptTemplate.from_template(MULTI_QUERY_PROMPT)

    # MultiQueryRetriever con prompt personalizado
    mmr_multi_retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=llm_queries,
        prompt=multi_query_prompt
    )

    # Ensemble Retriever que combinar MMR y similarity
    if ENABLE_HYBRID_SEARCH:
        ensemble_retriever = EnsembleRetriever(
            retrievers=[mmr_multi_retriever, similarity_retriever],
            weights=[0.7, 0.3], # mayor peso a MMR
            similarity_threshold=SIMILARITY_THRESHOLD
        )
        final_retriever = ensemble_retriever
    else:
        final_retriever = mmr_multi_retriever

    prompt = PromptTemplate.from_template(RAG_TEMPLATE)

    # Funcion para formatear y preprocesar los documentos recuperados
    def format_docs(docs):
        formatted = []

        for i, doc in enumerate(docs, 1):
            header = f"[Fragmento {i}]"
            
            if doc.metadata:
                if 'source' in doc.metadata:
                    source = doc.metadata['source'].split("\\")[-1] if '\\' in doc.metadata['source'] else doc.metadata['source']
                    header += f" - Fuente: {source}"
                if 'page' in doc.metadata:
                    header += f" - Pagina: {doc.metadata['page']}"
        
            content = doc.page_content.strip()
            formatted.append(f"{header}\n{content}")
        
        return "\n\n".join(formatted)

    rag_chain = (
        {
            "context": final_retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm_generation
        | StrOutputParser()
    )

    return rag_chain, mmr_multi_retriever


def query_rag(question):
    try:
        rag_chain, retriever = initialize_rag_system()

        # Obtener respuesta
        response = rag_chain.invoke(question)

        # Obtener documentos para mostrarlos
        docs = retriever.get_relevant_documents(question)

        # Formatear los documentos para mostrar
        docs_info = []
        for i, doc in enumerate(docs[:SEARCH_K], 1):
            doc_info = {
                "fragmento": i,
                "contenido": doc.page_content[:1000] + "..." if len(doc.page_content) > 1000 else doc.page_content,
                "fuente": doc.metadata.get('source', 'No especificada').split("\\")[-1],
                "pagina": doc.metadata.get('page', 'No especificada')
            }
            docs_info.append(doc_info)
        
        return response, docs_info
    
    except Exception as e:
        error_msg = f"Error al procesar la cosulta: {str(e)}"
        return error_msg, []
    
def get_retriever_info():
    """Obtiene información sobre la configuración del retriever"""
    return {
        "tipo": f"{SEARCH_TYPE.upper()} + MultiQuery" + (" + Hybrid" if ENABLE_HYBRID_SEARCH else ""),
        "documentos": SEARCH_K,
        "diversidad": MMR_DIVERSITY_LAMBDA,
        "candidatos": MMR_FETCH_K,
        "umbral": SIMILARITY_THRESHOLD if ENABLE_HYBRID_SEARCH else "N/A"
    }

def ingest_documents(vectorstore):
    """Carga, divide e indexa los documentos PDF configurados."""
    all_splits = []
    
    for pdf_file in PDF_FILES:
        file_path = os.path.join(DOCUMENTS_DIR, pdf_file)
        if not os.path.exists(file_path):
            st.warning(f"⚠️ Archivo no encontrado: {pdf_file}")
            continue
            
        st.toast(f"Procesando {pdf_file}...", icon="📄")
        
        # Cargar PDF
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        # Dividir en chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        splits = text_splitter.split_documents(docs)
        
        # Agregar metadata de origen limpia
        for split in splits:
            split.metadata["source"] = pdf_file
            
        all_splits.extend(splits)

    if all_splits:
        # Indexar en lotes para evitar problemas de memoria/limites
        batch_size = 100
        total_batches = len(all_splits) // batch_size + 1
        
        progress_bar = st.progress(0, text="Indexando documentos...")
        
        for i in range(0, len(all_splits), batch_size):
            batch = all_splits[i:i + batch_size]
            vectorstore.add_documents(batch)
            
            # Actualizar progreso
            progress = min((i + batch_size) / len(all_splits), 1.0)
            progress_bar.progress(progress, text=f"Indexando bloque {i // batch_size + 1} de {total_batches}")
            
        progress_bar.empty()
        st.toast("¡Indexación completada correctamente!", icon="✅")
    else:
        st.warning("No se encontraron documentos para procesar.")