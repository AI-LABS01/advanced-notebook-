# schemas/ingest_schemas.py
from typing import Literal, Optional
from pydantic import BaseModel, Field, HttpUrl


class DocumentIngestSchemas(BaseModel):
    data_type: Literal["pdf", "url", "image"] = Field(
        ...,
        description="The format of the input data. Allowed options: 'pdf', 'url', 'image'."
    )
    source_path: str = Field(
        ...,
        description="The url or absolute system filepath to the documents"
    )
    chunk_size: Optional[int] = Field(
        1000, description="The size of text segments for splitting."
    )
    chunk_overlap: Optional[int] = Field(
        10, description="The text overlap value between consecutive chunks."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "data_type": "url",
                "source_path": "https://www.apple.com/in/store",
                "chunk_size": 1000,
                "chunk_overlap": 10
            }
        }


class QueryRequest(BaseModel):
    question: str = Field(..., description="The user's natural language question")