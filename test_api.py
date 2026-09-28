#!/usr/bin/env python3
"""
Test Script for PDF Chatbot Application
Tests all API endpoints and functionality
"""

import requests
import json
import sys
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:5000"
TEST_PDF = "test_document.pdf"  # Place a test PDF in the same directory

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def test_health_check():
    """Test health check endpoint"""
    print_info("Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check passed: {data['status']}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False

def test_upload_document():
    """Test document upload endpoint"""
    print_info("Testing document upload...")
    
    # Check if test PDF exists
    if not Path(TEST_PDF).exists():
        print_warning(f"Test PDF '{TEST_PDF}' not found. Creating a dummy file...")
        # Create a simple test PDF (this is just a placeholder)
        print_error("Please provide a real PDF file named 'test_document.pdf'")
        return False
    
    try:
        with open(TEST_PDF, 'rb') as f:
            files = {'file': (TEST_PDF, f, 'application/pdf')}
            response = requests.post(f"{BASE_URL}/api/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print_success(f"Document uploaded: {data['filename']}")
                print_info(f"Document ID: {data['document_id']}")
                print_info(f"Text length: {data['text_length']} characters")
                return True
            else:
                print_error(f"Upload failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print_error(f"Upload failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Upload error: {str(e)}")
        return False

def test_get_documents():
    """Test get documents endpoint"""
    print_info("Testing get documents endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/documents")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print_success(f"Retrieved {data['count']} document(s)")
                for doc in data['documents']:
                    print_info(f"  - {doc['filename']} ({doc['chunks']} chunks)")
                return True
            else:
                print_error("Failed to get documents")
                return False
        else:
            print_error(f"Get documents failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Get documents error: {str(e)}")
        return False

def test_chat(question):
    """Test chat endpoint"""
    print_info(f"Testing chat with question: '{question}'")
    try:
        payload = {"question": question}
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print_success("Chat response received")
                print_info(f"Answer: {data['answer'][:100]}...")
                print_info(f"Confidence: {data['confidence']}")
                if data['sources']:
                    print_info(f"Sources: {len(data['sources'])} document section(s)")
                return True
            else:
                print_error(f"Chat failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print_error(f"Chat failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Chat error: {str(e)}")
        return False

def test_invalid_upload():
    """Test upload with invalid file"""
    print_info("Testing upload with invalid file type...")
    try:
        # Create a dummy text file
        dummy_content = b"This is not a PDF"
        files = {'file': ('test.txt', dummy_content, 'text/plain')}
        response = requests.post(f"{BASE_URL}/api/upload", files=files)
        
        if response.status_code == 400:
            print_success("Correctly rejected non-PDF file")
            return True
        else:
            print_warning(f"Expected 400 status, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Invalid upload test error: {str(e)}")
        return False

def test_chat_without_document():
    """Test chat without uploading document first"""
    print_info("Testing chat without document...")
    # This test only works if you start fresh without documents
    # Skip it if documents are already uploaded
    print_warning("Skipping - assumes documents are already uploaded")
    return True

def main():
    """Run all tests"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"PDF Chatbot Application - Test Suite")
    print(f"{'='*60}{Colors.END}\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Document Upload", test_upload_document),
        ("Get Documents", test_get_documents),
        ("Chat - General Question", lambda: test_chat("What is this document about?")),
        ("Chat - Specific Question", lambda: test_chat("Summarize the main points")),
        ("Invalid Upload", test_invalid_upload),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{Colors.YELLOW}[{test_name}]{Colors.END}")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # Print summary
    print(f"\n{Colors.BLUE}{'='*60}")
    print("Test Summary")
    print(f"{'='*60}{Colors.END}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status:8}{Colors.END} - {test_name}")
    
    print(f"\n{Colors.BLUE}Total: {passed}/{total} tests passed{Colors.END}\n")
    
    if passed == total:
        print_success("All tests passed! ✨")
        return 0
    else:
        print_error(f"{total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
