@echo off
echo ============================================================
echo Amazon Bedrock Content Summarizer
echo ============================================================
echo.

REM Check if credentials are set
if "%AWS_ACCESS_KEY_ID%"=="" (
    echo [ERROR] AWS credentials not found in environment.
    echo.
    echo Please set them first:
    echo   set AWS_ACCESS_KEY_ID=your_key
    echo   set AWS_SECRET_ACCESS_KEY=your_secret
    echo   set AWS_DEFAULT_REGION=us-east-1
    echo.
    pause
    exit /b 1
)

echo [OK] AWS credentials found
echo.
echo Starting Streamlit app...
echo The app will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run streamlit_app.py

pause
