@echo off
echo ========================================
echo ContentCraft Pro - Frontend Server
echo ========================================
echo.
echo Starting frontend development server...
echo.

cd /d "%~dp0"

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
    if errorlevel 1 (
        echo ERROR: Failed to install Node.js dependencies
        echo Make sure Node.js and npm are installed
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo Frontend starting on http://localhost:3000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the development server
npm start

pause

