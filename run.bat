@echo off
echo ========================================================
echo OpenCV AI Competition 2026 - Powered by AWS
echo Launching Autonomous Closed-Loop Inspection System...
echo ========================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found in PATH, trying py launcher...
    py -3.13 -m streamlit run app.py
) else (
    streamlit run app.py
)
pause
