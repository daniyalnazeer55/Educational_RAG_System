"""
FastAPI Server for RAG System
REST API with Swagger documentation
"""

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
from pipeline.rag_pipline import get_rag_pipeline, initialize_rag
from config.logging_config import app_logger


# Pydantic Models for Request/Response
class QueryRequest(BaseModel):
    """Query request model"""
    query: str = Field(..., min_length=3, max_length=500, description="User question")
    language: str = Field("en", description="Query language: en (English), ur (Urdu), ur_roman (Roman Urdu)")
    top_k: int = Field(3, ge=1, le=20, description="Number of results to retrieve")


class SourceInfo(BaseModel):
    """Source information model"""
    document_type: str
    filename: str
    chapter: Optional[int] = None
    confidence: float


class QueryResponse(BaseModel):
    """Query response model"""
    query: str
    answer: str
    sources: List[SourceInfo]
    confidence_score: float
    response_type: str
    processing_time: Optional[float] = None


class SystemStatus(BaseModel):
    """System status model"""
    status: str
    indexed_documents: int
    embedding_model: str
    vector_database: str
    llm_model: str


# Create FastAPI app
app = FastAPI(
    title="Class 11 Mathematics RAG System",
    description="Retrieval-Augmented Generation system for Class 11 Mathematics education",
    version="1.0.0",
    contact={
        "name": "RAG System Support",
        "email": "support@rag.local"
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    app_logger.info("FastAPI server starting up...")
    
    if not initialize_rag():
        app_logger.error("Failed to initialize RAG system")
        raise RuntimeError("Failed to initialize RAG system")
    
    app_logger.info("RAG system initialized successfully")


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Check API health"""
    return {"status": "healthy", "message": "RAG system is running"}


# System status endpoint
@app.get("/api/v1/status", response_model=SystemStatus, tags=["System"])
async def get_status():
    """Get RAG system status"""
    try:
        pipeline = get_rag_pipeline()
        status = pipeline.get_system_status()
        return SystemStatus(**status)
    except Exception as e:
        app_logger.error(f"Error getting status: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving system status")


# Main query endpoint
@app.post("/api/v1/ask", response_model=QueryResponse, tags=["RAG"])
async def ask_question(request: QueryRequest):
    """
    Ask a question about Class 11 Mathematics
    
    The system will retrieve relevant information from the indexed materials
    and generate an answer based on that context.
    
    Returns:
    - answer: The generated answer
    - sources: List of source materials used
    - confidence_score: Confidence in the answer (0-1)
    """
    try:
        # Validate request
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        app_logger.info(f"Processing query: {request.query[:100]}")
        
        # Get pipeline
        pipeline = get_rag_pipeline()
        
        # Process query
        response = pipeline.process_query(
            query=request.query,
            language=request.language,
            top_k=request.top_k,
            include_sources=True
        )
        
        # Handle error responses
        if response.get("response_type") == "error":
            raise HTTPException(status_code=400, detail=response.get("answer"))
        
        # Convert sources to SourceInfo objects (limit to top 3)
        sources = [SourceInfo(**source) for source in response.get("sources", [])[:3]]
        
        # Create response
        return QueryResponse(
            query=response["query"],
            answer=response["answer"],
            sources=sources,
            confidence_score=response["confidence_score"],
            response_type=response["response_type"],
            processing_time=response.get("processing_time")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing query")


# Search endpoint (without response generation)
@app.post("/api/v1/search", tags=["RAG"])
async def search(
    query: str = Query(..., min_length=3, max_length=500),
    top_k: int = Query(3, ge=1, le=20)
):
    """
    Search for relevant documents without generating a response
    
    Returns raw search results from the vector database.
    """
    try:
        pipeline = get_rag_pipeline()
        results = pipeline.search(query=query, top_k=top_k)
        
        return {
            "query": query,
            "results_count": len(results),
            "results": results
        }
    
    except Exception as e:
        app_logger.error(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error performing search")


# Batch query endpoint
@app.post("/api/v1/batch-ask", tags=["RAG"])
async def batch_ask_questions(requests: List[QueryRequest]):
    """
    Ask multiple questions in one request
    
    Useful for processing multiple queries efficiently.
    """
    try:
        pipeline = get_rag_pipeline()
        responses = []
        
        for req in requests:
            response = pipeline.process_query(
                query=req.query,
                language=req.language,
                top_k=req.top_k,
                include_sources=True
            )
            
            # Convert sources
            sources = [SourceInfo(**source) for source in response.get("sources", [])[:3]]
            
            query_response = QueryResponse(
                query=response["query"],
                answer=response["answer"],
                sources=sources,
                confidence_score=response["confidence_score"],
                response_type=response["response_type"],
                processing_time=response.get("processing_time")
            )
            
            responses.append(query_response)
        
        return {"queries": len(responses), "responses": responses}
    
    except Exception as e:
        app_logger.error(f"Batch query error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing batch queries")


# Info endpoint
@app.get("/api/v1/info", tags=["System"])
async def get_info():
    """Get information about the RAG system"""
    return {
        "name": "Class 11 Mathematics RAG System",
        "version": "1.0.0",
        "description": "Retrieval-Augmented Generation system for answering questions about Class 11 Mathematics",
        "supported_languages": ["English", "Urdu", "Roman Urdu"],
        "features": [
            "Semantic search using embeddings",
            "Multi-language query support",
            "Source attribution",
            "Hallucination prevention"
        ],
        "endpoints": {
            "ask": "/api/v1/ask - Ask a single question",
            "search": "/api/v1/search - Search for documents",
            "batch-ask": "/api/v1/batch-ask - Ask multiple questions",
            "status": "/api/v1/status - Get system status",
            "info": "/api/v1/info - Get system information"
        }
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with documentation"""
    return {
        "message": "Class 11 Mathematics RAG System",
        "documentation": "/docs",
        "alternative_docs": "/redoc"
    }


def main():
    """Run the server"""
    import argparse
    
    parser = argparse.ArgumentParser(description="RAG System FastAPI Server")
    parser.add_argument("--host", default="0.0.0.0", help="Server host")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--reload", action="store_true", help="Auto-reload on code changes")
    parser.add_argument("--workers", type=int, default=1, help="Number of workers")
    
    args = parser.parse_args()
    
    app_logger.info(f"Starting server on {args.host}:{args.port}")
    
    uvicorn.run(
        "server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers,
        log_level="info"
    )


if __name__ == "__main__":
    main()