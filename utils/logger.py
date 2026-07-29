"""
Logging utilities for RAG System

"""
 
import logging
from config.logging_config import (
    app_logger, api_logger, retrieval_logger,
    embedding_logger, generation_logger, database_logger
)
 
 
class LoggerFactory:
    """Factory for getting module-specific loggers"""
    
    _loggers = {
        "app": app_logger,
        "api": api_logger,
        "retrieval": retrieval_logger,
        "embedding": embedding_logger,
        "generation": generation_logger,
        "database": database_logger
    }
    
    @classmethod
    def get_logger(cls, module_name: str) -> logging.Logger:
        """
        Get logger for specific module
        
        Args:
            module_name: Name of the module
            
        Returns:
            Logger instance
        """
        return cls._loggers.get(module_name, app_logger)
 
 
def log_startup(service_name: str):
    """Log service startup"""
    app_logger.info(f"{service_name} started successfully")
 
 
def log_model_loading(model_name: str, provider: str):
    """Log model loading"""
    app_logger.info(f"Loading model: {model_name} from {provider}")
 
 
def log_embedding_creation(doc_count: int, embedding_model: str):
    """Log embedding creation"""
    embedding_logger.info(
        f"Creating embeddings for {doc_count} documents using {embedding_model}"
    )
 
 
def log_query_processing(query: str, language: str):
    """Log query processing"""
    app_logger.info(f"Processing query in {language}: {query[:100]}...")
 
 
def log_retrieval(query: str, results_count: int, elapsed_time: float):
    """Log retrieval operation"""
    retrieval_logger.info(
        f"Retrieved {results_count} results for query in {elapsed_time:.2f}s"
    )
 
 
def log_api_switch(old_key_index: int, new_key_index: int, reason: str):
    """Log API key switching"""
    api_logger.warning(
        f"Switched from key {old_key_index} to {new_key_index}. Reason: {reason}"
    )
 
 
def log_generation(task_type: str, model_name: str, elapsed_time: float):
    """Log response generation"""
    generation_logger.info(
        f"Generated response for task '{task_type}' using {model_name} "
        f"in {elapsed_time:.2f}s"
    )
 
 
def log_error(module: str, error_message: str, exception: Exception = None):
    """Log error"""
    logger = LoggerFactory.get_logger(module)
    
    if exception:
        logger.error(f"{error_message}: {str(exception)}", exc_info=True)
    else:
        logger.error(error_message)