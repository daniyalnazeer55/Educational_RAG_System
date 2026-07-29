"""
Ingestion Pipeline
Orchestrates loading, processing, and indexing of documents

"""
 
from typing import List
from pipeline.ingestion.document_loader import DocumentLoader
from pipeline.ingestion.document_processor import DocumentProcessor
from vectordb.chroma_handler import get_chroma_handler
from utils.logger import LoggerFactory
 
 
logger = LoggerFactory.get_logger("app")
 
 
class IngestionPipeline:
    """Main ingestion pipeline"""
    
    def __init__(self):
        """Initialize ingestion pipeline"""
        self.document_loader = DocumentLoader()
        self.document_processor = DocumentProcessor()
        self.vector_db = get_chroma_handler()
    
    def run(self) -> int:
        """
        Run the complete ingestion pipeline
        
        Returns:
            Number of documents indexed
        """
        logger.info("Starting document ingestion pipeline")
        
        try:
            logger.info("Step 1: Loading documents from disk")
            documents = self.document_loader.load_all_documents()
            
            if not documents:
                logger.warning("No documents found to index")
                return 0
            
            logger.info(f"Loaded {len(documents)} documents")

            logger.info("Step 2: Processing documents into chunks")
            chunks_data = self.document_processor.process_batch(documents)
            
            if not chunks_data:
                logger.warning("No chunks generated from documents")
                return 0
            
            logger.info(f"Created {len(chunks_data)} chunks")

            logger.info("Step 3: Indexing chunks into vector database")
            indexed_count = self.index_chunks(chunks_data)
            
            logger.info(f"Successfully indexed {indexed_count} chunks")

            self.vector_db.persist()
            logger.info("Database persisted to disk")
            
            return indexed_count
        
        except Exception as e:
            logger.error(f"Error in ingestion pipeline: {str(e)}")
            raise
    
    def index_chunks(self, chunks_data: List[tuple]) -> int:
        """
        Index chunks into vector database
        
        Args:
            chunks_data: List of (chunk, metadata) tuples
            
        Returns:
            Number of indexed chunks
        """
        documents = []
        metadatas = []
        ids = []
        
        for idx, (chunk, metadata) in enumerate(chunks_data):
            documents.append(chunk)
            metadatas.append(metadata)
            ids.append(f"chunk_{idx}")
        
        try:
            self.vector_db.add_documents(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            return len(documents)
        
        except Exception as e:
            logger.error(f"Error indexing chunks: {str(e)}")
            raise
    
    def check_database_status(self) -> dict:
        """
        Check status of indexed database
        
        Returns:
            Status information
        """
        doc_count = self.vector_db.get_document_count()
        
        status = {
            "document_count": doc_count,
            "database_path": str(self.vector_db.db_path),
            "collection_name": self.vector_db.collection_name,
            "status": "ready" if doc_count > 0 else "empty"
        }
        
        return status
 
 
def run_ingestion_pipeline() -> int:
    """
    Run the ingestion pipeline
    
    Returns:
        Number of documents indexed
    """
    pipeline = IngestionPipeline()
    return pipeline.run()
