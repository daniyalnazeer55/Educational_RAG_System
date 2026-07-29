"""
Logging configuration for RAG System

"""
 
import logging
import logging.handlers
from pathlib import Path
from config.settings import settings
from config.constants import LOG_FORMATS
 
logs_dir = settings.LOGS_DIR
logs_dir.mkdir(parents=True, exist_ok=True)
 
 
def setup_logging(name: str) -> logging.Logger:
    """Setup logging configuration"""
    
    logger = logging.getLogger(name)
    
    log_level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    logger.setLevel(log_level)
    
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(LOG_FORMATS["detailed"])
    simple_formatter = logging.Formatter(LOG_FORMATS["simple"])
    
    file_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "app.log",
        maxBytes=10485760, 
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    error_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "errors.log",
        maxBytes=10485760,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(simple_formatter)

    api_handler = logging.handlers.RotatingFileHandler(
        logs_dir / "api_switching.log",
        maxBytes=5242880, 
        backupCount=3
    )
    api_handler.setLevel(logging.INFO)
    api_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    return logger
 
app_logger = setup_logging("app")
api_logger = setup_logging("api")
retrieval_logger = setup_logging("retrieval")
embedding_logger = setup_logging("embedding")
generation_logger = setup_logging("generation")
database_logger = setup_logging("database")
