"""
Document Processor
Chunks and prepares documents for indexing
"""

import re
from typing import List, Dict, Tuple
from config.settings import settings
from utils.text_utils import TextProcessor, ChunkProcessor
from utils.logger import LoggerFactory


logger = LoggerFactory.get_logger("app")


class DocumentProcessor:
    """Process documents for indexing"""
    
    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None
    ):
        """
        Initialize document processor
        
        Args:
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
    
    def process_document(
        self,
        content: str,
        filename: str,
        document_type: str
    ) -> List[Tuple[str, Dict]]:
        """
        Process a single document
        
        Args:
            content: Document content
            filename: Original filename
            document_type: Type of document (textbook or guide)
            
        Returns:
            List of (chunk, metadata) tuples
        """
        # Clean content
        content = TextProcessor.clean_text(content)
        
        # Extract chapter information with positions
        chapters = self._extract_chapters(content)
        
        # Create chunks with position tracking
        chunks = []
        chunk_positions = []  # Track position of each chunk
        
        start = 0
        chunk_idx = 0
        
        while start < len(content):
            end = start + self.chunk_size
            chunk = content[start:end].strip()
            
            if chunk:
                chunks.append(chunk)
                chunk_positions.append(start) 
            
            chunk_idx += 1
            start = end - self.chunk_overlap
        
        # Create metadata for each chunk
        result = []
        for chunk_idx, (chunk, chunk_start_pos) in enumerate(zip(chunks, chunk_positions)):
            # Find which chapter this chunk belongs to based on position
            chapter = self._find_chunk_chapter_by_position(chunk_start_pos, chapters)
            
            metadata = {
                "subject": "Mathematics",
                "class_level": "11",
                "filename": filename,
                "document_type": document_type,
                "chapter": chapter,
                "chunk_index": chunk_idx,
                "total_chunks": len(chunks)
            }
            
            result.append((chunk, metadata))
        
        logger.info(f"Processed '{filename}': {len(chunks)} chunks created")
        
        return result
    
    def _extract_chapters(self, content: str) -> Dict[int, int]:
        """
        Extract chapter positions from content
        
        Args:
            content: Document content
            
        Returns:
            Dictionary of chapter number to position
        """
        chapters = {}
        
        # Pattern to find chapters
        pattern = r'(?:CHAPTER|Unit|Ch\.)\s+(\d+)'
        
        for match in re.finditer(pattern, content, re.IGNORECASE):
            chapter_num = int(match.group(1))
            position = match.start()
            chapters[chapter_num] = position
        
        return chapters
    
    def _find_chunk_chapter_by_position(self, chunk_position: int, chapters: Dict[int, int]) -> int:
        """
        Find which chapter a chunk belongs to based on its position
        
        Args:
            chunk_position: Starting position of chunk in document
            chapters: Dictionary of chapter_number -> position
            
        Returns:
            Chapter number
        """
        if not chapters:
            return 1
        
        # Find the chapter that starts before or at this position
        applicable_chapters = {ch: pos for ch, pos in chapters.items() if pos <= chunk_position}
        
        if not applicable_chapters:
            return 1
        
        # Return the chapter with highest position that's still before chunk
        return max(applicable_chapters.items(), key=lambda x: x[1])[0]
    
    def process_batch(
        self,
        documents: List[Tuple[str, str, str]]
    ) -> List[Tuple[str, Dict]]:
        """
        Process multiple documents
        
        Args:
            documents: List of (content, filename, document_type) tuples
            
        Returns:
            List of (chunk, metadata) tuples
        """
        all_chunks = []
        
        logger.info(f"Processing {len(documents)} documents")
        
        for content, filename, document_type in documents:
            chunks = self.process_document(content, filename, document_type)
            all_chunks.extend(chunks)
        
        logger.info(f"Total chunks created: {len(all_chunks)}")
        
        return all_chunks
    
    def estimate_chunk_count(self, documents: List[Tuple[str, str, str]]) -> int:
        """
        Estimate total number of chunks
        
        Args:
            documents: List of documents
            
        Returns:
            Estimated chunk count
        """
        total_content_length = sum(len(content) for content, _, _ in documents)
        
        if self.chunk_size == 0:
            return 0
        
        # Rough estimate (doesn't account for overlap reduction)
        estimated_chunks = total_content_length // self.chunk_size
        
        return max(1, estimated_chunks)