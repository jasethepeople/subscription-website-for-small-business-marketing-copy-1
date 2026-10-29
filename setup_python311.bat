@echo off
echo ========================================
echo ContentCraft Pro - Python 3.11 Setup
echo ========================================
echo.
echo This script will recreate your virtual environment with Python 3.11
echo Make sure you have Python 3.11 installed first!
echo.
pause
echo.
echo Removing old virtual environment...
if exist venv rmdir /s /q venv
echo.
echo Creating new virtual environment with Python 3.11...
C:\Python311\python.exe -m venv venv
if errorlevel 1 (
    echo ERROR: Python 3.11 not found at C:\Python311\python.exe
    echo Please install Python 3.11 first or update the path in this script
    pause
    exit /b 1
)
echo.
echo Activating virtual environment...
call venv\Scripts\activate
echo.
echo Installing packages...
pip install -r requirements.txt
echo.
echo Testing the backend...
echo Starting Flask app (press Ctrl+C to stop)...
python src\main.py

