"""
Vercel serverless function for Medical Chatbot API
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json

# Initialize FastAPI app
app = FastAPI(title="Medical Chatbot API", version="1.0.0")

# Add CORS middleware
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
            # For Vercel, we need to handle ChromaDB differently
            from services.rag_service import RAGService
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

# Vercel serverless handler
def handler(request):
    return app

@app.post("/api/query")
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

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/")
async def root():
    return {"status": "healthy", "service": "Medical Chatbot API"}

# For Vercel serverless
def main(request):
    """Main handler for Vercel serverless function"""
    return handler(request)

