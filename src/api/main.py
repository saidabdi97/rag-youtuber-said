from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

from ..rag.model import run_rag  # importerar din RAG-engine

app = FastAPI(
    title="RAG Youtuber Said API",
    description="Backend API för RAG-modellen som svarar på frågor baserat på kursmaterial.",
    version="1.0.0",
)

# -------------------------------------------------
# Request model
# -------------------------------------------------
class QueryRequest(BaseModel):
    query: str

# -------------------------------------------------
# Response model
# -------------------------------------------------
class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

# -------------------------------------------------
# RAG Endpoint
# -------------------------------------------------
@app.post("/rag", response_model=QueryResponse)
async def rag_endpoint(request: QueryRequest):
    """Tar emot en fråga och returnerar RAG-svar."""
    
    result = await run_rag(request.query)

    return QueryResponse(
        answer=result.answer,
        sources=result.sources
    )

# -------------------------------------------------
# Health check endpoint
# -------------------------------------------------
@app.get("/")
async def root():
    return {"status": "ok", "message": "RAG API is running!"}
