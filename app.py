# app.py
from fastapi import FastAPI, HTTPException, status
from schemas.ingest_schemas import DocumentIngestSchemas, QueryRequest
from services import process_and_store_document, search_and_generate_answer
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Research Index Stack Engine API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ingest", status_code=status.HTTP_200_OK)
def ingest_document(payload: DocumentIngestSchemas):
    try:
        chunks_created = process_and_store_document(payload)
        return {
            "status": "success",
            "chunks_created": chunks_created
        }
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(val_err)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unhandled execution crash occurred during document parsing: {str(e)}"
        )


@app.post("/query")
def query_knowledge_base(payload: QueryRequest):
    try:
        result = search_and_generate_answer(payload.question)
        return result
    except FileNotFoundError as fnf_err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(fnf_err)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unhandled execution crash occurred during query processing: {str(e)}"
        )


@app.get("/")
def read_root():
    return {"status": "healthy", "message": "Advanced Notebook AI Agent API is live!"}
