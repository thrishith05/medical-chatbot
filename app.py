import os
import sys
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from services.rag_service import RAGService

# Initialize FastAPI app
app = FastAPI(title="Medical Chatbot API", version="1.0.0")

# Add CORS middleware to allow requests from Hack-A-Cure evaluator
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Service (lazy loading)
rag_service = None

def get_rag_service():
    global rag_service
    if rag_service is None:
        try:
            print("Initializing RAG service...")
            rag_service = RAGService()
            print("RAG service initialized successfully")
        except Exception as e:
            print(f"Error initializing RAG service: {e}")
            raise
    return rag_service

# Request/Response Models
class QueryRequest(BaseModel):
    query: str
    top_k: int

class QueryResponse(BaseModel):
    answer: str
    contexts: List[str]

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    """
    Main query endpoint for medical questions
    """
    try:
        # Validate request
        if not req.query or not req.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        top_k = req.top_k if req.top_k is not None else 5
        top_k = max(1, min(top_k, 20))  # Clamp between 1 and 20
        
        # Get RAG service
        service = get_rag_service()
        
        # Get answer and contexts from RAG service
        result = service.get_answer(req.query, top_k=top_k)
        
        return QueryResponse(
            answer=result["answer"],
            contexts=result["contexts"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
async def root():
    return {"status": "healthy", "service": "Medical Chatbot API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Support deployment platforms (Render, Railway, etc.)
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)

