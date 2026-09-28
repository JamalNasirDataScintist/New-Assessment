"""
Configuration Settings for PDF Chatbot Application
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # AI Model settings
    # You can use HuggingFace models or OpenAI API
    MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'huggingface')  # 'huggingface' or 'openai'
    
    # OpenAI settings (if using OpenAI)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # HuggingFace settings
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
    
    # Embeddings model (sentence-transformers)
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
    
    # Vector database settings
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', 'vector_db')
    
    # Chunk settings for text processing
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 500))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 50))
    
    # Number of relevant chunks to retrieve for context
    TOP_K_CHUNKS = int(os.getenv('TOP_K_CHUNKS', 3))
