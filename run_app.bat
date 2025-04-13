@echo off
TITLE Mind Journal Application

echo ===================================
echo Mind Journal - Local Setup
echo ===================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error creating virtual environment.
        echo Please make sure Python is installed and in your PATH.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo Error activating virtual environment.
    pause
    exit /b 1
)

REM Check if requirements are installed
if not exist venv\Lib\site-packages\flask (
    echo Installing requirements...
    pip install -r requirements_list.txt
    if errorlevel 1 (
        echo Error installing requirements.
        pause
        exit /b 1
    )
)

REM Create instance directory if not exists
if not exist instance (
    echo Creating instance directory...
    mkdir instance
)

REM Run the application
echo.
echo Starting Mind Journal application...
echo.
echo Access the application at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python run.py

REM Deactivate virtual environment when done
call venv\Scripts\deactivate

pause