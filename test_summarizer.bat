@echo off
echo ============================================================
echo Testing Amazon Bedrock Summarizer
echo ============================================================
echo.

REM Check if credentials are set
if "%AWS_ACCESS_KEY_ID%"=="" (
    echo AWS credentials not found in environment.
    echo.
    echo Please set them first:
    echo   set AWS_ACCESS_KEY_ID=your_key
    echo   set AWS_SECRET_ACCESS_KEY=your_secret
    echo   set AWS_DEFAULT_REGION=us-east-1
    echo.
    pause
    exit /b 1
)

echo Running summarizer with sample text...
echo.
python bedrock_summarizer.py sample_text.txt

echo.
echo ============================================================
echo Test complete!
echo ============================================================
pause
