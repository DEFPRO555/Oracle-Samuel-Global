@echo off
REM Oracle Samuel Setup Script for Windows
REM © 2025 Dowek Analytics Ltd.

echo ========================================
echo ORACLE SAMUEL - THE REAL ESTATE MARKET PROPHET
echo Setup Script
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo ✓ Pip upgraded
echo.

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo ========================================
echo Setup Complete! 
echo ========================================
echo.
echo To run Oracle Samuel:
echo   1. Activate venv: venv\Scripts\activate
echo   2. Run app: streamlit run app.py
echo.
pause

