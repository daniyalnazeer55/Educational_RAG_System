"""
Text processing utilities for RAG System

"""
 
import re
from typing import List, Tuple
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
 
 
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
 
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
 
 
class TextProcessor:
    """Process and normalize text"""
    
    URDU_CHARS = set("ء ا أ ؤ إ ئ ب ة ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه ي ً ٌ ٍ َ ُ ِ")
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text by removing extra spaces and special characters
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'−', '-', text)
        text = text.strip()
        
        return text
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detect language of text (English, Urdu, or Roman Urdu)
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code: 'en', 'ur', or 'ur_roman'
        """
        urdu_chars = set("ء ا أ ؤ إ ئ ب ة ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه ي ً ٌ ٍ َ ُ ِ")

        urdu_count = sum(1 for char in text if char in urdu_chars)
        urdu_percentage = urdu_count / len(text) if text else 0
        
        if urdu_percentage > 0.3:
            return "ur"

        roman_urdu_patterns = r'\b(kya|hai|hy|hain|jo|woh|yeh|ye|isi|iska|iski)\b'
        if re.search(roman_urdu_patterns, text, re.IGNORECASE):
            return "ur_roman"
        
        return "en"
    
    @staticmethod
    def tokenize_sentences(text: str) -> List[str]:
        """
        Split text into sentences
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of sentences
        """
        try:
            sentences = sent_tokenize(text)
        except Exception:
            sentences = re.split(r'[.!?]+', text)
        
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def tokenize_words(text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of words
        """
        try:
            words = word_tokenize(text)
        except Exception:
            words = text.split()
        
        return [w for w in words if w.isalnum()]
    
    @staticmethod
    def remove_stopwords(words: List[str], language: str = "english") -> List[str]:
        """
        Remove stopwords from word list
        
        Args:
            words: List of words
            language: Language for stopwords
            
        Returns:
            Filtered word list
        """
        try:
            stop_words = set(stopwords.words(language))
            return [w for w in words if w.lower() not in stop_words]
        except Exception:
            return words
    
    @staticmethod
    def normalize_query(query: str) -> str:
        """
        Normalize query text
        
        Args:
            query: Raw query
            
        Returns:
            Normalized query
        """
        query = TextProcessor.clean_text(query)
        query = query.lower()
        query = query.strip('?!.')
        
        return query
    
    @staticmethod
    def extract_keywords(text: str, top_k: int = 10) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text: Text to extract keywords from
            top_k: Number of keywords to extract
            
        Returns:
            List of keywords
        """
        words = TextProcessor.tokenize_words(text)
        words = TextProcessor.remove_stopwords(words)

        word_freq = {}
        for word in words:
            word_freq[word.lower()] = word_freq.get(word.lower(), 0) + 1

        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:top_k]]
 
 
class ChunkProcessor:
    """Process document chunks"""
    
    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 70
    ) -> List[str]:
        """
        Split text into chunks with overlap
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk
            overlap: Overlap between chunks
            
        Returns:
            List of chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        
        return [c.strip() for c in chunks if c.strip()]
    
    @staticmethod
    def extract_metadata(text: str, doc_type: str) -> dict:
        """
        Extract metadata from document text
        
        Args:
            text: Document text
            doc_type: Type of document (book or guide)
            
        Returns:
            Dictionary with metadata
        """
        metadata = {
            "document_type": doc_type,
            "subject": "Mathematics",
            "class_level": "11",
            "chapter": None,
            "page_number": None
        }

        chapter_match = re.search(r'[Cc]hapter\s+(\d+)', text)
        if chapter_match:
            metadata["chapter"] = int(chapter_match.group(1))
        page_match = re.search(r'[Pp]age\s*\d+\s*---\s*(\d+)', text)
        if page_match:
            metadata["page_number"] = int(page_match.group(1))
        
        return metadata