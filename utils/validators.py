"""
Validators and input checkers for RAG System\

"""
 
from typing import Optional
from config.constants import ERROR_MESSAGES
 
 
class QueryValidator:
    """Validate user queries"""
    
    MIN_QUERY_LENGTH = 3
    MAX_QUERY_LENGTH = 500
    
    @staticmethod
    def validate_query(query: str) -> tuple[bool, Optional[str]]:
        """
        Validate user query
        
        Args:
            query: User query
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not query or not query.strip():
            return False, ERROR_MESSAGES["empty_query"]
        
        if len(query.strip()) < QueryValidator.MIN_QUERY_LENGTH:
            return False, f"Query too short. Minimum {QueryValidator.MIN_QUERY_LENGTH} characters."

        if len(query.strip()) > QueryValidator.MAX_QUERY_LENGTH:
            return False, f"Query too long. Maximum {QueryValidator.MAX_QUERY_LENGTH} characters."
        
        return True, None
    
    @staticmethod
    def validate_language(language: str) -> tuple[bool, Optional[str]]:
        """
        Validate language code
        
        Args:
            language: Language code
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        valid_languages = ["en", "ur", "ur_roman"]
        
        if language not in valid_languages:
            return False, f"Language '{language}' not supported. Use: {valid_languages}"
        
        return True, None
 
 
class ResponseValidator:
    """Validate generated responses"""
    
    MIN_RESPONSE_LENGTH = 10
    MAX_RESPONSE_LENGTH = 10000
    
    @staticmethod
    def validate_response(response: str) -> tuple[bool, Optional[str]]:
        """
        Validate generated response
        
        Args:
            response: Generated response
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not response or not response.strip():
            return False, "Empty response generated"
        
        if len(response.strip()) < ResponseValidator.MIN_RESPONSE_LENGTH:
            return False, "Response too short"
        
        if len(response.strip()) > ResponseValidator.MAX_RESPONSE_LENGTH:
            return False, "Response too long"
        
        return True, None
 
 
class FileValidator:
    """Validate uploaded files"""
    
    ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx"}
    MAX_FILE_SIZE = 100 * 1024 * 1024  
    
    @staticmethod
    def validate_file_extension(filename: str) -> tuple[bool, Optional[str]]:
        """Validate file extension"""
        import os
        ext = os.path.splitext(filename)[1].lower()
        
        if ext not in FileValidator.ALLOWED_EXTENSIONS:
            return False, f"File type '{ext}' not supported. Use: {FileValidator.ALLOWED_EXTENSIONS}"
        
        return True, None
    
    @staticmethod
    def validate_file_size(file_size: int) -> tuple[bool, Optional[str]]:
        """Validate file size"""
        if file_size > FileValidator.MAX_FILE_SIZE:
            return False, f"File too large. Maximum {FileValidator.MAX_FILE_SIZE / 1024 / 1024}MB"
        
        return True, None
 
 
class APIValidator:
    """Validate API responses"""
    
    @staticmethod
    def validate_embedding(embedding: list) -> tuple[bool, Optional[str]]:
        """
        Validate embedding vector
        
        Args:
            embedding: Embedding vector
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not embedding:
            return False, "Empty embedding"
        
        if not all(isinstance(x, (int, float)) for x in embedding):
            return False, "Embedding contains non-numeric values"
        
        return True, None
    
    @staticmethod
    def validate_api_response(response: dict) -> tuple[bool, Optional[str]]:
        """
        Validate API response structure
        
        Args:
            response: API response
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(response, dict):
            return False, "Response is not a dictionary"
        
        return True, None
 
 
class MetadataValidator:
    """Validate document metadata"""
    
    VALID_BOOK_TYPES = ["textbook", "guide"]
    VALID_CHAPTERS = list(range(1, 15)) 
    
    @staticmethod
    def validate_book_type(book_type: str) -> tuple[bool, Optional[str]]:
        """Validate book type"""
        if book_type.lower() not in MetadataValidator.VALID_BOOK_TYPES:
            return False, f"Invalid book type. Use: {MetadataValidator.VALID_BOOK_TYPES}"
        
        return True, None
    
    @staticmethod
    def validate_chapter(chapter: int) -> tuple[bool, Optional[str]]:
        """Validate chapter number"""
        if chapter not in MetadataValidator.VALID_CHAPTERS:
            return False, f"Invalid chapter. Use: {MetadataValidator.VALID_CHAPTERS}"
        
        return True, None
