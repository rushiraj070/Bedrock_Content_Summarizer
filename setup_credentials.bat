@echo off
echo ============================================================
echo AWS Credentials Setup for Amazon Bedrock
echo ============================================================
echo.
echo Please enter your AWS credentials:
echo.
set /p AWS_KEY="AWS Access Key ID: "
set /p AWS_SECRET="AWS Secret Access Key: "
set /p AWS_REGION="AWS Region (default: us-east-1): "

if "%AWS_REGION%"=="" set AWS_REGION=us-east-1

echo.
echo Setting environment variables...
setx AWS_ACCESS_KEY_ID "%AWS_KEY%"
setx AWS_SECRET_ACCESS_KEY "%AWS_SECRET%"
setx AWS_DEFAULT_REGION "%AWS_REGION%"

echo.
echo ============================================================
echo Credentials saved! Please restart your terminal or IDE.
echo ============================================================
pause
