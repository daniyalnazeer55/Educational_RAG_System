"""
Constants for RAG System

"""
 
DOCUMENT_TYPES = {
    "book": "Textbook",
    "guide": "Guide Book"
}
 
SUBJECT_NAME = "Mathematics"
CLASS_LEVEL = "11"

SUPPORTED_FILE_TYPES = {
    ".txt": "text",
    ".pdf": "pdf",
    ".docx": "docx"
}

RETRIEVAL_MODES = {
    "semantic": "Semantic search using embeddings",
    "hybrid": "Hybrid search (semantic + keyword)",
    "keyword": "Keyword-based search"
}

RESPONSE_TYPES = {
    "answer": "Direct answer",
    "explanation": "Detailed explanation",
    "example": "Example-based response",
    "summary": "Summary response"
}
 
LANGUAGE_CODES = {
    "en": "English",
    "ur": "Urdu",
    "ur_roman": "Roman Urdu"
}
 
URDU_LANGUAGE_INDICATORS = ["ہے", "کیا", "کی", "میں", "سے", "آپ", "یہ", "وہ"]

TASK_TYPES = {
    "question_answering": "QA",
    "summarization": "Summarization",
    "reasoning": "Reasoning",
    "mcq_generation": "MCQ Generation",
    "translation": "Translation",
    "metadata_extraction": "Metadata Extraction"
}

MODEL_SELECTION = {
    "question_answering": {
        "primary": "gemini-3.5-flash",
        "fallback": "deepseek/deepseek-chat",
        "speed": "fast",
    },
    "reasoning": {
        "primary": "gemini-1.5-pro",
        "fallback": "deepseek/deepseek-r1",
        "speed": "moderate",
    },
    "summarization": {
        "primary": "gemini-1.5-flash",
        "fallback": "gemini-1.5-pro",
        "speed": "fast",
    },
    "mcq_generation": {
        "primary": "gemini-1.5-flash",
        "fallback": "deepseek/deepseek-chat",
        "speed": "fast",
    },
    "translation": {
        "primary": "gemini-1.5-flash",
        "fallback": "cohere/aya-expanse-32b", 
        "speed": "fast",
    },
    "query_normalization": {
        "primary": "gemini-1.5-flash",
        "fallback": "gpt-4o-mini",
        "speed": "fast",
    },
    "metadata_extraction": {
        "primary": "gemini-1.5-flash",
        "fallback": "gpt-4o-mini",
        "speed": "fast",
    },
    "hallucination_check": {
        "primary": "gemini-1.5-flash",
        "fallback": "gpt-4o-mini",
        "speed": "fast",
    },
}

ERROR_MESSAGES = {
    "no_api_key": "No API keys available. Please check .env file.",
    "empty_query": "Query cannot be empty. Please provide a valid question.",
    "no_results": "I could not find relevant information in the Class 11 Mathematics textbook or guide.",
    "model_timeout": "The model took too long to respond. Please try again.",
    "invalid_language": "The language is not supported. Supported languages: English, Urdu, Roman Urdu",
    "embedding_failed": "Failed to generate embeddings for the query.",
    "retrieval_failed": "Failed to retrieve information from the database.",
    "database_error": "Vector database error occurred. Please check logs.",
}

SUCCESS_MESSAGES = {
    "initialized": "RAG System initialized successfully",
    "db_loaded": "Vector database loaded successfully",
    "models_loaded": "Models loaded successfully",
    "query_processed": "Query processed successfully"
}
 
LOG_FORMATS = {
    "detailed": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
    "simple": "%(asctime)s - %(levelname)s - %(message)s"
}

CACHE_KEYS = {
    "embedding_": "embedding_",
    "response_": "response_",
    "metadata_": "metadata_"
}
 
CACHE_TTL = {
    "embedding": 86400, 
    "response": 3600,   
    "metadata": 86400    
}
 
HALLUCINATION_CHECK = {
    "max_speculation": 0.15,
    "confidence_threshold": 0.7,
    "source_requirement": True
}

RESPONSE_TEMPLATE = {
    "answer": "",
    "source_book": "",
    "chapter": "",
    "page_number": None,
    "confidence": 0.0,
    "language": "en"
}