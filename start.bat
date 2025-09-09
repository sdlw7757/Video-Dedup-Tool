@echo off
echo ================================
echo Video Deduplication Tool Launcher
echo ================================
echo.

cd /d "%~dp0"

echo Checking required components...
if not exist "python\python.exe" (
    echo Error: python\python.exe not found
    echo Please ensure all files are in the same directory
    pause
    exit /b 1
)

if not exist "ffmpeg-8.0\bin\ffmpeg.exe" (
    echo Error: ffmpeg-8.0\bin\ffmpeg.exe not found
    echo Please ensure all files are in the same directory
    pause
    exit /b 1
)

echo Starting Video Deduplication Tool...
echo.

"python\python.exe" "video_dedup_tool.py"

if %errorlevel% neq 0 (
    echo.
    echo Program encountered an error, please check the error message above
    pause
)