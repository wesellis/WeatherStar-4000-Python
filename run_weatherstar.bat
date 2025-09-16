@echo off
rem WeatherStar 4000 Launcher for Windows
rem Double-click this file to run

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Starting WeatherStar 4000...
python weatherstar4000.py
pause