# services/ingest_service.py
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_mistralai import MistralAIEmbeddings
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from schemas.ingest_schemas import DocumentIngestSchemas

load_dotenv()

CHROMA_DIR = "./data/chroma_db"

def process_and_store_document(payload: DocumentIngestSchemas) -> int:
    source = payload.source_path.strip()
    
    # ------------------------------------------------------------------------
    # 1. Routing: Handle PDF vs Web URL Loading
    # ------------------------------------------------------------------------
    if payload.data_type == "pdf":
        if not os.path.exists(source):
            raise ValueError(f"Local file target path does not exist: {source}")
        
        # Lightweight local PDF-to-Markdown processing
        loader = PyMuPDF4LLMLoader(file_path=source, mode="single")
        data = loader.load()

    elif payload.data_type == "url":
        if not (source.startswith("http://") or source.startswith("https://")):
            raise ValueError("URL source path must start with http:// or https://")
        
        # FIX: Check if the web URL is pointing directly to an online PDF file
        if source.lower().endswith(".pdf"):
            # PyMuPDF4LLMLoader natively accepts web-hosted PDF URLs directly!
            loader = PyMuPDF4LLMLoader(file_path=source, mode="single")
            data = loader.load()
        else:
            # Scrape web layout asynchronously if it's standard HTML text
            staged_loader = AsyncHtmlLoader([source])
            html_docs = staged_loader.load()
            
            # Convert noisy HTML boilerplate structure into clean RAG Markdown text
            transformer = Html2TextTransformer()
            data = transformer.transform_documents(html_docs)

    else:
        raise ValueError(f"Ingestion engine type '{payload.data_type}' not supported.")

    # ------------------------------------------------------------------------
    # 2. Text Splitting & Chunk Creation
    # ------------------------------------------------------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=payload.chunk_size, 
        chunk_overlap=payload.chunk_overlap
    )
    splits = splitter.split_documents(data)

    if not splits:
        raise ValueError("Extraction yielded empty document content segments.")

    # ------------------------------------------------------------------------
    # 3. Vectorization & Vector Store Storage
    # ------------------------------------------------------------------------
    # FIXED: Changed parameter from 'model_name' to 'model'
    embeddings = MistralAIEmbeddings(model="mistral-embed")

    Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=CHROMA_DIR
    )
    
    return len(splits)