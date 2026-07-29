"""
Embedding Model Handler
Handles generation of embeddings for documents and queries

"""
 
from typing import List, Optional
from sentence_transformers import SentenceTransformer
import numpy as np
from config.settings import settings
from config.model_config import EMBEDDING_MODELS
from utils.logger import LoggerFactory
 
 
logger = LoggerFactory.get_logger("embedding")
 
 
class EmbeddingModel:
    """Handle embedding generation using sentence transformers"""
    
    def __init__(self, model_name: str = None):
        """
        Initialize embedding model
        
        Args:
            model_name: Name of embedding model to use
        """
        if model_name is None:
            model_name = settings.EMBEDDING_MODEL
        
        self.model_name = model_name
        self.model = None
        self.dimension = None
        
        self.load_model()
    
    def load_model(self):
        """Load the embedding model"""
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            
            self.model = SentenceTransformer(self.model_name)

            if self.model_name in EMBEDDING_MODELS:
                self.dimension = EMBEDDING_MODELS[self.model_name]["dimension"]
            else:
                self.dimension = 384
            
            logger.info(f"Embedding model loaded. Dimension: {self.dimension}")
        
        except Exception as e:
            logger.error(f"Failed to load embedding model: {str(e)}")
            raise
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for single text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return np.zeros(self.dimension)
        
        try:
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding
        
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def embed_texts(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            batch_size: Batch size for processing
            
        Returns:
            Array of embeddings
        """
        if not texts:
            logger.warning("Empty text list provided for embedding")
            return np.array([])
        
        try:
            logger.info(f"Generating embeddings for {len(texts)} texts")
            
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                convert_to_tensor=False,
                show_progress_bar=True
            )
            
            logger.info(f"Generated {len(embeddings)} embeddings")
            
            return embeddings
        
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self.dimension
    
    def get_model_info(self) -> dict:
        """Get information about the embedding model"""
        if self.model_name in EMBEDDING_MODELS:
            return EMBEDDING_MODELS[self.model_name]
        
        return {
            "name": self.model_name,
            "dimension": self.dimension
        }
 

_embedding_model: Optional[EmbeddingModel] = None
 
 
def get_embedding_model(model_name: str = None) -> EmbeddingModel:
    """Get or create embedding model instance"""
    global _embedding_model
    
    if _embedding_model is None or (model_name and model_name != _embedding_model.model_name):
        _embedding_model = EmbeddingModel(model_name)
    
    return _embedding_model
