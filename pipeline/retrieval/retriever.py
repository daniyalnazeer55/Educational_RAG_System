"""
Retriever Module
Retrieves relevant context from vector database

"""
 
from typing import List, Dict, Tuple
from utils.text_utils import TextProcessor
from vectordb.chroma_handler import get_chroma_handler
from config.settings import settings
from utils.logger import LoggerFactory
 
 
logger = LoggerFactory.get_logger("retrieval")
 
 
class Retriever:
    """Retrieve relevant documents from database"""
    
    def __init__(self, top_k: int = None):
        """
        Initialize retriever
        
        Args:
            top_k: Number of results to retrieve
        """
        self.vector_db = get_chroma_handler()
        self.top_k = top_k or settings.TOP_K_RESULTS
        self.similarity_threshold = settings.SIMILARITY_THRESHOLD
    
    def retrieve(
        self,
        query: str,
        top_k: int = None,
        filters: Dict = None
    ) -> List[Dict]:
        """
        Retrieve relevant documents
        
        Args:
            query: User query
            top_k: Number of results (uses default if not provided)
            filters: Metadata filters
            
        Returns:
            List of retrieved documents with scores
        """
        if top_k is None:
            top_k = self.top_k
        
        try:
            logger.info(f"Retrieving {top_k} results for query: {query[:100]}")

            ids, documents, distances, metadatas = self.vector_db.query(
                query_text=query,
                top_k=top_k,
                filters=filters
            )
            
            similarities = [1 - (dist / 2) for dist in distances] 

            results = []
            for doc_id, document, similarity, metadata in zip(
                ids, documents, similarities, metadatas
            ):

                if similarity >= self.similarity_threshold:
                    result = {
                        "id": doc_id,
                        "content": document,
                        "similarity_score": round(similarity, 4),
                        "metadata": metadata
                    }
                    results.append(result)
            
            logger.info(f"Retrieved {len(results)} relevant documents")
            
            return results
        
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise
    
    def retrieve_by_chapter(
        self,
        query: str,
        chapter: int = None,
        top_k: int = None
    ) -> List[Dict]:
        """
        Retrieve documents for a specific chapter
        
        Args:
            query: User query
            chapter: Chapter number filter
            top_k: Number of results
            
        Returns:
            List of retrieved documents
        """
        filters = None
        
        if chapter is not None:
            filters = {"chapter": chapter}
        
        return self.retrieve(query, top_k=top_k, filters=filters)
    
    def retrieve_by_book_type(
        self,
        query: str,
        book_type: str = None,
        top_k: int = None
    ) -> List[Dict]:
        """
        Retrieve documents from specific book type
        
        Args:
            query: User query
            book_type: Type of book (textbook or guide)
            top_k: Number of results
            
        Returns:
            List of retrieved documents
        """
        filters = None
        
        if book_type is not None:
            filters = {"document_type": book_type}
        
        return self.retrieve(query, top_k=top_k, filters=filters)
    
    def get_context_string(self, results: List[Dict]) -> str:
        """
        Convert retrieved results to context string
        
        Args:
            results: Retrieved documents
            
        Returns:
            Formatted context string
        """
        if not results:
            return "No relevant information found in the database."
        
        context_parts = []
        context_parts.append("RELEVANT CONTEXT FROM MATHEMATICS MATERIALS:\n")
        context_parts.append("=" * 50 + "\n")
        
        for idx, result in enumerate(results, 1):
            metadata = result.get("metadata", {})
            content = result.get("content", "")
            similarity = result.get("similarity_score", 0)
            
            context_parts.append(f"\n[Source {idx}]")
            context_parts.append(f"Book: {metadata.get('document_type', 'Unknown').capitalize()}")
            
            if metadata.get("chapter"):
                context_parts.append(f"Chapter: {metadata.get('chapter')}")
            
            context_parts.append(f"Relevance: {self._format_similarity(similarity)}")
            context_parts.append(f"\nContent:\n{content[:500]}...")
            context_parts.append("\n" + "-" * 50)
        
        return "\n".join(context_parts)
    
    def _format_similarity(self, score: float) -> str:
        """Format similarity score as readable string"""
        if score >= 0.8:
            return f"Very High ({score:.2%})"
        elif score >= 0.6:
            return f"High ({score:.2%})"
        elif score >= 0.4:
            return f"Moderate ({score:.2%})"
        else:
            return f"Low ({score:.2%})"
    
    def get_source_info(self, results: List[Dict]) -> List[Dict]:
        """
        Extract source information from results
        
        Args:
            results: Retrieved documents
            
        Returns:
            List of source information
        """
        sources = []
        
        for result in results:
            metadata = result.get("metadata", {})
            source = {
                "document_type": metadata.get("document_type", "Unknown"),
                "filename": metadata.get("filename", "Unknown"),
                "chapter": metadata.get("chapter"),
                "confidence": result.get("similarity_score", 0)
            }
            sources.append(source)
        
        return sources
