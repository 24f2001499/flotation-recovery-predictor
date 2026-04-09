@echo off
REM Quick Streamlit App Deployment Script for Windows
REM This script prepares your app for Streamlit Cloud deployment

echo ========================================
echo Froth Flotation Predictor - Deployment Setup
echo ========================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo Download Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1] Git found ✓
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Download Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [2] Python found ✓
echo.

REM Install requirements
echo [3] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [3] Dependencies installed ✓
echo.

REM Test the app locally
echo [4] Testing app locally...
echo (Press Ctrl+C to stop after testing)
echo.

timeout /t 3

streamlit run streamlit_app.py

echo.
echo ========================================
echo Deployment Checklist:
echo ========================================
echo.
echo [ ] 1. Create GitHub account (https://github.com)
echo [ ] 2. Create new repository named "flotation-recovery-predictor"
echo [ ] 3. Push files to GitHub:
echo.
echo     git init
echo     git add .
echo     git commit -m "Initial commit: Streamlit app"
echo     git branch -M main
echo     git remote add origin https://github.com/YOUR_USERNAME/flotation-recovery-predictor.git
echo     git push -u origin main
echo.
echo [ ] 4. Go to https://share.streamlit.io/
echo [ ] 5. Sign in with GitHub
echo [ ] 6. Click "New app"
echo [ ] 7. Select your repository
echo [ ] 8. Confirm deployment
echo.
echo [ ] 9. Wait 2-3 minutes for deployment
echo [ ] 10. Your app is LIVE at https://share.streamlit.io/YOUR_USERNAME/flotation-recovery-predictor
echo.
echo ========================================
echo For more details, see: STREAMLIT_DEPLOYMENT_GUIDE.md
echo ========================================
echo.
pause
