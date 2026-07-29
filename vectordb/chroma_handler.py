"""
ChromaDB Vector Database Handler

"""

from typing import List, Dict, Optional, Tuple
import chromadb
import numpy as np
from config.settings import settings
from embeddings.embedding_generator import get_embedding_generator
from utils.logger import LoggerFactory


logger = LoggerFactory.get_logger("database")


class ChromaDBHandler:
    """Handle ChromaDB vector database operations"""
    
    def __init__(self):
        """Initialize ChromaDB handler"""
        self.db_path = str(settings.CHROMA_DB_PATH)
        self.collection_name = settings.VECTOR_DB_COLLECTION_NAME
        self.client = None
        self.collection = None
        self.embedding_generator = get_embedding_generator()
        
        self.initialize_db()
    
    def initialize_db(self):
        """Initialize ChromaDB client and collection"""
        try:
            logger.info(f"Initializing ChromaDB at {self.db_path}")
            
            # Create client using new API (v0.4+)
            self.client = chromadb.PersistentClient(
                path=self.db_path,
                settings=chromadb.Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"ChromaDB collection '{self.collection_name}' ready")
        
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {str(e)}")
            raise
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict],
        ids: List[str] = None
    ) -> List[str]:
        """
        Add documents to the collection
        
        Args:
            documents: List of document texts
            metadatas: List of metadata dicts for each document
            ids: Optional list of document IDs
            
        Returns:
            List of document IDs
        """
        try:
            # Generate IDs if not provided
            if ids is None:
                ids = [f"doc_{i}" for i in range(len(documents))]
            
            logger.info(f"Adding {len(documents)} documents to database")
            
            # Generate embeddings
            embeddings, _ = self.embedding_generator.generate_embeddings(documents)
            
            # Convert embeddings to list format
            embeddings_list = [embedding.tolist() for embedding in embeddings]
            
            # Add to collection
            self.collection.add(
                documents=documents,
                embeddings=embeddings_list,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Successfully added {len(documents)} documents")
            
            return ids
        
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def query(
        self,
        query_text: str,
        top_k: int = 5,
        filters: Dict = None
    ) -> Tuple[List[str], List[List[str]], List[List[float]], List[Dict]]:
        """
        Query the database
        
        Args:
            query_text: Query text
            top_k: Number of results to return
            filters: Metadata filters
            
        Returns:
            Tuple of (ids, documents, distances, metadatas)
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_generator.generate_embedding(query_text)
            query_embedding_list = query_embedding.tolist()
            
            # Query collection
            results = self.collection.query(
                query_embeddings=[query_embedding_list],
                n_results=top_k,
                where=filters if filters else None
            )
            
            # Extract results
            ids = results['ids'][0] if results['ids'] else []
            documents = results['documents'][0] if results['documents'] else []
            distances = results['distances'][0] if results['distances'] else []
            metadatas = results['metadatas'][0] if results['metadatas'] else []
            
            logger.info(f"Query returned {len(documents)} results")
            
            return ids, documents, distances, metadatas
        
        except Exception as e:
            logger.error(f"Error querying database: {str(e)}")
            raise
    
    def get_document_count(self) -> int:
        """Get number of documents in collection"""
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Error getting document count: {str(e)}")
            return 0
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document
        
        Args:
            doc_id: Document ID
            
        Returns:
            Success status
        """
        try:
            self.collection.delete(ids=[doc_id])
            logger.info(f"Deleted document: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False
    
    def update_document(
        self,
        doc_id: str,
        document: str,
        metadata: Dict = None
    ) -> bool:
        """
        Update a document
        
        Args:
            doc_id: Document ID
            document: New document text
            metadata: New metadata
            
        Returns:
            Success status
        """
        try:
            # Generate new embedding
            embedding = self.embedding_generator.generate_embedding(document)
            embedding_list = embedding.tolist()
            
            # Update in collection
            self.collection.update(
                ids=[doc_id],
                documents=[document],
                embeddings=[embedding_list],
                metadatas=[metadata] if metadata else None
            )
            
            logger.info(f"Updated document: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating document: {str(e)}")
            return False
    
    def clear_collection(self) -> bool:
        """Clear all documents from collection"""
        try:
            doc_count = self.get_document_count()
            
            # Get all document IDs
            results = self.collection.get()
            if results['ids']:
                self.collection.delete(ids=results['ids'])
            
            logger.info(f"Cleared {doc_count} documents from collection")
            return True
        except Exception as e:
            logger.error(f"Error clearing collection: {str(e)}")
            return False
    
    def persist(self):
        """Persist database to disk"""
        try:
            # New API automatically persists, but we can ensure it
            if hasattr(self.client, 'persist'):
                self.client.persist()
            logger.info("Database persisted")
        except Exception as e:
            logger.warning(f"Persist call: {str(e)}")  # May not be needed in new API


# Global ChromaDB handler instance
_chroma_handler: Optional[ChromaDBHandler] = None


def get_chroma_handler() -> ChromaDBHandler:
    """Get or create ChromaDB handler instance"""
    global _chroma_handler
    
    if _chroma_handler is None:
        _chroma_handler = ChromaDBHandler()
    
    return _chroma_handler