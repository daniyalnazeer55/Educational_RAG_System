
"""
Configuration settings for RAG System

"""
 
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
 
load_dotenv()
 
 
class Settings:
    """Main configuration class"""

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "RAG_Class11_Mathematics")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    BOOKS_DIR: Path = DATA_DIR / "books"
    GUIDES_DIR: Path = DATA_DIR / "guides"
    PROCESSED_DIR: Path = DATA_DIR / "processed"
    VECTORDB_DIR: Path = BASE_DIR / os.getenv("VECTOR_DB_PATH", "vectordb")
    CHROMA_DB_PATH: Path = BASE_DIR / os.getenv("CHROMA_DB_PATH", "vectordb/chroma")
    LOGS_DIR: Path = BASE_DIR / "logs"
    PROMPTS_DIR: Path = BASE_DIR / "pipeline" / "prompts" / "templates"

    for directory in [DATA_DIR, BOOKS_DIR, GUIDES_DIR, PROCESSED_DIR, 
                      VECTORDB_DIR, CHROMA_DB_PATH, LOGS_DIR, PROMPTS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

    API_KEYS: list = [
        os.getenv("GEMINI_API_KEY_1", ""),
        os.getenv("GEMINI_API_KEY_2", ""),
        os.getenv("GEMINI_API_KEY_3", ""),
        os.getenv("GEMINI_API_KEY_4", "")
    ]

    # Filter out empty/missing keys from the list
    API_KEYS = [key for key in API_KEYS if key]

    EMBEDDING_API_KEY: Optional[str] = os.getenv("EMBEDDING_API_KEY", None)
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-large-en-v1.5")
    EMBEDDING_DIMENSION: int = 1024 
    
    DEFAULT_LLM_MODEL: str = os.getenv("DEFAULT_LLM_MODEL", "gemini-3.5-flash")
    LLM_TIMEOUT: int = 60
    LLM_MAX_RETRIES: int = len(API_KEYS)


 
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "70"))

    VECTOR_DB_TYPE: str = "chroma" 
    VECTOR_DB_COLLECTION_NAME: str = "class11_mathematics"

    CACHE_EMBEDDINGS: bool = os.getenv("CACHE_EMBEDDINGS", "true").lower() == "true"
    CACHE_RESPONSES: bool = os.getenv("CACHE_RESPONSES", "true").lower() == "true"
    CACHE_DIR: Path = VECTORDB_DIR / "cache"

    TOP_K_RESULTS: int = 3
    SIMILARITY_THRESHOLD: float = 0.3

    SUPPORTED_LANGUAGES: list = ["en", "ur", "ur_roman"] 
    DEFAULT_LANGUAGE: str = "en"

    SESSION_TIMEOUT: int = 3600  

    BATCH_SIZE: int = 32
    NUM_WORKERS: int = 4
 
 
class DevelopmentSettings(Settings):
    """Development environment settings"""
    ENVIRONMENT = "development"
    LOG_LEVEL = "DEBUG"
 
 
class ProductionSettings(Settings):
    """Production environment settings"""
    ENVIRONMENT = "production"
    LOG_LEVEL = "INFO"
 

def get_settings() -> Settings:
    """Get settings based on ENVIRONMENT variable"""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return ProductionSettings()
    return DevelopmentSettings()
 

settings = get_settings()