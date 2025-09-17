@echo off
echo Building WeatherStar 4000+ v2.1.0 for Windows...
echo.
echo Prerequisites:
echo - Python 3.8+ with pip
echo - PyInstaller (pip install pyinstaller)
echo - All dependencies from requirements.txt
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist WeatherStar4000.exe del WeatherStar4000.exe

REM Build executable
echo Building executable...
pyinstaller --onefile ^
    --windowed ^
    --name WeatherStar4000 ^
    --icon weatherstar_assets/app_icons/weatherstar.ico ^
    --add-data "weatherstar_assets;weatherstar_assets" ^
    --add-data "weatherstar_modules;weatherstar_modules" ^
    --hidden-import pygame ^
    --hidden-import requests ^
    --hidden-import PIL ^
    --hidden-import ephem ^
    weatherstar4000.py

REM Copy to root
if exist dist\WeatherStar4000.exe (
    copy dist\WeatherStar4000.exe .
    echo.
    echo Build complete! WeatherStar4000.exe created.
    echo.

    REM Create release zip
    echo Creating release package...
    if exist WeatherStar4000-v2.1.0-Windows.zip del WeatherStar4000-v2.1.0-Windows.zip
    powershell Compress-Archive -Path WeatherStar4000.exe, README.md, LICENSE, requirements.txt, RELEASE_NOTES.md -DestinationPath WeatherStar4000-v2.1.0-Windows.zip
    echo Release package created: WeatherStar4000-v2.1.0-Windows.zip
) else (
    echo Build failed!
)

pause