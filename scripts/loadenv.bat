@echo off

:: Check if .env file path is provided as an argument
IF "%~1"=="" (
    echo Usage: %0 path_to_env_file
    exit /b 1
)

:: Load environment variables from the provided .env file
for /f "tokens=1,* delims===" %%a in ('type "%~1" 2^>nul') do (
    set "%%a=%%b"
)

echo Environment variables loaded from %~1
