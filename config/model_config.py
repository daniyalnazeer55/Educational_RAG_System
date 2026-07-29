"""
Model Configuration for RAG System

"""

# LLM Model Configurations
LLM_MODELS = {
"gemini-3.5-flash": {
        "provider": "google",
        "name": "gemini-3.5-flash",
        "type": "latest",
        "context_window": 1048576,
        "input_cost_per_1m": 0.10,
        "output_cost_per_1m": 0.40,
        "tasks": ["all", "coding", "reasoning", "agentic_workflows"],
        "speed": "ultra_fast",
        "accuracy": "frontier",
    },
    "gemini-2.0-flash": {
        "provider": "google",
        "name": "gemini-2.0-flash",
        "type": "latest",
        "context_window": 1000000,
        "input_cost_per_1m": 0.10,
        "output_cost_per_1m": 0.40,
        "tasks": ["all"],
        "speed": "very_fast",
        "accuracy": "very_high",
    },
    "gemini-1.5-pro": {
        "provider": "google",
        "name": "gemini-1.5-pro",
        "type": "large",
        "context_window": 1000000,
        "input_cost_per_1m": 1.25,
        "output_cost_per_1m": 5.00,
        "tasks": ["reasoning", "complex_qa", "summarization"],
        "speed": "moderate",
        "accuracy": "high",
    },
    "gemini-1.5-flash": {
        "provider": "google",
        "name": "gemini-1.5-flash",
        "type": "fast",
        "context_window": 1000000,
        "input_cost_per_1m": 0.075,
        "output_cost_per_1m": 0.30,
        "tasks": ["qa", "translation", "fast_response", "metadata_extraction", "query_normalization"],
        "speed": "very_fast",
        "accuracy": "good",
    },
    "deepseek-chat": {
        "provider": "deepseek",
        "name": "deepseek-chat",
        "type": "balanced",
        "context_window": 64000,
        "input_cost_per_1m": 0.14,
        "output_cost_per_1m": 0.28,
        "tasks": ["qa", "reasoning"],
        "speed": "fast",
        "accuracy": "high",
    },
    "deepseek-r1": {
        "provider": "deepseek",
        "name": "deepseek-reasoner",
        "type": "reasoning",
        "context_window": 64000,
        "input_cost_per_1m": 0.55,
        "output_cost_per_1m": 2.19,
        "tasks": ["reasoning", "complex_math", "code_analysis"],
        "speed": "slow",
        "accuracy": "very_high",
    },
    "cohere/aya-expanse-32b": {
        "provider": "openrouter",
        "name": "cohere/aya-expanse-32b",
        "type": "multilingual",
        "context_window": 128000,
        "input_cost_per_1m": 0.50,
        "output_cost_per_1m": 1.50,
        "tasks": ["translation", "multilingual_qa"],
        "speed": "fast",
        "accuracy": "high",
    },
}

# Embedding Model Configurations
EMBEDDING_MODELS = {
    "BAAI/bge-small-en-v1.5": {
        "provider": "huggingface",
        "dimension": 384,
        "model_size": "small",
        "speed": "very_fast",
        "accuracy": "good",
        "use_case": "general_purpose"
    },
    "BAAI/bge-base-en-v1.5": {
        "provider": "huggingface",
        "dimension": 768,
        "model_size": "base",
        "speed": "fast",
        "accuracy": "very_good",
        "use_case": "production"
    },
    "BAAI/bge-large-en-v1.5": {
        "provider": "huggingface",
        "dimension": 1024,
        "model_size": "large",
        "speed": "moderate",
        "accuracy": "excellent",
        "use_case": "high_accuracy"
    }
}

# Task-specific Model Selection
TASK_MODEL_MAPPING = {
    "question_answering": {
        "models": ["gemini-3.5-flash", "gemini-1.5-pro"],
        "preferred": "gemini-3.5-flash",
        "fallback": "gemini-1.5-pro",
        "reason": "Flash for rapid baseline QA, DeepSeek-Chat as a reliable fallback",
    },
    "reasoning": {
        "models": ["gemini-1.5-pro", "deepseek-r1"],
        "preferred": "deepseek-r1",
        "fallback": "gemini-1.5-pro",
        "reason": "DeepSeek R1 for step-by-step Class 11 Math proofs; Gemini Pro as fallback",
    },
    "summarization": {
        "models": ["gemini-1.5-flash", "gemini-1.5-pro"],
        "preferred": "gemini-1.5-flash",
        "fallback": "gemini-1.5-pro",
        "reason": "Fast, high-context window processing for long document chunks",
    },
    "mcq_generation": {
        "models": ["gemini-1.5-flash", "deepseek-chat"],
        "preferred": "gemini-1.5-flash",
        "fallback": "deepseek-chat",
        "reason": "Structured generation of options and questions based strictly on context",
    },
    "translation": {
        "models": ["gemini-1.5-flash", "cohere/aya-expanse-32b"],
        "preferred": "gemini-1.5-flash",
        "fallback": "cohere/aya-expanse-32b",
        "reason": "Flash for broad speed; Aya via OpenRouter for specialized multilingual tasks",
    },
    "query_normalization": {
        "models": ["gemini-1.5-flash"],
        "preferred": "gemini-1.5-flash",
        "fallback": "deepseek-chat",
        "reason": "Ultra-fast latency requirement to avoid bottlenecking RAG search",
    },
    "metadata_extraction": {
        "models": ["gemini-1.5-flash"],
        "preferred": "gemini-1.5-flash",
        "fallback": "deepseek-chat",
        "reason": "Lightweight structural JSON output generation",
    },
    "hallucination_check": {
        "models": ["gemini-1.5-flash", "deepseek-chat"],
        "preferred": "gemini-1.5-flash",
        "fallback": "deepseek-chat",
        "reason": "Fast verification of answer grounding against context",
    },
}

# Prompt Templates Configuration
PROMPT_TEMPLATES = {
    "question_answering": "templates/qa_prompt.txt",
    "summarization": "templates/summarization_prompt.txt",
    "reasoning": "templates/reasoning_prompt.txt",
    "mcq_generation": "templates/mcq_prompt.txt",
    "translation": "templates/translation_prompt.txt",
    "metadata_extraction": "templates/metadata_prompt.txt",
    "hallucination_check": "templates/hallucination_check_prompt.txt"
}

# Retrieval Configuration
RETRIEVAL_CONFIG = {
    "method": "semantic",
    "top_k": 3,
    "similarity_threshold": 0.3,
    "filters": {
        "by_chapter": True,
        "by_book_type": True,
        "by_subject": True
    }
}

# Generation Configuration
GENERATION_CONFIG = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
    "repetition_penalty": 1.0
}

# Cache Configuration
CACHE_CONFIG = {
    "enable_embedding_cache": True,
    "enable_response_cache": True,
    "embedding_cache_ttl": 86400,
    "response_cache_ttl": 3600
}