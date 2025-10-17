@echo off
echo 🚀 Oracle Samuel - GitHub Deployment Script
echo ================================================

cd /d "%~dp0"

if not exist "ORACLE_SAMUEL_GITHUB" (
    echo ❌ ORACLE_SAMUEL_GITHUB folder not found!
    echo Please run this script from the main project directory.
    pause
    exit /b 1
)

cd ORACLE_SAMUEL_GITHUB
echo 📁 Changed to: %CD%

if not exist ".git" (
    echo 🔧 Initializing Git repository...
    git init
    if errorlevel 1 (
        echo ❌ Git initialization failed!
        pause
        exit /b 1
    )
    echo ✅ Git repository initialized
) else (
    echo ✅ Git repository already initialized
)

echo 🔄 Adding files to Git...
git add .
if errorlevel 1 (
    echo ❌ Adding files failed!
    pause
    exit /b 1
)

echo 🔄 Committing changes...
git commit -m "Update Oracle Samuel for GitHub Pages deployment"
if errorlevel 1 (
    echo ℹ️  No changes to commit or commit failed
)

echo 🔄 Checking remote repositories...
git remote -v >nul 2>&1
if errorlevel 1 (
    echo.
    echo 🔗 Please add your GitHub repository remote:
    echo Example: git remote add origin https://github.com/yourusername/oracle-samuel-universal.git
    echo.
    echo After adding the remote, run:
    echo git push -u origin main
    pause
    exit /b 0
)

echo 🔄 Pushing to GitHub...
git push origin main
if errorlevel 1 (
    echo ❌ Push failed! If this is your first push, try:
    echo git push -u origin main
    pause
    exit /b 1
)

echo.
echo 🎉 Deployment completed successfully!
echo 🌐 Your site will be available at:
echo https://yourusername.github.io/oracle-samuel-universal/
echo.
echo 📋 Next steps:
echo 1. Go to your GitHub repository
echo 2. Navigate to Settings → Pages
echo 3. Select 'Deploy from a branch' → 'main'
echo 4. Wait 5-10 minutes for deployment to complete

pause
