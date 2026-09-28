"""
PDF Processing Service

Handles extraction of text from PDF documents.
"""

import logging
from typing import Optional
import PyPDF2

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Service for processing PDF documents"""
    
    def __init__(self):
        """Initialize PDF processor"""
        logger.info("PDF Processor initialized")
    
    def extract_text(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as string, or None if extraction fails
        """
        try:
            text = ""
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                logger.info(f"Processing PDF with {num_pages} pages")
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    if page_text:
                        text += page_text + "\n\n"
                
            # Clean up the text
            text = self._clean_text(text)
            
            logger.info(f"Extracted {len(text)} characters from PDF")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove special characters that might cause issues
        text = text.replace('\x00', '')
        
        return text.strip()
