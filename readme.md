# Class 11 Mathematics RAG System

A Retrieval-Augmented Generation (RAG) system for answering questions about Grade 11 Mathematics education content.

## Project Overview

This RAG system combines:
- Vector-based semantic search using embeddings
- Language model responses
- Automatic API key fallback mechanism
- Multi-language query support (English, Urdu, Roman Urdu)
- Maximum hallucination prevention
- Source attribution
- Response from knowledge base

## Features

- Semantic search using BAAI/bge-large-en-v1.5 embeddings
- Advanced LLM responses using Google Gemini
- Automatic API key rotation (4 key fallback)
- ChromaDB vector database for fast retrieval
- Multi-language query support (English, Urdu, Roman Urdu)
- Response grounding to prevent hallucinations
- Source citation with metadata
- FastAPI REST server with Swagger documentation
- Interactive terminal CLI
- Logging and error handling
- Caching for embeddings and responses

## Folder Structure

```
RAG_Project/
├── config/                    # Configuration files
│   ├── settings.py           # Main settings
│   ├── constants.py          # Constants and configurations
│   ├── logging_config.py     # Logging setup
│   └── model_config.py       # Model configurations
├── data/                      # Data directory
│   ├── books/                # Textbook files
│   ├── guides/               # Guide book files
│   └── processed/            # Processed documents
├── embeddings/               # Embedding related code
│   ├── embedding_model.py    # Embedding model handler
│   ├── embedding_generator.py # Embedding generation with cache
│   └── cache/                # Embedding cache
├── vectordb/                 # Vector database
│   ├── chroma_handler.py     # ChromaDB handler
│   ├── chroma/               # ChromaDB data
│   └── metadata/             # Metadata storage
├── models/                   # Model factory and providers
│   ├── llm_factory.py        # LLM factory
│   └── providers/            # LLM provider configs
├── pipeline/                 # Core RAG pipeline
│   ├── ingestion/           # Document ingestion
│   │   ├── document_loader.py
│   │   ├── document_processor.py
│   │   └── ingestion_pipeline.py
│   ├── retrieval/           # Document retrieval
│   │   └── retriever.py
│   ├── generation/          # Response generation
│   │   └── response_generator.py
│   ├── prompts/             # Prompt templates
│   │   ├── qa_prompt.txt
│   │   └── summarization_prompt.txt
│   ├── rag_pipeline.py      # Main orchestrator
│   └── session/             # Session management
├── api/                      # API related code
│   ├── routes.py            # API routes
│   ├── request_models.py    # Request models
│   ├── response_models.py   # Response models
│   └── dependencies.py      # Dependencies
├── utils/                    # Utility functions
│   ├── logger.py            # Logging utilities
│   ├── text_utils.py        # Text processing
│   ├── validators.py        # Input validators
│   └── helpers.py           # Helper functions
├── logs/                     # Log files
├── tests/                    # Test files
├── app.py                    # Terminal CLI application
├── server.py                 # FastAPI server
├── key_manager.py            # API key management
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── .env.example              # Example environment file
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Virtual environment tool

### Step 1: Create Virtual Environment

```bash
# Navigate to project directory
cd RAG_Project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

Required variables in `.env`:
```
GEMINI_API_KEY_1=your_first_api_key
GEMINI_API_KEY_2=your_second_api_key
GEMINI_API_KEY_3=your_third_api_key
GEMINI_API_KEY_4=your_fourth_api_key
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt

# Download spacy model
python -m spacy download en_core_web_sm
```

## API Setup

### Getting Gemini API Keys

1. Visit: https://aistudio.google.com/apikey
2. Create a new API project
3. Generate API keys
4. Add keys to the `.env` file (minimum 5 recommended)

The system will automatically rotate between keys if one hits rate limits.

## Running the Application

### Option 1: Terminal CLI (app.py)

```bash
# Make sure virtual environment is activated
python app.py
```

Commands in CLI:
- `/help` - Show available commands
- `/status` - Display system status
- `/exit` - Exit the application
- Regular text - Your mathematics questions

Example:
```
You: What is a complex number?
Processing your question...
[System retrieves relevant context and generates answer]
```

### Option 2: FastAPI Server (server.py)

```bash
# Start the server
python server.py --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

#### Swagger Documentation
Open your browser to `http://localhost:8000/docs`

#### Available Endpoints

**POST /api/v1/ask** - Ask a single question
```json
{
  "query": "What is a Sequence? Or Solve Example #some_number from Chapter #some_number",
  "language": "en",
  "top_k": 5
}
```

**POST /api/v1/search** - Search without response generation
```json
{
  "query": "trigonometric functions",
  "top_k": 5
}
```

**POST /api/v1/batch-ask** - Ask multiple questions
```json
{
  "requests": [
    {"query": "What is differentiation?"},
    {"query": "Explain integration."}
  ]
}
```

**GET /api/v1/status** - System status

**GET /api/v1/info** - System information

**GET /health** - Health check

## Data Management

### Copy Your Books to Data Directory

```bash
# Copy the textbook
cp OCR_MATH_GENERAL_BOOK.txt data/books/class11_mathematics_textbook.txt

# Copy the guide
cp OCR_MATH_GUIDE_BOOK.txt data/guides/class11_mathematics_guide.txt
```

### Database Initialization

On first run, the system will:
1. Load documents from data/ directory
2. Split into chunks
3. Generate embeddings
4. Index in ChromaDB

This may take several minutes depending on document size.

## Configuration

### Chunk Configuration
Edit `config/settings.py`:
```python
CHUNK_SIZE = 500      # Characters per chunk
CHUNK_OVERLAP = 70    # Overlap between chunks
```

### Retrieval Configuration
```python
TOP_K_RESULTS = 3               # Number of results to retrieve
SIMILARITY_THRESHOLD = 0.3      # Minimum similarity score
```

### Model Selection
Edit `config/model_config.py` to change:
- Default LLM model
- Embedding model
- Model selection strategy for different tasks

## Selected Models

### LLM Models
- **Primary**: Google Gemini 3.5 Flash (fast, efficient)
- **Fallback**: Other Google Gemini Models

### Embedding Model
- **Model**: BAAI/bge-large-en-v1.5
- **Dimension**: 1028


## Prompting Strategy

### Task-Specific Prompts
Each task has a dedicated prompt template:
- Question Answering (`qa_prompt.txt`)
- Summarization (`summarization_prompt.txt`)
- Translation (`translation_prompt.txt`)
- Metadata Extraction (`metadata_prompt.txt`)

## Technologies Used

- **Framework**: FastAPI
- **LLM**: Google Generative AI (Gemini)
- **Embeddings**: Sentence Transformers (BAAI/bge)
- **Vector DB**: ChromaDB
- **Web Server**: Uvicorn
- **Text Processing**: NLTK, spaCy
- **Caching**: Pickle-based file caching
- 
## Logging

Logs are stored in the `logs/` directory:
- `app.log` - General application logs
- `errors.log` - Error logs only
- `api_switching.log` - API key switching events

### Log Levels
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages
- **ERROR**: Error messages

## Troubleshooting

### Issue: "No API keys found"
**Solution**: Ensure the `.env` file exists and contains API keys

### Issue: "Empty database"
**Solution**: 
```bash
# Check data directory
ls data/books/
ls data/guides/

# Verify files are copied to correct location
```

### Issue: Slow responses
**Solution**: 
- Increase `CHUNK_SIZE` in settings
- Reduce `TOP_K_RESULTS`
- Reduce database size

### Issue: Low quality answers
**Solution**:
- Check `CHUNK_SIZE` (too small = context loss)
- Verify API key quotas haven't been exceeded
- Check retrieved context relevance

Database:
- ~2392 documents indexed

## Contributing

This is an educational RAG system for Class 11 Mathematics. 

## Support

For issues or questions:
1. Check the logs in the `logs/` directory
2. Verify configuration in the `config/`
3. Test with terminal CLI (`app.py`)
4. Check FastAPI docs at `/docs`
