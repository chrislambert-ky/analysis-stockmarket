# GitHub Pages Deployment Guide
**Date:** October 4, 2025  
**Status:** Ready for automated daily updates

---

## Overview

Your Stock Market Analysis site is hosted on **GitHub Pages**, which means:
- ✅ Data files must be in the repository
- ✅ ETL must commit and push updated data
- ✅ GitHub Pages automatically deploys after push
- ✅ Updates go live in 1-2 minutes

---

## Automation Scripts Created

### **Option 1: PowerShell Script** (Recommended for Windows 10+)
**File:** `update-data-to-github.ps1`

**Features:**
- Runs V2 ETL
- Checks for data changes
- Auto-commits with timestamp
- Pushes to GitHub
- Color-coded output
- Error handling

### **Option 2: Batch Script** (Compatible with all Windows)
**File:** `update-data-to-github.bat`

**Features:**
- Same functionality as PowerShell
- Works on older Windows versions
- Simpler output

---

## Manual Run (Test First!)

### PowerShell:
```powershell
cd c:\Apps\gh\analysis-stockmarket
.\update-data-to-github.ps1
```

### Batch:
```cmd
cd c:\Apps\gh\analysis-stockmarket
update-data-to-github.bat
```

---

## What the Scripts Do:

```
[1/4] Running V2 ETL to fetch latest market data...
      ↓ Executes: python etl-market-data-v2.py
      ↓ Fetches from Yahoo Finance
      ↓ Updates data/tickers/ files
      ↓ Updates data/tickers/tickers_index.json

[2/4] Checking for changes in data files...
      ↓ Checks: git status data/
      ↓ If no changes → Exit (nothing to commit)
      ↓ If changes found → Continue

[3/4] Staging and committing changes...
      ↓ Stage: git add data/
      ↓ Commit: git commit -m "Auto-update: Market data ETL run - [timestamp]"

[4/4] Pushing to GitHub...
      ↓ Push: git push origin main
      ↓ GitHub Pages starts deployment
      ↓ Site updates in 1-2 minutes
```

---

## Schedule Daily Automated Updates

### **Method 1: Windows Task Scheduler (GUI)**

1. **Open Task Scheduler:**
   - Press `Win + R`
   - Type: `taskschd.msc`
   - Press Enter

2. **Create Basic Task:**
   - Click "Create Basic Task"
   - Name: `Stock Market ETL - GitHub Pages`
   - Description: `Daily stock market data update with auto-push to GitHub Pages`

3. **Set Trigger:**
   - Trigger: Daily
   - Start: Today
   - Time: `6:00 PM` (after market close)
   - Recur every: 1 days

4. **Set Action:**
   - Action: Start a program
   - Program/script: `powershell.exe`
   - Add arguments: `-ExecutionPolicy Bypass -File "c:\Apps\gh\analysis-stockmarket\update-data-to-github.ps1"`
   - Start in: `c:\Apps\gh\analysis-stockmarket`

5. **Finish:**
   - Check "Open Properties dialog" → OK
   - Under "Security options":
     - Select "Run whether user is logged on or not" (optional)
     - Check "Run with highest privileges" (if needed)

6. **Test it:**
   - Right-click the task → Run
   - Check the History tab for results

---

### **Method 2: PowerShell Scheduled Job**

```powershell
# Run PowerShell as Administrator
$trigger = New-JobTrigger -Daily -At "6:00 PM"
$options = New-ScheduledJobOption -RunElevated

Register-ScheduledJob -Name "StockMarketETL-GitHubPages" -ScriptBlock {
    Set-Location "c:\Apps\gh\analysis-stockmarket"
    & .\update-data-to-github.ps1
} -Trigger $trigger -ScheduledJobOption $options
```

**Check status:**
```powershell
Get-ScheduledJob | Where-Object {$_.Name -like "*StockMarket*"}
```

**Remove if needed:**
```powershell
Unregister-ScheduledJob -Name "StockMarketETL-GitHubPages"
```

---

### **Method 3: GitHub Actions** (Alternative - No local machine needed!)

If you prefer running ETL in the cloud, create `.github/workflows/update-data.yml`:

```yaml
name: Update Stock Market Data

on:
  schedule:
    # Run daily at 6 PM UTC (adjust for your timezone)
    - cron: '0 18 * * *'
  workflow_dispatch: # Allow manual trigger

jobs:
  update-data:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        pip install yfinance pandas
        
    - name: Run ETL
      run: python etl-market-data-v2.py
      
    - name: Commit and push if changed
      run: |
        git config --global user.name 'GitHub Actions Bot'
        git config --global user.email 'actions@github.com'
        git add data/
        git diff --quiet && git diff --staged --quiet || \
        (git commit -m "Auto-update: Market data $(date +'%Y-%m-%d %H:%M:%S')" && git push)
```

**Benefits of GitHub Actions:**
- ✅ Runs in the cloud (no local machine needed)
- ✅ Free for public repos
- ✅ Reliable scheduled execution
- ✅ No Windows machine required

**Drawbacks:**
- ⚠️ Requires repository secrets for authentication
- ⚠️ Limited free minutes (but plenty for this use case)

---

## Git Configuration

### Ensure Git is Configured:

```bash
# Set your name and email (if not already set)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Check current config
git config --list
```

### GitHub Authentication:

**Option 1: Personal Access Token (Recommended)**

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` permissions
3. Store token securely

**Use token for authentication:**
```bash
# First time push will ask for credentials
# Username: your-github-username
# Password: [paste your token]

# Or configure credential helper
git config --global credential.helper wincred
```

**Option 2: SSH Key**

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add key to GitHub: Settings → SSH and GPG keys → New SSH key
# Copy public key
type %USERPROFILE%\.ssh\id_ed25519.pub

# Test connection
ssh -T git@github.com
```

**Update remote to use SSH:**
```bash
git remote set-url origin git@github.com:yourusername/analysis-stockmarket.git
```

---

## Verify GitHub Pages Settings

1. Go to your repo on GitHub
2. Settings → Pages
3. Verify:
   - **Source:** Deploy from a branch
   - **Branch:** main (or master) → / (root)
   - **Custom domain:** (if you have one)

4. Your site URL should be:
   - `https://yourusername.github.io/analysis-stockmarket/`

---

## Testing the Automation

### Test Run 1: Manual Execution
```powershell
cd c:\Apps\gh\analysis-stockmarket
.\update-data-to-github.ps1
```

**Expected output:**
```
[1/4] Running V2 ETL to fetch latest market data...
✓ Fetching AAPL... done
✓ Fetching GOOGL... done
[... more tickers ...]

[2/4] Checking for changes in data files...
✓ Changes detected

[3/4] Staging and committing changes...
✓ Committed: Auto-update: Market data ETL run - 2025-10-04 18:00:00

[4/4] Pushing to GitHub...
✓ Pushed to origin/main

SUCCESS! Data updated and pushed to GitHub Pages
Your GitHub Pages site will update in 1-2 minutes.
```

### Test Run 2: Scheduled Task
1. Right-click task in Task Scheduler → Run
2. Check History tab for execution status
3. Check GitHub repo for new commit
4. Wait 1-2 minutes, verify site updated

---

## Monitoring & Troubleshooting

### Check Last ETL Run:
```bash
# Check last commit
git log --oneline -1

# Check when data was last updated
git log -1 --format="%ai" -- data/
```

### Check GitHub Pages Deployment:
1. Go to repo on GitHub
2. Click "Actions" tab (if using GitHub Actions)
3. Or check "Environments" → github-pages → View deployment

### Common Issues:

**Issue 1: "git push failed - authentication"**
```bash
# Solution: Set up credential helper or use SSH
git config --global credential.helper wincred
# Then try push again - enter token when prompted
```

**Issue 2: "No changes to commit"**
- ETL ran but data didn't change (weekend/holiday)
- This is normal - script will exit gracefully

**Issue 3: "ETL script failed"**
- Check internet connection
- Check Python dependencies: `pip install yfinance pandas`
- Run ETL manually to see error: `python etl-market-data-v2.py`

**Issue 4: "Task runs but nothing happens"**
- Check Task Scheduler History
- Ensure task runs with correct working directory
- Try running script manually first

---

## File Sizes & GitHub Limits

**Current data size:**
- Per ticker per year: ~50-250KB
- 26 tickers × 20 years ≈ **26-130MB total**
- tickers_index.json: ~100KB

**GitHub limits:**
- ✅ File size: <100MB per file (you're well under)
- ✅ Repo size: <1GB recommended (you're fine)
- ✅ Push size: <2GB (no problem)

**Note:** If repo gets large, consider:
- Git LFS (Large File Storage) for CSV files
- Exclude very old year files
- Archive historical data separately

---

## Daily Workflow (Automated)

```
6:00 PM Daily:
  ↓
Scheduled Task Triggers
  ↓
PowerShell Script Runs
  ↓
ETL Fetches Fresh Data
  ↓
Git Commits Changes
  ↓
Git Pushes to GitHub
  ↓
GitHub Pages Deploys
  ↓
Site Updated (1-2 min)
  ↓
Users See Fresh Data!
```

---

## Maintenance

### Weekly:
- Check Task Scheduler history for failures
- Verify site has current data
- Check repo for commit history

### Monthly:
- Review error logs (if any)
- Verify ETL is fetching all tickers
- Check GitHub Pages build status

### As Needed:
- Update Python dependencies: `pip install --upgrade yfinance pandas`
- Update tickers list in `etl-market-data-v2.py`
- Adjust schedule time if market hours change

---

## Rollback / Recovery

### If Bad Data Pushed:

```bash
# See recent commits
git log --oneline -10

# Revert to previous commit
git revert HEAD

# Or hard reset (if needed)
git reset --hard HEAD~1
git push --force origin main
```

### If Script Breaks:

```bash
# Run ETL manually
python etl-market-data-v2.py

# Then manually commit/push
git add data/
git commit -m "Manual data update"
git push origin main
```

---

## Quick Reference

**Manual update:**
```powershell
.\update-data-to-github.ps1
```

**Check scheduled task:**
```
Task Scheduler → Task Scheduler Library → Find "Stock Market ETL"
```

**Force ETL refresh:**
```bash
python etl-market-data-v2.py --force
git add data/
git commit -m "Force refresh: all data"
git push origin main
```

**Check site status:**
- Your site: `https://yourusername.github.io/analysis-stockmarket/`
- Check data freshness: Open any V2 page, check dates

---

## Success Checklist

- [ ] Manual script run successful (`.\update-data-to-github.ps1`)
- [ ] Data committed and pushed to GitHub
- [ ] GitHub Pages site updated (check URL)
- [ ] Scheduled task created in Task Scheduler
- [ ] Test scheduled task runs successfully
- [ ] GitHub credentials/SSH configured
- [ ] Git user.name and user.email set

---

## Support & Resources

**Files Created:**
- `update-data-to-github.ps1` - PowerShell automation script
- `update-data-to-github.bat` - Batch automation script
- `docs/github-pages-deployment.md` - This guide

**Existing Files:**
- `etl-market-data-v2.py` - V2 ETL script
- `data/tickers/tickers_index.json` - Metadata index

**GitHub Pages Docs:**
- https://docs.github.com/en/pages

**Windows Task Scheduler:**
- https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page

---

## Next Steps

1. **Test the script manually** - Run `.\update-data-to-github.ps1`
2. **Verify GitHub push** - Check repo for new commit
3. **Check site updated** - Visit GitHub Pages URL
4. **Schedule the task** - Set up daily automation
5. **Monitor for a week** - Ensure automated runs work

Your site will now automatically stay up-to-date! 🎉
