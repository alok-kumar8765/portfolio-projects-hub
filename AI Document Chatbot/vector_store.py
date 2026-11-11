from typing import List
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.documents import Document
from config import RETRIEVAL_TOP_K


def create_hybrid_retriever(documents: List[Document], api_key: str):
    """
    Creates an Ensemble Retriever combining FAISS (semantic) and BM25 (keyword).
    """
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=api_key
    )
    
    # 1. FAISS Vector Store
    faiss_vectorstore = FAISS.from_documents(documents, embeddings)
    faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k": RETRIEVAL_TOP_K})
    
    # 2. BM25 Keyword Store
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = RETRIEVAL_TOP_K
    
    # 3. Hybrid Ensemble (50/50 weighting)
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever],
        weights=[0.5, 0.5]
    )
    
    return ensemble_retriever, faiss_vectorstore