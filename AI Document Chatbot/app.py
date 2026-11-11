import streamlit as st
import config
from document_processor import extract_pdf_with_metadata, chunk_documents
from vector_store import create_hybrid_retriever
from qa_chain import get_answer

# Page Configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide"
)

st.title(f"{config.APP_ICON} {config.APP_TITLE}")
st.caption("Production-grade document intelligence with Hybrid Search & Gemini AI")

# --- SIDEBAR: BYOK & FILE UPLOAD ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Initialize api_key in session state if not present
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    entered_key = st.text_input(
        "Enter Google Gemini API Key", 
        value=st.session_state.api_key,
        type="password",
        help="Your key is saved in your active session. Change it here anytime."
    )
    
    if entered_key != st.session_state.api_key:
        st.session_state.api_key = entered_key

    selected_model = st.selectbox(
        "Select Gemini Model",
        ["gemini-1.5-pro", "gemini-pro","gemini-1.5-flash"],
        index=0
    )
    
    st.divider()
    st.header("📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF Files", 
        type=["pdf"], 
        accept_multiple_files=True
    )
    
    process_button = st.button("⚡ Process & Index Documents", use_container_width=True)

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "retriever" not in st.session_state:
    st.session_state.retriever = None

# --- DOCUMENT PROCESSING WORKFLOW ---
if process_button:
    if not st.session_state.api_key:
        st.sidebar.error("Please enter a valid Google Gemini API Key!")
    elif not uploaded_files:
        st.sidebar.warning("Please upload at least one PDF file.")
    else:
        with st.spinner("Parsing PDFs, generating embeddings, and building hybrid index..."):
            try:
                all_raw_docs = []
                for file in uploaded_files:
                    bytes_data = file.read()
                    docs = extract_pdf_with_metadata(bytes_data, file.name)
                    all_raw_docs.extend(docs)
                
                # Split documents into chunks preserving metadata
                chunks = chunk_documents(all_raw_docs)
                
                # Create Hybrid (FAISS + BM25) Retriever using session state key
                retriever, _ = create_hybrid_retriever(chunks, st.session_state.api_key)
                
                # Store in session state
                st.session_state.retriever = retriever
                st.sidebar.success(f"Indexed {len(uploaded_files)} PDF(s) into {len(chunks)} chunks!")
            except Exception as e:
                st.sidebar.error(f"Error building index: {str(e)}")

# --- CHAT INTERFACE ---
# Display prior chat messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "citations" in msg and msg["citations"]:
            with st.expander("📌 View Source Citations"):
                for cite in msg["citations"]:
                    st.write(f"**Doc:** `{cite['filename']}` | **Page:** `{cite['page']}`")
                    st.caption(f"*\"{cite['content_snippet']}\"*")

# Handle New User Input
if prompt := st.chat_input("Ask a question about your uploaded documents..."):
    if not st.session_state.api_key:
        st.error("Please provide your Google Gemini API key in the sidebar to chat.")
    elif st.session_state.retriever is None:
        st.warning("Please upload and click 'Process & Index Documents' first.")
    else:
        # User message UI
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant response UI
        with st.chat_message("assistant"):
            with st.spinner("Searching documents & generating answer..."):
                res = get_answer(
                    query=prompt,
                    retriever=st.session_state.retriever,
                    api_key=st.session_state.api_key,
                    model_name=selected_model
                )
                
                st.markdown(res["answer"])
                
                if res["citations"]:
                    with st.expander("📌 View Source Citations"):
                        for cite in res["citations"]:
                            st.write(f"**Doc:** `{cite['filename']}` | **Page:** `{cite['page']}`")
                            st.caption(f"*\"{cite['content_snippet']}\"*")
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": res["answer"],
                    "citations": res["citations"]
                })