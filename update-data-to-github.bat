@echo off
REM GitHub Pages ETL Automation Script (Batch version)
REM This script runs the V2 ETL, then commits and pushes the updated data to GitHub Pages

echo ================================================
echo Stock Market Data ETL - GitHub Pages Update
echo ================================================
echo.

cd /d "c:\Apps\gh\analysis-stockmarket"

echo [1/4] Running V2 ETL to fetch latest market data...
echo.

python etl-market-data-v2.py

if errorlevel 1 (
    echo.
    echo ERROR: ETL script failed!
    exit /b 1
)

echo.
echo [2/4] Checking for changes in data files...
echo.

git status --porcelain data/ > %TEMP%\git-status.txt
for %%A in (%TEMP%\git-status.txt) do set size=%%~zA
if %size% == 0 (
    echo No changes detected in data files. Nothing to commit.
    echo.
    echo ETL completed successfully - data is up to date!
    del %TEMP%\git-status.txt
    exit /b 0
)

echo Changes detected:
git status data/
echo.

echo [3/4] Staging and committing changes...
echo.

git add data/

REM Create commit with timestamp
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set mydate=%%c-%%a-%%b
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a:%%b
set timestamp=%mydate% %mytime%

git commit -m "Auto-update: Market data ETL run - %timestamp%"

if errorlevel 1 (
    echo.
    echo ERROR: Git commit failed!
    exit /b 1
)

echo.
echo [4/4] Pushing to GitHub...
echo.

git push origin main

if errorlevel 1 (
    echo.
    echo ERROR: Git push failed! Check your credentials and connection.
    echo You may need to manually push with: git push origin main
    exit /b 1
)

echo.
echo ================================================
echo SUCCESS! Data updated and pushed to GitHub Pages
echo ================================================
echo.
echo Your GitHub Pages site will update in 1-2 minutes.
echo.

del %TEMP%\git-status.txt
