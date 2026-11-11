from typing import Dict, List, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from config import DEFAULT_MODEL


SYSTEM_PROMPT = """You are an enterprise AI document assistant. 
Answer the user's question accurately using ONLY the provided context below.

Rules:
1. Rely strictly on the provided Context. Do not invent or assume details.
2. If the context does not contain enough information to answer the question, clearly state: "I couldn't find the answer in the uploaded document(s)."
3. Maintain a professional, concise, and direct tone.

Context:
{context}
"""


def format_docs_with_citations(docs: List[Document]) -> Tuple[str, List[Dict]]:
    """
    Formats doc content for the LLM prompt while collecting metadata for front-end citations.
    """
    context_parts = []
    citations = []

    for idx, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "Unknown Document")
        page = doc.metadata.get("page", "N/A")
        
        context_parts.append(f"[Source {idx} - {source} (Page {page})]:\n{doc.page_content}")
        
        citations.append({
            "source_id": idx,
            "filename": source,
            "page": page,
            "content_snippet": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
        })

    formatted_context = "\n\n---\n\n".join(context_parts)
    return formatted_context, citations


def get_answer(query: str, retriever, api_key: str, model_name: str = DEFAULT_MODEL) -> Dict:
    """
    Retrieves documents, generates a response using Gemini, and returns citations.
    """
    # 1. Initialize Gemini LLM with BYOK key
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.2
    )

    # 2. Retrieve relevant chunks using Hybrid Ensemble Retriever
    retrieved_docs = retriever.invoke(query)
    
    if not retrieved_docs:
        return {
            "answer": "No relevant context found in the uploaded document(s).",
            "citations": []
        }

    # 3. Format retrieved documents and extract citation details
    context_text, citations = format_docs_with_citations(retrieved_docs)

    # 4. Construct Prompt
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}")
    ])
    
    chain = prompt_template | llm

    # 5. Execute Chain
    response = chain.invoke({
        "context": context_text,
        "question": query
    })

    return {
        "answer": response.content,
        "citations": citations
    }