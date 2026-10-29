@echo off
echo ================================
echo ContentCraft Pro - Seed Templates
echo ================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate
echo.
echo Seeding templates into database...
python src\seed_templates.py
echo.
echo Done! Templates have been seeded.
echo.
pause

