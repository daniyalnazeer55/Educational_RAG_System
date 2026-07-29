"""
Response Generator
Generates responses using LLM based on retrieved context
"""

from typing import Optional, List, Dict, Tuple
from pathlib import Path
from models.llm_factory import get_llm_factory
from config.settings import settings
from utils.logger import LoggerFactory
from utils.text_utils import TextProcessor


logger = LoggerFactory.get_logger("generation")


class ResponseGenerator:
    """Generate responses using LLM"""
    
    def __init__(self):
        """Initialize response generator"""
        self.llm_factory = get_llm_factory()
        self.prompts_dir = settings.PROMPTS_DIR
        self.model_name = settings.DEFAULT_LLM_MODEL
    
    def load_prompt_template(self, template_name: str) -> str:
        """
        Load prompt template from file
        
        Args:
            template_name: Name of the template file
            
        Returns:
            Prompt template content
        """
        template_path = self.prompts_dir / f"{template_name}.txt"
        
        if not template_path.exists():
            logger.warning(f"Prompt template not found: {template_name}")
            return "Answer the following based on the context:\n\nContext: {context}\n\nQuestion: {query}"
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        except Exception as e:
            logger.error(f"Error loading prompt template: {str(e)}")
            return "Answer the following based on the context:\n\nContext: {context}\n\nQuestion: {query}"
    
    def generate_qa_response(
        self,
        query: str,
        context: str,
        model_name: str = None
    ) -> str:
        """
        Generate question answering response
        
        Args:
            query: User question
            context: Retrieved context
            model_name: Model to use
            
        Returns:
            Generated response
        """
        logger.info("Generating QA response")
        
        # Load prompt template
        template = self.load_prompt_template("qa_prompt")
        
        # Format prompt
        prompt = template.format(context=context, query=query)
        
        try:
            # Generate response
            response = self.llm_factory.generate_response(
                prompt=prompt,
                model_name=model_name,
                temperature=0.3,
                max_tokens=2048
            )
            
            return response
        
        except Exception as e:
            logger.error(f"Error generating QA response: {str(e)}")
            raise
    
    def generate_summary(
        self,
        text: str,
        model_name: str = None
    ) -> str:
        """
        Generate summary of text
        
        Args:
            text: Text to summarize
            model_name: Model to use
            
        Returns:
            Generated summary
        """
        logger.info("Generating summary")
        
        # Load prompt template
        template = self.load_prompt_template("summarization_prompt")
        
        # Format prompt
        prompt = template.format(context=text)
        
        try:
            # Generate response
            response = self.llm_factory.generate_response(
                prompt=prompt,
                model_name=model_name,
                temperature=0.3,
                max_tokens=512
            )
            
            return response
        
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise
    
    def validate_hallucination(
        self,
        question: str,
        context: str,
        response: str
    ) -> Tuple[bool, float]:
        """
        Check if response is grounded in context
        
        Args:
            question: Original question
            context: Retrieved context
            response: Generated response
            
        Returns:
            Tuple of (is_grounded, confidence_score)
        """
        logger.info("Validating response for hallucination")
        
        hallucination_prompt = f"""
        Evaluate if the following response is grounded in the provided context.
        
        Context:
        {context}
        
        Question:
        {question}
        
        Response:
        {response}
        
        Answer with:
        1. Is the response grounded in context? (YES/NO)
        2. Confidence score (0-1)
        
        Format: GROUNDED: [YES/NO], SCORE: [0.0-1.0]
        """
        
        try:
            validation_response = self.llm_factory.generate_response(
                prompt=hallucination_prompt,
                temperature=0.3,
                max_tokens=50
            )
            
            # Parse response
            if "YES" in validation_response.upper():
                grounded = True
            else:
                grounded = False
            
            # Extract score
            try:
                score_str = validation_response.split("SCORE:")[-1].strip()
                confidence = float(score_str.rstrip(')'))
            except:
                confidence = 0.5 if grounded else 0.3
            
            return grounded, confidence
        
        except Exception as e:
            logger.error(f"Error validating hallucination: {str(e)}")
            return False, 0.5
    
    def format_final_response(
        self,
        answer: str,
        sources: List[Dict],
        query: str,
        confidence: float = 1.0
    ) -> Dict:
        """
        Format final response with metadata
        
        Args:
            answer: Generated answer
            sources: Source information
            query: Original query
            confidence: Confidence score
            
        Returns:
            Formatted response dictionary
        """
        response = {
            "query": query,
            "answer": answer,
            "sources": sources,
            "confidence_score": confidence,
            "response_type": "grounded_answer"
        }
        
        return response


def get_response_generator() -> ResponseGenerator:
    """Get response generator instance"""
    return ResponseGenerator()