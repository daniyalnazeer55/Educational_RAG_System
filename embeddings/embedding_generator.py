"""
Embedding Generator
Processes documents and generates embeddings with caching

"""
 
import os
import pickle
import hashlib
from pathlib import Path
from typing import List, Tuple, Optional
import numpy as np
from embeddings.embedding_model import get_embedding_model
from config.settings import settings
from utils.logger import LoggerFactory
 
 
logger = LoggerFactory.get_logger("embedding")
 
 
class EmbeddingGenerator:
    """Generate and cache embeddings"""
    
    def __init__(self):
        """Initialize embedding generator"""
        self.embedding_model = get_embedding_model()
        self.cache_dir = settings.CACHE_DIR / "embeddings"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_enabled = settings.CACHE_EMBEDDINGS
    
    def get_cache_path(self, text: str) -> Path:
        """
        Get cache file path for text
        
        Args:
            text: Text to generate cache path for
            
        Returns:
            Cache file path
        """
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return self.cache_dir / f"{text_hash}.pkl"
    
    def get_cached_embedding(self, text: str) -> Optional[np.ndarray]:
        """
        Get embedding from cache if available
        
        Args:
            text: Text to get cached embedding for
            
        Returns:
            Cached embedding or None
        """
        if not self.cache_enabled:
            return None
        cache_path = self.get_cache_path(text)
        
        if cache_path.exists():
            try:
                with open(cache_path, 'rb') as f:
                    embedding = pickle.load(f)
                logger.debug(f"Retrieved embedding from cache: {cache_path}")
                return embedding
            
            except Exception as e:
                logger.warning(f"Error loading cached embedding: {str(e)}")
                return None
        
        return None
    
    def cache_embedding(self, text: str, embedding: np.ndarray):
        """
        Cache embedding for text
        
        Args:
            text: Text the embedding represents
            embedding: Embedding to cache
        """
        if not self.cache_enabled:
            return
        cache_path = self.get_cache_path(text)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(embedding, f)
            logger.debug(f"Cached embedding: {cache_path}")
        
        except Exception as e:
            logger.warning(f"Error caching embedding: {str(e)}")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for text with caching
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        cached = self.get_cached_embedding(text)
        if cached is not None:
            return cached

        embedding = self.embedding_model.embed_text(text)
        self.cache_embedding(text, embedding)
        
        return embedding
    
    def generate_embeddings(
        self,
        texts: List[str],
        batch_size: int = 32,
        use_cache: bool = True
    ) -> Tuple[List[np.ndarray], List[int]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            batch_size: Batch size for processing
            use_cache: Whether to use cache
            
        Returns:
            Tuple of (embeddings, uncached_indices)
        """
        embeddings = []
        uncached_texts = []
        uncached_indices = []

        for idx, text in enumerate(texts):
            if use_cache:
                cached = self.get_cached_embedding(text)
                if cached is not None:
                    embeddings.append(cached)
                else:
                    uncached_texts.append(text)
                    uncached_indices.append(idx)
            else:
                uncached_texts.append(text)
                uncached_indices.append(idx)

        if uncached_texts:
            logger.info(f"Generating embeddings for {len(uncached_texts)} texts")
            
            new_embeddings = self.embedding_model.embed_texts(
                uncached_texts,
                batch_size=batch_size
            )

            if use_cache:
                for text, embedding in zip(uncached_texts, new_embeddings):
                    self.cache_embedding(text, embedding)
        else:
            new_embeddings = []

        result_embeddings = []
        new_idx = 0
        cached_idx = 0
        
        for idx in range(len(texts)):
            if idx in uncached_indices:
                result_embeddings.append(new_embeddings[new_idx])
                new_idx += 1
            else:
                result_embeddings.append(embeddings[cached_idx])
                cached_idx += 1
        
        logger.info(f"Successfully generated embeddings for {len(texts)} texts")
        
        return result_embeddings, uncached_indices
    
    def clear_cache(self):
        """Clear embedding cache"""
        try:
            import shutil
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Embedding cache cleared")
        
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
    
    def get_cache_size(self) -> int:
        """Get total size of cache in bytes"""
        total_size = 0
        
        for file_path in self.cache_dir.glob("*.pkl"):
            total_size += file_path.stat().st_size
        
        return total_size
 

_embedding_generator: Optional[EmbeddingGenerator] = None
 
 
def get_embedding_generator() -> EmbeddingGenerator:
    """Get or create embedding generator instance"""
    global _embedding_generator
    
    if _embedding_generator is None:
        _embedding_generator = EmbeddingGenerator()
    
    return _embedding_generator
