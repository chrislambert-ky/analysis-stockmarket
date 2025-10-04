# GitHub Pages ETL Automation Script
# This script runs the V2 ETL, then commits and pushes the updated data to GitHub Pages

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Stock Market Data ETL - GitHub Pages Update" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Change to the repository directory
$repoPath = "c:\Apps\gh\analysis-stockmarket"
Set-Location $repoPath

Write-Host "[1/4] Running V2 ETL to fetch latest market data..." -ForegroundColor Yellow
Write-Host ""

# Run the ETL script
python etl-market-data-v2.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: ETL script failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/4] Checking for changes in data files..." -ForegroundColor Yellow
Write-Host ""

# Check git status
$gitStatus = git status --porcelain data/

if ([string]::IsNullOrWhiteSpace($gitStatus)) {
    Write-Host "No changes detected in data files. Nothing to commit." -ForegroundColor Green
    Write-Host ""
    Write-Host "ETL completed successfully - data is up to date!" -ForegroundColor Green
    exit 0
}

Write-Host "Changes detected:" -ForegroundColor Green
git status data/
Write-Host ""

Write-Host "[3/4] Staging and committing changes..." -ForegroundColor Yellow
Write-Host ""

# Stage all changes in data folder
git add data/

# Create commit with timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMessage = "Auto-update: Market data ETL run - $timestamp"

git commit -m $commitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Git commit failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[4/4] Pushing to GitHub..." -ForegroundColor Yellow
Write-Host ""

# Push to remote
git push origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Git push failed! Check your credentials and connection." -ForegroundColor Red
    Write-Host "You may need to manually push with: git push origin main" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "SUCCESS! Data updated and pushed to GitHub Pages" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your GitHub Pages site will update in 1-2 minutes." -ForegroundColor Cyan
Write-Host ""
