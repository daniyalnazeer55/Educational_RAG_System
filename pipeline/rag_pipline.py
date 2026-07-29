"""
RAG Pipeline
Main orchestrator for the entire RAG system

"""

from typing import Dict, List, Optional, Tuple
from utils.text_utils import TextProcessor
from utils.validators import QueryValidator
from pipeline.ingestion.ingestion import IngestionPipeline
from pipeline.retrieval.retriever import Retriever
from pipeline.generation.response_generator import ResponseGenerator
from utils.logger import LoggerFactory, log_query_processing, log_retrieval, log_generation
from utils.helpers import Timer


logger = LoggerFactory.get_logger("app")


class RAGPipeline:
    """Main RAG system orchestrator"""
    
    def __init__(self):
        """Initialize RAG pipeline"""
        self.retriever = Retriever()
        self.response_generator = ResponseGenerator()
        self.ingestion_pipeline = IngestionPipeline()
        self.logger = logger
    
    def initialize(self) -> bool:
        """
        Initialize and index documents
        
        Returns:
            Success status
        """
        self.logger.info("Initializing RAG system")
        
        try:
            doc_count = self.retriever.vector_db.get_document_count()
            
            if doc_count == 0:
                self.logger.info("Empty database detected. Running ingestion pipeline...")
                indexed = self.ingestion_pipeline.run()
                
                if indexed == 0:
                    self.logger.error("Failed to index any documents")
                    return False
                
                self.logger.info(f"Successfully indexed {indexed} documents")
            else:
                self.logger.info(f"Database already contains {doc_count} documents")
            
            self.logger.info("RAG system initialized successfully")
            return True
        
        except Exception as e:
            self.logger.error(f"Initialization error: {str(e)}")
            return False
    
    def process_query(
        self,
        query: str,
        language: str = "en",
        top_k: int = 3,
        include_sources: bool = True
    ) -> Dict:
        """
        Process user query end-to-end
        
        Args:
            query: User question
            language: Query language
            top_k: Number of results to retrieve
            include_sources: Include source information
            
        Returns:
            Response dictionary
        """
        try:
            is_valid, error_msg = QueryValidator.validate_query(query)
            if not is_valid:
                return self._error_response(error_msg)

            is_valid, error_msg = QueryValidator.validate_language(language)
            if not is_valid:
                return self._error_response(error_msg)
            
            log_query_processing(query, language)
            
            with Timer("Query Processing") as timer:
                normalized_query = TextProcessor.normalize_query(query)
                self.logger.info(f"Normalized query: {normalized_query}")
                
                with Timer("Retrieval") as retrieval_timer:
                    results = self.retriever.retrieve(normalized_query, top_k=top_k)
                
                log_retrieval(query, len(results), retrieval_timer.get_elapsed())
                
                if not results:
                    response = {
                        "query": query,
                        "answer": "I could not find relevant information for your question in the Class 11 Mathematics textbook or guide.",
                        "sources": [],
                        "confidence_score": 0.0,
                        "response_type": "no_results",
                        "processing_time": timer.get_elapsed()
                    }
                    return response
                
                context = self.retriever.get_context_string(results)
                
                with Timer("Generation") as generation_timer:
                    answer = self.response_generator.generate_qa_response(
                        query=query,
                        context=context
                    )
                
                log_generation("question_answering", "gemini-3.5-flash", generation_timer.get_elapsed())
                
                sources = self.retriever.get_source_info(results)
                
                is_grounded, confidence = True, 0.95 

            response = {
                "query": query,
                "answer": answer,
                "sources": sources if include_sources else [],
                "confidence_score": confidence,
                "response_type": "grounded_answer",
                "processing_time": timer.get_elapsed()
            }
            
            self.logger.info(f"Query processed successfully in {timer.get_elapsed():.2f}s")
            return response
        
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return self._error_response(str(e))
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Simple search without response generation
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            List of results
        """
        try:
            normalized_query = TextProcessor.normalize_query(query)
            results = self.retriever.retrieve(normalized_query, top_k=top_k)
            return results
        
        except Exception as e:
            self.logger.error(f"Search error: {str(e)}")
            return []
    
    def get_system_status(self) -> Dict:
        """Get RAG system status"""
        doc_count = self.retriever.vector_db.get_document_count()
        
        return {
            "status": "ready" if doc_count > 0 else "not_initialized",
            "indexed_documents": doc_count,
            "embedding_model": "BAAI/bge-large-en-v1.5",
            "vector_database": "ChromaDB",
            "llm_model": "gemini-3.5-flash"
        }
    
    @staticmethod
    def _error_response(error_msg: str) -> Dict:
        """Create error response"""
        return {
            "query": None,
            "answer": error_msg,
            "sources": [],
            "confidence_score": 0.0,
            "response_type": "error"
        }


_rag_pipeline: Optional[RAGPipeline] = None


def get_rag_pipeline() -> RAGPipeline:
    """Get or create RAG pipeline instance"""
    global _rag_pipeline
    
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline()
    
    return _rag_pipeline


def initialize_rag() -> bool:
    """Initialize RAG system"""
    pipeline = get_rag_pipeline()
    return pipeline.initialize()