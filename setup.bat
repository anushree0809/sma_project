@echo off
REM Social Media Analytics Application - Setup Script for Windows

echo ==================================
echo Social Media Analytics Setup
echo ==================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python not found. Please install Python 3.8+
    exit /b 1
)

REM Check Node.js
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Node.js not found. Please install Node.js 14+
    exit /b 1
)

echo OK Python and Node.js found
echo.

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Setup frontend
echo Installing frontend dependencies...
cd frontend
call npm install
cd ..

REM Create .env file
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo WARNING: Update .env with your Apify API key
)

echo.
echo ==================================
echo OK Setup Complete!
echo ==================================
echo.
echo To start the application:
echo.
echo 1. Start backend (Terminal 1):
echo    venv\Scripts\activate.bat
echo    python run.py
echo.
echo 2. Start frontend (Terminal 2):
echo    cd frontend
echo    npm start
echo.
echo Then open http://localhost:3000
echo.
pause
