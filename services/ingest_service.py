# services/ingest_service.py
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from schemas.ingest_schemas import DocumentIngestSchemas
import trafilatura

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

        loader = PyMuPDF4LLMLoader(file_path=source, mode="single")
        data = loader.load()

    elif payload.data_type == "url":
        if not (source.startswith("http://") or source.startswith("https://")):
            raise ValueError("URL source path must start with http:// or https://")

        if source.lower().endswith(".pdf"):
            loader = PyMuPDF4LLMLoader(file_path=source, mode="single")
            data = loader.load()
        else:
            # Use trafilatura for clean main-content extraction
            # (strips nav bars, footers, bot-policy notices, etc.)
            downloaded = trafilatura.fetch_url(source)
            if not downloaded:
                raise ValueError(f"Could not download content from URL: {source}")

            extracted_text = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
            if not extracted_text or not extracted_text.strip():
                raise ValueError(f"No extractable main content found at URL: {source}")

            data = [Document(page_content=extracted_text, metadata={"source": source})]
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
    embeddings = MistralAIEmbeddings(model="mistral-embed")
    os.makedirs(CHROMA_DIR, exist_ok=True)

    Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    return len(splits)
