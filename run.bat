@echo off
echo ================================
echo   PDF Chatbot - Starting App
echo ================================

echo Step 1: Creating virtual environment...
python -m venv venv

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo Step 4: Installing dependencies...
pip install Flask==3.0.0 flask-cors==4.0.0 PyPDF2==3.0.1 torch==2.5.1 transformers==4.44.0 sentence-transformers==2.7.0 numpy==1.24.3 python-dotenv==1.0.0 werkzeug==3.0.1

echo.
echo ================================
echo   Starting Flask App...
echo   Open: http://localhost:5000
echo ================================
echo.

python app.py

pause
