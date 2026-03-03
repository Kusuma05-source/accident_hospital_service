@echo off
REM Accident Hospital Service - Windows Startup Script

echo.
echo ========================================
echo   Accident Hospital Service
echo   Emergency Response System
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting Flask application...
echo.
echo ========================================
echo Service running at: http://localhost:5000
echo ========================================
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
