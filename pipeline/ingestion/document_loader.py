"""
Document Loader for RAG System
Loads and processes educational materials

"""
 
from pathlib import Path
from typing import List, Tuple, Dict
from config.settings import settings
from utils.logger import LoggerFactory
 
 
logger = LoggerFactory.get_logger("app")
 
 
class DocumentLoader:
    """Load and process documents"""
    
    def __init__(self):
        """Initialize document loader"""
        self.books_dir = settings.BOOKS_DIR
        self.guides_dir = settings.GUIDES_DIR
    
    def load_text_file(self, file_path: Path) -> str:
        """
        Load text from file
        
        Args:
            file_path: Path to file
            
        Returns:
            File content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"Loaded file: {file_path.name}")
            return content
        
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {str(e)}")
            raise
    
    def load_books(self) -> List[Tuple[str, str, str]]:
        """
        Load all textbooks
        
        Returns:
            List of (content, filename, book_type)
        """
        books = []

        if self.books_dir.exists():
            for file_path in self.books_dir.glob("*.txt"):
                try:
                    content = self.load_text_file(file_path)
                    books.append((content, file_path.name, "textbook"))
                except Exception as e:
                    logger.warning(f"Skipped file {file_path.name}: {str(e)}")
        
        logger.info(f"Loaded {len(books)} textbooks")
        return books
    
    def load_guides(self) -> List[Tuple[str, str, str]]:
        """
        Load all guide books
        
        Returns:
            List of (content, filename, book_type)
        """
        guides = []

        if self.guides_dir.exists():
            for file_path in self.guides_dir.glob("*.txt"):
                try:
                    content = self.load_text_file(file_path)
                    guides.append((content, file_path.name, "guide"))
                except Exception as e:
                    logger.warning(f"Skipped file {file_path.name}: {str(e)}")
        
        logger.info(f"Loaded {len(guides)} guides")
        return guides
    
    def load_all_documents(self) -> List[Tuple[str, str, str]]:
        """
        Load all documents (books and guides)
        
        Returns:
            List of (content, filename, book_type)
        """
        books = self.load_books()
        guides = self.load_guides()
        
        return books + guides
    
    def get_file_metadata(self, filename: str, book_type: str) -> Dict:
        """
        Extract metadata from filename
        
        Args:
            filename: Filename
            book_type: Type of book (textbook or guide)
            
        Returns:
            Metadata dictionary
        """
        return {
            "subject": "Mathematics",
            "class_level": "11",
            "filename": filename,
            "document_type": book_type
        }
 
