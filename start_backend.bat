@echo off
echo ========================================
echo ContentCraft Pro - Python 3.13 Compatible
echo ========================================
echo.
echo Starting backend server...
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Make sure Python is installed and added to PATH
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install requirements if needed
if not exist "venv\Lib\site-packages\flask" (
    echo Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo Backend starting on http://localhost:5000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the application
python src/main.py

pause

