@echo off
echo ================================
echo Video Deduplication Tool Launcher
echo ================================
echo.

cd /d "%~dp0"

echo Checking required components...
if not exist "ffmpeg-8.0\bin\ffmpeg.exe" (
    echo Error: ffmpeg-8.0\bin\ffmpeg.exe not found
    echo Please ensure all files are in the same directory
    pause
    exit /b 1
)

if not exist "ffmpeg-8.0\bin\ffprobe.exe" (
    echo Error: ffmpeg-8.0\bin\ffprobe.exe not found
    echo Please ensure all files are in the same directory
    pause
    exit /b 1
)

rem Prefer the bundled portable Python (skip it if it is only a tiny LFS stub)
set "PY_CMD="
for %%A in ("python\python.exe") do if %%~zA GTR 10000 set "PY_CMD=python\python.exe"

if not defined PY_CMD (
    where python >nul 2>nul && set "PY_CMD=python"
)

if not defined PY_CMD (
    where py >nul 2>nul && set "PY_CMD=py"
)

if not defined PY_CMD (
    echo Error: no usable Python found.
    echo The bundled python\python.exe is missing or invalid,
    echo and no system Python was found in PATH.
    echo Please keep the bundled python folder or install Python 3.10+.
    pause
    exit /b 1
)

echo Using Python: %PY_CMD%
echo Starting Video Deduplication Tool...
echo.

"%PY_CMD%" "video_dedup_tool.py"

if %errorlevel% neq 0 (
    echo.
    echo Program encountered an error, please check the error message above
    pause
)
