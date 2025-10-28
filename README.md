# Medical Chatbot API with RAG

A medical question-answering system using Retrieval-Augmented Generation (RAG) that provides accurate, explainable, and citation-backed answers from medical PDF documents.

## Features

- **RAG-powered**: Uses retrieval-augmented generation for accurate medical answers
- **Citation-backed**: Returns source contexts for all answers
- **Fast API**: Built with FastAPI for high performance
- **Medical Documents**: Processes PDF files from anatomy, cardiology, dentistry, emergency medicine, gastroenterology, infectious disease, internal medicine, and nephrology

## Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or use the quick install script:
```bash
chmod +x run.sh
./run.sh
```

### 2. Run Quick Start Check

```bash
python quick_start.py
```

This will verify all dependencies and configurations.

### 3. Environment Configuration (Optional)

Create a `.env` file (optional if using local models):

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

**Note**: The system works with open-source models by default using HuggingFace embeddings and can use OpenAI if an API key is provided.

### 4. First Run (Index Documents)

The system will automatically:
1. Load all PDF documents from the Dataset directory
2. Create embeddings and vector database (takes 5-10 minutes first time)
3. Save everything to `chroma_db/` for faster subsequent runs

## Running the API

### Local Development

```bash
python app.py
```

or

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Deploy to Production

For public deployment, use services like:
- **Render.com**
- **Railway**
- **Heroku**
- **AWS**
- **Google Cloud Run**

## API Endpoints

### POST `/query`

Main query endpoint for medical questions.

**Request:**
```json
{
  "query": "What are the symptoms of heart attack?",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "Heart attack symptoms include chest pain, shortness of breath, nausea, and sweating...",
  "contexts": [
    "Heart attack or myocardial infarction...",
    "Common symptoms include..."
  ]
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### GET `/`

Root endpoint with service information.

**Response:**
```json
{
  "status": "healthy",
  "service": "Medical Chatbot API"
}
```

## API Specification

- **Method**: POST
- **Content-Type**: application/json
- **Timeout**: 60 seconds
- **Request Fields**:
  - `query` (string, required): User question
  - `top_k` (integer, optional, default=5): Number of contexts to return
- **Response Fields**:
  - `answer` (string, required): Generated answer
  - `contexts` (array of strings): Relevant document snippets

## Usage Example

```python
import requests

url = "YOUR_API_URL/query"
payload = {
    "query": "What causes diabetes?",
    "top_k": 3
}

response = requests.post(url, json=payload)
result = response.json()

print("Answer:", result["answer"])
print("Contexts:", result["contexts"])
```

## Project Structure

```
HAC/
├── app.py                      # FastAPI application
├── requirements.txt            # Python dependencies
├── services/
│   ├── __init__.py
│   └── rag_service.py         # RAG implementation
├── chroma_db/                 # Vector database (created on first run)
└── README.md
```

## Dataset

The system processes PDF files from:
- Anatomy & Physiology
- Cardiology
- Dentistry
- Emergency Medicine
- Gastrology
- General Medicine
- Infectious Disease
- Internal Medicine
- Nephrology

## Performance

- First run: ~5-10 minutes (document processing and indexing)
- Subsequent runs: ~10-30 seconds (vector store loading)
- Query response: <10 seconds typically

## Technologies

- **FastAPI**: Web framework
- **LangChain**: RAG pipeline
- **Chroma**: Vector database
- **HuggingFace**: Embeddings and LLMs
- **PyPDF**: PDF document processing

## Troubleshooting

### Issues with OpenAI API

If you don't have an OpenAI API key, the system will automatically use open-source HuggingFace models (GPT-2 as fallback).

### Dataset Not Found

Make sure the dataset path is correct. The system looks for PDF files in:
- `/Users/thrishithreddy/Desktop/Dataset`
- `../Dataset`
- `./Dataset`

Update the path in `services/rag_service.py` if needed.

### Memory Issues

For large datasets, you may need to:
1. Increase available memory
2. Process documents in batches
3. Use smaller embedding models

## License

MIT

