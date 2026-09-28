"""
PDF Chatbot Application - Main Flask Application
AI/ML Engineer Assessment for AppLab

This application provides a chatbot that can answer questions based on uploaded PDF documents.
Uses RAG (Retrieval Augmented Generation) with embeddings for accurate context-aware responses.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime

# Import custom modules
from services.pdf_processor import PDFProcessor
from services.chatbot import Chatbot
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize services
pdf_processor = PDFProcessor()
chatbot = Chatbot()

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    """Serve the main chatbot interface"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_document():
    """
    API Endpoint: Upload PDF Document
    
    Accepts PDF files, extracts text, and adds to chatbot knowledge base.
    
    Returns:
        JSON response with upload status and document information
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({
                'success': False,
                'error': 'Only PDF files are allowed'
            }), 400
        
        # Secure the filename and save
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(filepath)
        logger.info(f"File saved: {filepath}")
        
        # Extract text from PDF
        extracted_text = pdf_processor.extract_text(filepath)
        
        if not extracted_text:
            return jsonify({
                'success': False,
                'error': 'Could not extract text from PDF'
            }), 400
        
        # Add document to chatbot knowledge base
        doc_id = chatbot.add_document(extracted_text, filename)
        
        logger.info(f"Document processed successfully: {filename}")
        
        return jsonify({
            'success': True,
            'message': 'Document uploaded and processed successfully',
            'document_id': doc_id,
            'filename': filename,
            'text_length': len(extracted_text)
        }), 200
        
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    API Endpoint: Chat with Chatbot
    
    Accepts user questions and returns AI-generated answers based on uploaded documents.
    
    Request JSON:
        {
            "question": "User's question"
        }
    
    Returns:
        JSON response with answer and source information
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'error': 'No question provided'
            }), 400
        
        question = data['question'].strip()
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'Question cannot be empty'
            }), 400
        
        # Check if any documents have been uploaded
        if not chatbot.has_documents():
            return jsonify({
                'success': False,
                'error': 'Please upload a PDF document first'
            }), 400
        
        # Get answer from chatbot
        response = chatbot.get_answer(question)
        
        logger.info(f"Question answered: {question[:50]}...")
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': response['answer'],
            'sources': response.get('sources', []),
            'confidence': response.get('confidence', 'medium')
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/documents', methods=['GET'])
def get_documents():
    """
    API Endpoint: Get list of uploaded documents
    
    Returns:
        JSON list of uploaded documents
    """
    try:
        documents = chatbot.get_document_list()
        
        return jsonify({
            'success': True,
            'documents': documents,
            'count': len(documents)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching documents: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'PDF Chatbot API',
        'timestamp': datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
