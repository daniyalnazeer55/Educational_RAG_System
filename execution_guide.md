# COMPLETE EXECUTION GUIDE - RAG System for Class 11 Mathematics

This guide provides step-by-step instructions to set up and run the entire RAG system.

---

## PHASE 1: INITIAL SETUP (15 minutes)

### Step 1: Prepare Your Workspace

```bash
# Navigate to a directory where you want the project
cd your_projects_directory

# Create project folder (if not already created)
mkdir RAG_Project
cd RAG_Project
```

### Step 2: Create Virtual Environment

The virtual environment isolates project dependencies from your system Python.

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# You should see (venv) prefix in your terminal
```

**Verify Activation**:
```bash
# Check Python location points to venv
which python  # macOS/Linux
where python  # Windows

# Should show path like /path/to/RAG_Project/venv/bin/python
```

### Step 3: Verify Python Version

```bash
python --version
# Should be Python 3.10 or higher
```

---

## PHASE 2: API KEY SETUP (5 minutes)

### Step 4: Create .env File

**CRITICAL**: This file contains your API keys. Never commit to Git.

Create a file named `.env` in your RAG_Project root:

```
GEMINI_API_KEY_1=paste_your_first_key_here
GEMINI_API_KEY_2=paste_your_second_key_here
GEMINI_API_KEY_3=paste_your_third_key_here
GEMINI_API_KEY_4=paste_your_fourth_key_here
GEMINI_API_KEY_5=paste_your_fifth_key_here
EMBEDDING_API_KEY=optional_if_using_external_embedding_service
PROJECT_NAME=RAG_Class11_Mathematics
ENVIRONMENT=development
LOG_LEVEL=INFO
VECTOR_DB_PATH=./vectordb
CHROMA_DB_PATH=./vectordb/chroma
DEFAULT_LLM_MODEL=gemini-1.5-flash
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
CACHE_EMBEDDINGS=true
CACHE_RESPONSES=true
```

### Step 5: Get Gemini API Keys

Minimum 5 API keys required for automatic fallback:

1. Go to: https://aistudio.google.com/apikey
2. Click "Get API Key"
3. Create new project or select existing
4. Generate API key
5. Copy and paste into `.env` file
6. Repeat 5 times for 5 different keys

**Why 5 keys?**
- Fallback mechanism if one key hits rate limit
- Ensures system keeps running even if one key fails
- Automatic rotation between keys

### Step 6: Create .env.example (for Git)

Create `.env.example` (without actual keys):

```
GEMINI_API_KEY_1=
GEMINI_API_KEY_2=
GEMINI_API_KEY_3=
GEMINI_API_KEY_4=
GEMINI_API_KEY_5=
EMBEDDING_API_KEY=
PROJECT_NAME=RAG_Class11_Mathematics
ENVIRONMENT=development
LOG_LEVEL=INFO
VECTOR_DB_PATH=./vectordb
CHROMA_DB_PATH=./vectordb/chroma
DEFAULT_LLM_MODEL=gemini-1.5-flash
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
CACHE_EMBEDDINGS=true
CACHE_RESPONSES=true
```

---

## PHASE 3: INSTALL DEPENDENCIES (10 minutes)

### Step 7: Install Python Packages

```bash
# Make sure virtual environment is activated (you should see (venv) prefix)

# Install all required packages
pip install -r requirements.txt

# This installs:
# - google-generativeai (Gemini API)
# - chromadb (Vector database)
# - sentence-transformers (Embeddings)
# - fastapi & uvicorn (Web server)
# - and many more (see requirements.txt)
```

**Expected output**:
```
Successfully installed [package names]...
```

### Step 8: Download spaCy Model

```bash
# Download English language model for text processing
python -m spacy download en_core_web_sm

# This downloads language data for tokenization
```

---

## PHASE 4: CREATE FOLDER STRUCTURE (5 minutes)

### Step 9: Create All Required Directories

```bash
# Run from RAG_Project root directory

# Create configuration directory
mkdir -p config

# Create data directories
mkdir -p data/books
mkdir -p data/guides
mkdir -p data/processed

# Create embedding directories
mkdir -p embeddings/cache

# Create vector database directories
mkdir -p vectordb/chroma
mkdir -p vectordb/metadata

# Create model directories
mkdir -p models/providers

# Create pipeline directories
mkdir -p pipeline/prompts
mkdir -p pipeline/ingestion
mkdir -p pipeline/retrieval
mkdir -p pipeline/generation
mkdir -p pipeline/session
mkdir -p pipeline/scripts

# Create API directories
mkdir -p api

# Create utility directories
mkdir -p utils

# Create log directory
mkdir -p logs

# Create test directory
mkdir -p tests

# Create docs directory
mkdir -p docs

# Verify structure
ls -la
```

---

## PHASE 5: COPY PYTHON FILES (10 minutes)

### Step 10: Copy All Python Files to Project

Copy all the `.py` files created into their respective directories:

**Configuration Files** (`config/`):
- settings.py
- constants.py
- logging_config.py
- model_config.py

**Root Level Files**:
- key_manager.py
- app.py
- server.py
- requirements.txt
- README.md
- EXECUTION_GUIDE.md (this file)
- .gitignore
- .env (with your API keys)
- .env.example

**Utilities** (`utils/`):
- logger.py
- text_utils.py
- validators.py
- helpers.py

**Models** (`models/`):
- llm_factory.py

**Embeddings** (`embeddings/`):
- embedding_model.py
- embedding_generator.py

**Vector Database** (`vectordb/`):
- __init__.py
- chroma_handler.py

**Pipeline** (`pipeline/`):
- rag_pipeline.py

**Ingestion Pipeline** (`pipeline/ingestion/`):
- document_loader.py
- document_processor.py
- ingestion_pipeline.py

**Retrieval Pipeline** (`pipeline/retrieval/`):
- retriever.py

**Generation Pipeline** (`pipeline/generation/`):
- response_generator.py

**Prompt Templates** (`pipeline/prompts/`):
- qa_prompt.txt
- summarization_prompt.txt

### Step 11: Copy Data Files

Copy your OCR-extracted math books to the data directory:

```bash
# Copy from wherever your files are located
cp /path/to/OCR_MATH_GENERAL_BOOK.txt data/books/class11_mathematics_textbook.txt
cp /path/to/OCR_MATH_GUIDE_BOOK.txt data/guides/class11_mathematics_guide.txt

# Verify files are copied
ls -la data/books/
ls -la data/guides/
```

**Expected output**:
```
total 1234
-rw-r--r-- 1 user staff 484K Oct 1 12:00 class11_mathematics_textbook.txt
```

---

## PHASE 6: VERIFY INSTALLATION (5 minutes)

### Step 12: Test Python Imports

```bash
# Test if all packages are installed correctly
python -c "import google.generativeai; print('✓ Gemini API')"
python -c "import chromadb; print('✓ ChromaDB')"
python -c "import sentence_transformers; print('✓ Sentence Transformers')"
python -c "import fastapi; print('✓ FastAPI')"
python -c "import nltk; print('✓ NLTK')"

# Test if your .env file is readable
python -c "from config.settings import settings; print('✓ Settings loaded')"
```

**Expected output**:
```
✓ Gemini API
✓ ChromaDB
✓ Sentence Transformers
✓ FastAPI
✓ NLTK
✓ Settings loaded
```

### Step 13: Verify Folder Structure

```bash
# Check that all required directories exist
find . -type d -name "__pycache__" -prune -o -type d -print | sort

# Should show all your directories
```

---

## PHASE 7: INITIAL DATA INGESTION (30-60 minutes)

### Step 14: Run Ingestion Pipeline (First Time Only)

The ingestion pipeline will:
1. Load your Math books and guide
2. Split into chunks (1000 chars each)
3. Generate embeddings
4. Index in ChromaDB

```bash
# From RAG_Project root, with (venv) activated

# Option 1: Run via Python directly
python -c "from pipeline.ingestion.ingestion_pipeline import run_ingestion_pipeline; indexed = run_ingestion_pipeline(); print(f'Indexed {indexed} chunks')"

# Option 2: Will auto-run on first app.py execution (see next step)
```

**What happens during ingestion**:
```
Step 1: Loading documents from disk
Loaded 2 documents (textbook + guide)

Step 2: Processing documents into chunks
Created 1247 chunks

Step 3: Indexing chunks into vector database
Generating embeddings for 1247 documents
[████████████████████████] 100% complete
Successfully added 1247 documents

Database persisted to disk
```

**Expected time**: 20-60 minutes depending on:
- Document size (2 files ~ 600KB)
- Internet speed (downloading embeddings)
- Computer performance

---

## PHASE 8: RUN THE APPLICATION

### Step 15: Run Terminal CLI (Option 1)

**Best for testing and interactive use**:

```bash
# From RAG_Project root with (venv) activated
python app.py

# Expected output:
# ============================================================
#   CLASS 11 MATHEMATICS - RAG SYSTEM
#   Interactive Question Answering
# ============================================================
#
# Initializing RAG system...
# ✓ RAG system initialized successfully
#
# Available Commands:
#   /help      - Show help message
#   /status    - Show system status
#   /exit      - Exit application
#   /clear     - Clear screen
#
# You: _
```

**Try asking questions**:
```
You: What is a complex number?

Processing your question...

============================================================
RESPONSE
============================================================

A complex number is a number of the form z = a + ib, where a and b are 
real numbers and i is the imaginary unit defined as √(-1). In this notation,
'a' is called the real part and 'b' is called the imaginary part...

============================================================
SOURCES
============================================================

[Source 1]
Type: Textbook
File: class11_mathematics_textbook.txt
Chapter: 1
Confidence: 95.23%

============================================================
METADATA
============================================================

Confidence Score: 95.23%
Processing Time: 2.34s
```

**Exit the app**:
```
You: /exit

Thank you for using the RAG system. Goodbye!
```

### Step 16: Run FastAPI Server (Option 2)

**Best for production and API integration**:

```bash
# From RAG_Project root with (venv) activated
python server.py

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Press CTRL+C to quit
```

**Open API Documentation** (in your web browser):

1. Swagger UI: http://localhost:8000/docs
2. ReDoc: http://localhost:8000/redoc

**Try the API**:

Open `http://localhost:8000/docs`, find the `/api/v1/ask` endpoint:

```json
{
  "query": "What is the Pythagorean theorem?",
  "language": "en",
  "top_k": 5
}
```

Click "Try it out" → "Execute"

**Response Example**:
```json
{
  "query": "What is the Pythagorean theorem?",
  "answer": "The Pythagorean theorem states that in a right-angled triangle...",
  "sources": [
    {
      "document_type": "textbook",
      "filename": "class11_mathematics_textbook.txt",
      "chapter": 10,
      "confidence": 0.94
    }
  ],
  "confidence_score": 0.94,
  "response_type": "grounded_answer",
  "processing_time": 2.15
}
```

---

## PHASE 9: TESTING & VALIDATION (20 minutes)

### Step 17: Test Different Query Types

**Test 1: Simple Question**
```
Query: "Define differentiation"
Expected: Quick answer with source attribution
```

**Test 2: Complex Query**
```
Query: "Explain the relationship between trigonometric identities and unit circle"
Expected: Comprehensive answer with multiple sources
```

**Test 3: Multi-language (if using GUI)**
```
Query: "Newton ka pehla qanoon kya hai?" (Roman Urdu)
Expected: Answer in the same language
```

**Test 4: Out-of-scope Query**
```
Query: "Tell me about quantum physics"
Expected: "I couldn't find relevant information in Class 11 Mathematics materials"
```

### Step 18: Check System Logs

```bash
# View application logs
tail -f logs/app.log

# View errors only
tail -f logs/errors.log

# View API key switching logs
tail -f logs/api_switching.log

# Check full log structure
ls -lh logs/
```

---

## PHASE 10: PRODUCTION DEPLOYMENT (Optional)

### Step 19: Run with Gunicorn (Production)

For production deployment, use Gunicorn instead of Uvicorn:

```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -b 0.0.0.0:8000 server:app
```

### Step 20: Enable HTTPS (Production)

```bash
# Generate SSL certificates (self-signed, for testing only)
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with SSL
gunicorn -w 4 -b 0.0.0.0:8443 --certfile=cert.pem --keyfile=key.pem server:app
```

---

## COMMON COMMANDS REFERENCE

### Development Workflow

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run terminal CLI
python app.py

# Run API server
python server.py

# Run with custom host/port
python server.py --host 0.0.0.0 --port 8000

# Run with auto-reload (development)
python server.py --reload

# Deactivate virtual environment
deactivate
```

### Database Management

```bash
# Check indexed documents
python -c "from vectordb.chroma_handler import get_chroma_handler; print(get_chroma_handler().get_document_count())"

# Clear all documents (fresh start)
python -c "from vectordb.chroma_handler import get_chroma_handler; get_chroma_handler().clear_collection()"
```

### Debugging

```bash
# Check if all modules load
python -m py_compile config/*.py models/*.py pipeline/**/*.py

# Run with debug logging
PYTHONDEBUG=1 python app.py

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

---

## TROUBLESHOOTING

### Problem: "ModuleNotFoundError"

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall requirements
pip install --upgrade -r requirements.txt

# Verify imports
python -c "import config.settings"
```

### Problem: "No API keys found"

**Solution**:
```bash
# Check .env file exists
ls -la .env

# Verify API keys are set
python -c "from config.settings import settings; print(settings.GEMINI_API_KEYS)"

# Should show list of non-empty keys
```

### Problem: "Database is empty"

**Solution**:
```bash
# Verify data files exist
ls -la data/books/
ls -la data/guides/

# Re-run ingestion
python -c "from pipeline.ingestion.ingestion_pipeline import run_ingestion_pipeline; run_ingestion_pipeline()"

# Check result
python -c "from vectordb.chroma_handler import get_chroma_handler; print(f'Documents: {get_chroma_handler().get_document_count()}')"
```

### Problem: "Slow responses"

**Solutions**:
```python
# In config/settings.py, increase chunk size:
CHUNK_SIZE = 1500  # Instead of 1000

# Reduce retrieval results:
TOP_K_RESULTS = 3  # Instead of 5

# Disable caching (if cache is corrupted):
CACHE_EMBEDDINGS = False
```

---

## PERFORMANCE OPTIMIZATION

### Speed up Embeddings

```python
# In config/settings.py
BATCH_SIZE = 64  # Increase from 32
NUM_WORKERS = 4  # Increase from 2
```

### Speed up API Responses

```python
# In config/settings.py
CHUNK_SIZE = 2000  # Larger chunks = fewer queries
TOP_K_RESULTS = 3  # Fewer results = faster processing
```

---

## MONITORING IN PRODUCTION

### Check System Health

```bash
# Terminal 1: Run server
python server.py

# Terminal 2 (in new terminal, activate venv first):
# Check API is running
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","message":"RAG system is running"}
```

### Monitor Logs in Real-time

```bash
# Watch all logs
tail -f logs/app.log

# Watch errors
tail -f logs/errors.log | grep ERROR

# Count API switches (indicates quota issues)
grep "API Key switched" logs/api_switching.log | wc -l
```

---

## NEXT STEPS

1. **Test thoroughly**: Ask various questions to test system
2. **Monitor logs**: Check for errors or warnings
3. **Optimize settings**: Adjust CHUNK_SIZE, TOP_K based on your needs
4. **Deploy**: Use FastAPI with production web server
5. **Integrate**: Connect to your application via API

---

## QUICK START CHECKLIST

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] .env file created with 5 API keys
- [ ] requirements.txt installed
- [ ] spaCy model downloaded
- [ ] Folder structure created
- [ ] All Python files copied
- [ ] Math books copied to data/ folder
- [ ] Imports verified (Step 12)
- [ ] First ingestion run completed
- [ ] Terminal CLI tested (app.py)
- [ ] API server tested (server.py)
- [ ] Sample queries answered successfully

---

## ADDITIONAL RESOURCES

- **Gemini API Docs**: https://ai.google.dev/docs
- **ChromaDB Docs**: https://docs.trychroma.com
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Sentence Transformers**: https://www.sbert.net

---

**Congratulations!** You now have a fully functional RAG system for Class 11 Mathematics!