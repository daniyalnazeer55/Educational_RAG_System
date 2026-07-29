"""
Helper functions for RAG System

"""
 
import time
import json
from typing import Any, Callable, Optional
from functools import wraps
from datetime import datetime
from utils.logger import log_error
 
 
def measure_time(func: Callable) -> Callable:
    """
    Decorator to measure function execution time
    
    Args:
        func: Function to measure
        
    Returns:
        Wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        
        return result, elapsed_time
    
    return wrapper
 
 
def retry_on_failure(max_retries: int = 3, delay: int = 1):
    """
    Decorator to retry function on failure
    
    Args:
        max_retries: Maximum number of retries
        delay: Delay between retries in seconds
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        raise
        
        return wrapper
    
    return decorator
 
 
class Timer:
    """Context manager for measuring execution time"""
    
    def __init__(self, name: str = "Operation"):
        """
        Initialize timer
        
        Args:
            name: Operation name for logging
        """
        self.name = name
        self.start_time = None
        self.elapsed_time = None
    
    def __enter__(self):
        """Start timing"""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timing"""
        self.elapsed_time = time.time() - self.start_time
    
    def get_elapsed(self) -> float:
        """Get elapsed time"""
        if self.elapsed_time is None:
            return time.time() - self.start_time if self.start_time else 0
        return self.elapsed_time
 
 
def safe_json_load(json_str: str, default: Any = None) -> Any:
    """
    Safely load JSON string
    
    Args:
        json_str: JSON string
        default: Default value if parsing fails
        
    Returns:
        Parsed JSON or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default
 
 
def safe_json_dump(obj: Any, default: str = "{}") -> str:
    """
    Safely dump object to JSON string
    
    Args:
        obj: Object to dump
        default: Default value if serialization fails
        
    Returns:
        JSON string or default
    """
    try:
        return json.dumps(obj)
    except (TypeError, ValueError):
        return default
 
 
def format_timestamp(dt: datetime = None) -> str:
    """
    Format datetime to string
    
    Args:
        dt: Datetime object, uses now() if not provided
        
    Returns:
        Formatted timestamp
    """
    if dt is None:
        dt = datetime.now()
    
    return dt.strftime("%Y-%m-%d %H:%M:%S")
 
 
def truncate_string(text: str, max_length: int = 100) -> str:
    """
    Truncate string to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."
 
 
def format_response(answer: str, source_book: str, chapter: Optional[int] = None,
                   page_number: Optional[int] = None) -> dict:
    """
    Format response with source information
    
    Args:
        answer: The answer text
        source_book: Source book name
        chapter: Chapter number
        page_number: Page number
        
    Returns:
        Formatted response dictionary
    """
    response = {
        "answer": answer,
        "source_book": source_book,
        "chapter": chapter,
        "page_number": page_number,
        "timestamp": format_timestamp()
    }
    
    return response
 
 
def merge_metadata(metadata_list: list) -> dict:
    """
    Merge multiple metadata dictionaries
    
    Args:
        metadata_list: List of metadata dicts
        
    Returns:
        Merged metadata
    """
    merged = {
        "sources": [],
        "chapters": set(),
        "document_types": set()
    }
    
    for metadata in metadata_list:
        if "source_book" in metadata:
            merged["sources"].append(metadata["source_book"])
        
        if "chapter" in metadata and metadata["chapter"]:
            merged["chapters"].add(metadata["chapter"])
        
        if "document_type" in metadata:
            merged["document_types"].add(metadata["document_type"])
    
    # Convert sets to lists
    merged["chapters"] = sorted(list(merged["chapters"]))
    merged["document_types"] = list(merged["document_types"])
    
    return merged
 
 
def calculate_similarity_score(score: float) -> str:
    """
    Convert similarity score to readable format
    
    Args:
        score: Similarity score (0-1)
        
    Returns:
        Readable similarity description
    """
    if score >= 0.8:
        return "Very High"
    elif score >= 0.6:
        return "High"
    elif score >= 0.4:
        return "Moderate"
    elif score >= 0.2:
        return "Low"
    else:
        return "Very Low"
 
