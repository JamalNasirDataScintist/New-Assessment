"""
Chatbot Service with RAG (Retrieval Augmented Generation)

Implements a chatbot that uses embeddings and similarity search to answer questions
based on uploaded PDF documents.
"""

import logging
from typing import Dict, List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import torch
from config import Config

logger = logging.getLogger(__name__)


class Chatbot:
    """AI Chatbot with document-based question answering"""
    
    def __init__(self):
        """Initialize chatbot with embedding model and document store"""
        logger.info("Initializing Chatbot...")
        
        # Load embedding model
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        logger.info(f"Loaded embedding model: {Config.EMBEDDING_MODEL}")
        
        # Document storage
        self.documents = []  # List of document chunks
        self.embeddings = []  # List of embeddings for each chunk
        self.document_metadata = []  # Metadata for each document
        
        # Chunk settings
        self.chunk_size = Config.CHUNK_SIZE
        self.chunk_overlap = Config.CHUNK_OVERLAP
        self.top_k = Config.TOP_K_CHUNKS
        
        logger.info("Chatbot initialized successfully")
    
    def add_document(self, text: str, filename: str) -> str:
        """
        Add a document to the knowledge base
        
        Args:
            text: Extracted text from document
            filename: Name of the document
            
        Returns:
            Document ID
        """
        logger.info(f"Adding document: {filename}")
        
        # Split text into chunks
        chunks = self._chunk_text(text)
        
        # Generate embeddings for chunks
        chunk_embeddings = self.embedding_model.encode(chunks, convert_to_tensor=True)
        
        # Store chunks and embeddings
        doc_id = f"doc_{len(self.document_metadata)}"
        
        for i, (chunk, embedding) in enumerate(zip(chunks, chunk_embeddings)):
            self.documents.append(chunk)
            self.embeddings.append(embedding)
            self.document_metadata.append({
                'doc_id': doc_id,
                'filename': filename,
                'chunk_index': i,
                'total_chunks': len(chunks)
            })
        
        logger.info(f"Added {len(chunks)} chunks from {filename}")
        return doc_id
    
    def get_answer(self, question: str) -> Dict:
        """
        Get an answer to a question based on document content
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer and metadata
        """
        logger.info(f"Processing question: {question}")
        
        if not self.documents:
            return {
                'answer': 'No documents have been uploaded yet. Please upload a PDF document first.',
                'sources': [],
                'confidence': 'low'
            }
        
        # Get relevant context using similarity search
        relevant_chunks = self._retrieve_relevant_chunks(question)
        
        # Generate answer based on retrieved context
        answer = self._generate_answer(question, relevant_chunks)
        
        # Extract source information
        sources = [
            {
                'filename': chunk['metadata']['filename'],
                'chunk': chunk['metadata']['chunk_index'] + 1,
                'snippet': chunk['text'][:100] + '...'
            }
            for chunk in relevant_chunks
        ]
        
        return {
            'answer': answer,
            'sources': sources,
            'confidence': self._calculate_confidence(relevant_chunks)
        }
    
    def _retrieve_relevant_chunks(self, question: str) -> List[Dict]:
        """
        Retrieve most relevant document chunks for a question
        
        Args:
            question: User's question
            
        Returns:
            List of relevant chunks with metadata
        """
        # Generate embedding for the question
        question_embedding = self.embedding_model.encode(question, convert_to_tensor=True)
        
        # Calculate cosine similarity with all document chunks
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = torch.cosine_similarity(
                question_embedding.unsqueeze(0),
                doc_embedding.unsqueeze(0)
            ).item()
            similarities.append((i, similarity))
        
        # Sort by similarity and get top K
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in similarities[:self.top_k]]
        
        # Return relevant chunks
        relevant_chunks = [
            {
                'text': self.documents[idx],
                'metadata': self.document_metadata[idx],
                'similarity': similarities[i][1]
            }
            for i, idx in enumerate(top_indices)
        ]
        
        return relevant_chunks
    
    def _generate_answer(self, question: str, relevant_chunks: List[Dict]) -> str:
        """
        Generate an answer based on relevant context
        
        This is a simple implementation using context extraction.
        For production, you could integrate with OpenAI API or use a local LLM.
        
        Args:
            question: User's question
            relevant_chunks: Retrieved relevant chunks
            
        Returns:
            Generated answer
        """
        if not relevant_chunks:
            return "I couldn't find relevant information in the uploaded documents to answer your question."
        
        # Combine relevant chunks into context
        context = "\n\n".join([chunk['text'] for chunk in relevant_chunks])
        
        # Simple answer generation (extractive)
        # In production, you would use an LLM here
        answer = self._extractive_answer(question, context, relevant_chunks)
        
        return answer
    
    def _extractive_answer(self, question: str, context: str, chunks: List[Dict]) -> str:
        """
        Generate extractive answer from context
        
        This is a simple implementation. For better results, integrate:
        - OpenAI API (GPT-3.5/4)
        - Local LLM (Llama, Mistral)
        - HuggingFace Inference API
        """
        # For now, return the most relevant chunk with context
        if chunks:
            most_relevant = chunks[0]['text']
            
            # Create a formatted response
            answer = f"Based on the uploaded document:\n\n{most_relevant}"
            
            if len(chunks) > 1:
                answer += f"\n\nAdditional relevant information:\n{chunks[1]['text'][:200]}..."
            
            return answer
        
        return "No relevant information found."
    
    def _chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = ' '.join(words[i:i + self.chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    def _calculate_confidence(self, chunks: List[Dict]) -> str:
        """
        Calculate confidence level based on similarity scores
        
        Args:
            chunks: Retrieved chunks with similarity scores
            
        Returns:
            Confidence level: 'high', 'medium', or 'low'
        """
        if not chunks:
            return 'low'
        
        avg_similarity = np.mean([chunk['similarity'] for chunk in chunks])
        
        if avg_similarity > 0.7:
            return 'high'
        elif avg_similarity > 0.5:
            return 'medium'
        else:
            return 'low'
    
    def has_documents(self) -> bool:
        """Check if any documents have been added"""
        return len(self.documents) > 0
    
    def get_document_list(self) -> List[Dict]:
        """Get list of uploaded documents"""
        # Get unique documents
        docs = {}
        for metadata in self.document_metadata:
            doc_id = metadata['doc_id']
            if doc_id not in docs:
                docs[doc_id] = {
                    'id': doc_id,
                    'filename': metadata['filename'],
                    'chunks': metadata['total_chunks']
                }
        
        return list(docs.values())
