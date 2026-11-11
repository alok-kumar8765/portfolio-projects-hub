import io
from typing import List
import pdfplumber
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP


def extract_pdf_with_metadata(file_bytes: bytes, filename: str) -> List[Document]:
    """
    Extracts text page-by-page using pdfplumber to maintain page numbers
    and metadata for precise citations.
    """
    documents = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                doc = Document(
                    page_content=text,
                    metadata={
                        "source": filename,
                        "page": page_idx,
                        "total_pages": len(pdf.pages)
                    }
                )
                documents.append(doc)
    return documents


def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Splits documents into overlapping chunks while retaining metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(documents)