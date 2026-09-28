# PDF Chatbot Application

**AI/ML Engineer Assessment for AppLab**

A production-ready Python application that uses AI/ML techniques to create an intelligent chatbot capable of answering questions based on information extracted from PDF documents. Built with Flask, sentence transformers, and modern NLP techniques.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

## 🌟 Features

- **📄 PDF Document Upload**: Upload and process PDF documents through an intuitive web interface
- **🤖 Intelligent Q&A**: Ask questions and get accurate, context-aware answers from your documents
- **🔍 RAG Architecture**: Uses Retrieval Augmented Generation with semantic search
- **🎨 Modern UI**: Clean, responsive web interface with real-time chat
- **🐳 Docker Ready**: Fully containerized for easy deployment
- **📊 Source Attribution**: Shows which document sections were used to generate answers
- **⚡ Fast Performance**: Efficient text chunking and vector similarity search

## 🏗️ Architecture Overview

### System Design

```
┌─────────────────────────────────────────────────────┐
│                   User Interface                     │
│              (HTML/CSS/JavaScript)                   │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│                  Flask API Layer                     │
│  ┌──────────────┐  ┌──────────────┐                │
│  │ Upload API   │  │  Chat API    │                │
│  └──────┬───────┘  └──────┬───────┘                │
└─────────┼──────────────────┼───────────────────────┘
          │                  │
┌─────────▼──────────┐  ┌────▼──────────────────────┐
│  PDF Processor     │  │   Chatbot Service         │
│  - Text Extraction │  │   - Embedding Generation  │
│  - Cleaning        │  │   - Similarity Search     │
└────────────────────┘  │   - Answer Generation     │
                        └───────────────────────────┘
                                    │
                        ┌───────────▼───────────────┐
                        │   Vector Knowledge Base   │
                        │   - Document Chunks       │
                        │   - Embeddings            │
                        │   - Metadata              │
                        └───────────────────────────┘
```

### Technology Stack

- **Backend**: Flask (Python web framework)
- **NLP Models**: Sentence Transformers (all-MiniLM-L6-v2)
- **PDF Processing**: PyPDF2
- **Vector Operations**: PyTorch, NumPy
- **Deployment**: Docker, Gunicorn
- **Frontend**: Vanilla JavaScript, Modern CSS

### NLP & AI Approach

1. **Document Processing**:
   - Extract text from PDFs using PyPDF2
   - Clean and normalize text
   - Split into overlapping chunks (500 words, 50 word overlap)

2. **Embedding Generation**:
   - Use Sentence Transformers (all-MiniLM-L6-v2) for semantic embeddings
   - Create 384-dimensional vectors for each chunk
   - Store embeddings in memory for fast retrieval

3. **Question Answering**:
   - Generate embedding for user question
   - Compute cosine similarity with all document chunks
   - Retrieve top-K most relevant chunks
   - Generate answer based on retrieved context

## 📋 Prerequisites

- Python 3.10 or higher
- Docker (optional, for containerized deployment)
- 4GB RAM minimum
- 2GB disk space

## 🚀 Quick Start

### Option 1: Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd pdf-chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open browser to `http://localhost:5000`

### Option 2: Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t pdf-chatbot .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 -v $(pwd)/uploads:/app/uploads pdf-chatbot
   ```

3. **Access the application**
   - Open browser to `http://localhost:5000`

### Option 3: Docker Compose (Recommended)

1. **Start the application**
   ```bash
   docker-compose up -d
   ```

2. **View logs**
   ```bash
   docker-compose logs -f
   ```

3. **Stop the application**
   ```bash
   docker-compose down
   ```

## 📡 API Documentation

### 1. Upload Document

**Endpoint**: `POST /api/upload`

**Description**: Upload a PDF document to the chatbot's knowledge base

**Request**:
- Method: POST
- Content-Type: multipart/form-data
- Body: 
  - `file`: PDF file (max 16MB)

**Response**:
```json
{
  "success": true,
  "message": "Document uploaded and processed successfully",
  "document_id": "doc_0",
  "filename": "example.pdf",
  "text_length": 15420
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@document.pdf"
```

### 2. Chat/Ask Question

**Endpoint**: `POST /api/chat`

**Description**: Ask a question based on uploaded documents

**Request**:
```json
{
  "question": "What is the main topic of the document?"
}
```

**Response**:
```json
{
  "success": true,
  "question": "What is the main topic of the document?",
  "answer": "Based on the uploaded document: The main topic discusses...",
  "sources": [
    {
      "filename": "example.pdf",
      "chunk": 1,
      "snippet": "The document focuses on..."
    }
  ],
  "confidence": "high"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

### 3. Get Documents

**Endpoint**: `GET /api/documents`

**Description**: Retrieve list of uploaded documents

**Response**:
```json
{
  "success": true,
  "documents": [
    {
      "id": "doc_0",
      "filename": "example.pdf",
      "chunks": 25
    }
  ],
  "count": 1
}
```

### 4. Health Check

**Endpoint**: `GET /api/health`

**Description**: Check if the service is running

**Response**:
```json
{
  "status": "healthy",
  "service": "PDF Chatbot API",
  "timestamp": "2026-02-10T12:00:00"
}
```

## 🔧 Configuration

Edit `.env` file to customize:

```env
# Flask Settings
SECRET_KEY=your-secret-key
DEBUG=False
HOST=0.0.0.0
PORT=5000

# AI Model Settings
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_CHUNKS=3

# File Upload
UPLOAD_FOLDER=uploads
```

## 📁 Project Structure

```
pdf-chatbot/
├── app.py                  # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # This file
│
├── services/            # Core business logic
│   ├── __init__.py
│   ├── pdf_processor.py    # PDF text extraction
│   └── chatbot.py         # RAG chatbot implementation
│
├── templates/           # HTML templates
│   └── index.html       # Main web interface
│
└── uploads/            # Uploaded PDF files (gitignored)
```

## 🧪 Testing the Application

### Manual Testing

1. **Upload a PDF**:
   - Click the upload area
   - Select a PDF file
   - Click "Upload Document"
   - Wait for success message

2. **Ask Questions**:
   - Type a question in the chat input
   - Press Enter or click Send
   - View the AI-generated response

### API Testing

**Test Upload**:
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@sample.pdf"
```

**Test Chat**:
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Summarize the document"}'
```

## 🎯 Use Cases

- **Document Analysis**: Extract insights from research papers, reports
- **Legal Document Q&A**: Query contracts, agreements, legal documents
- **Student Study Aid**: Ask questions about textbooks, study materials
- **Business Intelligence**: Analyze business documents, presentations
- **Knowledge Management**: Create searchable knowledge bases from PDFs

## 🚀 Deployment Guide

### Production Deployment

1. **Set environment variables**:
   ```bash
   export SECRET_KEY=your-production-secret-key
   export DEBUG=False
   ```

2. **Use production WSGI server** (Gunicorn):
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
   ```

3. **Set up reverse proxy** (Nginx):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Cloud Deployment Options

- **AWS**: Deploy on EC2, ECS, or Elastic Beanstalk
- **Google Cloud**: Use App Engine or Cloud Run
- **Azure**: Deploy on App Service or Container Instances
- **Heroku**: One-click deployment with Procfile

## 🔒 Security Considerations

- File size limits enforced (16MB default)
- Only PDF files accepted
- Secure filename handling
- CORS configured
- Environment variables for secrets
- Input validation on all endpoints

## 🐛 Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'torch'"
```bash
Solution: pip install torch==2.1.0
```

**Issue**: "Port 5000 already in use"
```bash
Solution: Change PORT in .env or kill process using port 5000
```

**Issue**: "Error extracting text from PDF"
```bash
Solution: Ensure PDF is not encrypted or corrupted
```

**Issue**: Docker build fails
```bash
Solution: Ensure Docker has enough memory (increase to 4GB+)
```

## 📈 Future Enhancements

- [ ] Support for multiple file formats (DOCX, TXT, HTML)
- [ ] Integration with OpenAI GPT for better answers
- [ ] User authentication and document permissions
- [ ] Persistent vector database (FAISS, Pinecone)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] API rate limiting
- [ ] Conversation history
- [ ] Document summarization
- [ ] Export chat transcripts

## 📝 Development Notes

### Adding New Features

1. Create feature branch
2. Implement changes
3. Test thoroughly
4. Update documentation
5. Submit pull request

### Code Quality

- Follow PEP 8 style guide
- Add docstrings to all functions
- Include type hints
- Write unit tests
- Keep functions focused and small

## 👨‍💻 Developer Information

**Candidate**: [Your Name]  
**Position**: AI/ML Engineer  
**Company**: AppLab  
**Submission Date**: 15/02/2026

## 📧 Contact

For technical inquiries:
- **Email**: Khurram.r@applab.qa
- **Project Issues**: [GitHub Issues](your-repo-url/issues)

## 📄 License

This project was created as an assessment for AppLab.

## 🙏 Acknowledgments

- Sentence Transformers team for the embedding models
- Flask community for the excellent framework
- PyPDF2 contributors for PDF processing capabilities

---

**Note**: This application demonstrates proficiency in:
- Python development
- Flask API design
- NLP and AI/ML techniques
- Docker containerization
- Clean code practices
- Documentation skills
- Full-stack development

Built with ❤️ for AppLab Assessment
