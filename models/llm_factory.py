"""
LLM Factory for managing different language models
"""

import time
from typing import Optional, List
import google.genai as genai
from google.genai.errors import APIError
from config.settings import settings
from config.model_config import LLM_MODELS, TASK_MODEL_MAPPING
from key_manager import get_key_manager
from utils.logger import LoggerFactory


logger = LoggerFactory.get_logger("generation")


class LLMFactory:
    """Factory for creating and managing LLM instances"""

    def __init__(self):
        """Initialize LLM factory"""
        self.current_model = None
        self.current_api_key = None
        self.client = None
        self.initialize_api()

    def initialize_api(self):
        """Initialize Gemini API with current key"""
        key_manager = get_key_manager()
        api_key = key_manager.get_current_key()

        # Create fresh client with API key
        self.client = genai.Client(api_key=api_key)
        self.current_api_key = api_key

        logger.info(f"Gemini API initialized with key index {key_manager.current_key_index}")

    def get_model(self, model_name: str = None):
        """
        Get LLM model instance

        Args:
            model_name: Model name (uses default if not provided)

        Returns:
            Model name
        """
        if model_name is None:
            model_name = settings.DEFAULT_LLM_MODEL

        # Check if model exists in config
        if model_name not in LLM_MODELS:
            logger.warning(f"Model {model_name} not in config, using default")
            model_name = settings.DEFAULT_LLM_MODEL

        self.current_model = model_name
        return model_name

    def get_model_for_task(self, task_type: str):
        """
        Get best model for specific task

        Args:
            task_type: Type of task

        Returns:
            Model name
        """
        if task_type not in TASK_MODEL_MAPPING:
            logger.warning(f"Task {task_type} not in mapping, using default")
            return self.get_model()

        preferred_model = TASK_MODEL_MAPPING[task_type]["preferred"]
        return self.get_model(preferred_model)

    def generate_response(
        self,
        prompt: str,
        model_name: str = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> str:
        """
        Generate response using LLM with key rotation fallback and 503 backoff.
        """
        model_name = self.get_model(model_name)
        key_manager = get_key_manager()
        max_attempts = len(key_manager.api_keys)

        for attempt in range(max_attempts):
            try:
                # Ensure client uses active key state
                if self.current_api_key != key_manager.get_current_key():
                    self.initialize_api()

                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        temperature=temperature,
                        top_p=0.95,
                        top_k=40,
                        max_output_tokens=max_tokens,
                    ),
                )

                if response.text:
                    key_manager.mark_key_success()
                    logger.info(
                        f"Response generated successfully using {model_name} (Key Index: {key_manager.current_key_index})"
                    )
                    return response.text
                else:
                    logger.error("Empty response from model")
                    return "Unable to generate response"

            except Exception as e:
                err_msg = str(e)
                logger.warning(
                    f"Attempt {attempt + 1}/{max_attempts} failed (Key Index {key_manager.current_key_index}): {err_msg}"
                )

                if attempt < max_attempts - 1:
                    # Exponential backoff delay specifically for 503 / UNAVAILABLE / Overloaded spikes
                    if any(code in err_msg for code in ["503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED"]):
                        backoff_seconds = (attempt + 1) * 2
                        logger.info(f"Server busy or rate limited. Backing off for {backoff_seconds}s before rotation...")
                        time.sleep(backoff_seconds)

                    self.switch_api_key(reason=f"Error: {err_msg[:100]}")
                else:
                    logger.error("All API keys exhausted.")
                    raise e

    def stream_response(
        self,
        prompt: str,
        model_name: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ):
        """
        Stream response from LLM with key rotation fallback.
        """
        model_name = self.get_model(model_name)
        key_manager = get_key_manager()
        max_attempts = len(key_manager.api_keys)

        for attempt in range(max_attempts):
            has_yielded = False
            try:
                if self.current_api_key != key_manager.get_current_key():
                    self.initialize_api()

                response = self.client.models.generate_content_stream(
                    model=model_name,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        temperature=temperature,
                        top_p=0.95,
                        top_k=40,
                        max_output_tokens=max_tokens,
                    ),
                )

                for chunk in response:
                    if hasattr(chunk, "text") and chunk.text:
                        has_yielded = True
                        yield chunk.text

                if has_yielded:
                    key_manager.mark_key_success()
                    return

            except Exception as e:
                err_msg = str(e)
                logger.warning(
                    f"Streaming attempt {attempt + 1}/{max_attempts} failed on key index {key_manager.current_key_index}: {err_msg}"
                )

                # If we've already yielded chunks to caller, re-attempting will duplicate text
                if has_yielded:
                    logger.error("Stream failed mid-transmission after output was already produced.")
                    raise e

                if attempt < max_attempts - 1:
                    if any(code in err_msg for code in ["503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED"]):
                        backoff_seconds = (attempt + 1) * 2
                        time.sleep(backoff_seconds)

                    self.switch_api_key(reason=f"Streaming error: {err_msg[:100]}")
                else:
                    logger.error("All API keys exhausted during streaming.")
                    raise e

    def switch_api_key(self, reason: str = "API limit"):
        """
        Switch to next API key and recreate Client instance
        """
        key_manager = get_key_manager()
        new_key = key_manager.mark_key_failed(reason)

        # Force a fresh client instance on rotation
        self.client = genai.Client(api_key=new_key)
        self.current_api_key = new_key

        logger.warning(f"API key switched to index {key_manager.current_key_index}. Reason: {reason}")

    def get_model_info(self, model_name: str) -> dict:
        """Get information about a model"""
        if model_name in LLM_MODELS:
            return LLM_MODELS[model_name]
        return {}


# Global LLM factory instance
_llm_factory: Optional[LLMFactory] = None


def get_llm_factory() -> LLMFactory:
    """Get or create LLM factory instance"""
    global _llm_factory

    if _llm_factory is None:
        _llm_factory = LLMFactory()

    return _llm_factory