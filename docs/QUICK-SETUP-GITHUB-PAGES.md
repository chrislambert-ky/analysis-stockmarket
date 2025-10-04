# Quick Setup: GitHub Pages Auto-Update

## 🚀 Step 1: Test Manual Run (5 minutes)

Open PowerShell in your project folder and run:

```powershell
cd c:\Apps\gh\analysis-stockmarket
.\update-data-to-github.ps1
```

**What it does:**
1. Runs ETL (fetches fresh market data)
2. Commits changes to git
3. Pushes to GitHub
4. Your site updates automatically in 1-2 minutes!

**Expected output:**
```
[1/4] Running V2 ETL to fetch latest market data...
[2/4] Checking for changes in data files...
[3/4] Staging and committing changes...
[4/4] Pushing to GitHub...

SUCCESS! Data updated and pushed to GitHub Pages
```

---

## ⚙️ Step 2: Schedule Daily Updates (10 minutes)

### Quick PowerShell Setup (Administrator required):

```powershell
# Run PowerShell as Administrator
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File c:\Apps\gh\analysis-stockmarket\update-data-to-github.ps1" `
    -WorkingDirectory "c:\Apps\gh\analysis-stockmarket"

$trigger = New-ScheduledTaskTrigger -Daily -At 6:00PM

$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType S4U

Register-ScheduledTask `
    -TaskName "StockMarket-GitHubPages-Update" `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Description "Daily stock market data update with auto-push to GitHub Pages"
```

### Or Use Task Scheduler GUI:

1. **Open:** `Win + R` → type `taskschd.msc` → Enter
2. **Create Basic Task:**
   - Name: `StockMarket-GitHubPages-Update`
   - Trigger: Daily at 6:00 PM
   - Action: Start a program
   - Program: `powershell.exe`
   - Arguments: `-ExecutionPolicy Bypass -File "c:\Apps\gh\analysis-stockmarket\update-data-to-github.ps1"`
   - Start in: `c:\Apps\gh\analysis-stockmarket`
3. **Finish** and test it!

---

## ✅ Step 3: Verify It Works

### Test the scheduled task:
1. Open Task Scheduler
2. Find "StockMarket-GitHubPages-Update"
3. Right-click → **Run**
4. Check History tab for results

### Check GitHub:
- Visit your repo: `https://github.com/yourusername/analysis-stockmarket`
- Should see new commit: "Auto-update: Market data ETL run - [timestamp]"

### Check Your Site:
- Visit: `https://yourusername.github.io/analysis-stockmarket/`
- Wait 1-2 minutes after push
- Site should have fresh data!

---

## 🔧 Troubleshooting

### "git push failed"
```bash
# Set up credentials
git config --global credential.helper wincred

# Try again - enter your GitHub token when prompted
.\update-data-to-github.ps1
```

### "Python not found"
```bash
# Make sure Python is in PATH
python --version

# If not found, reinstall Python with "Add to PATH" checked
```

### "Task runs but nothing happens"
- Check Task Scheduler → History
- Run script manually to see errors
- Ensure working directory is set correctly

---

## 📋 What You Have Now

✅ **`update-data-to-github.ps1`** - Automated update script  
✅ **`update-data-to-github.bat`** - Batch version (alternative)  
✅ **Scheduled Task** - Runs daily at 6 PM  
✅ **Auto-push to GitHub** - Site stays current  
✅ **GitHub Pages** - Deploys automatically  

---

## 📚 Full Documentation

See **`docs/github-pages-deployment.md`** for:
- Detailed setup instructions
- GitHub Actions alternative (cloud-based)
- Authentication setup
- Monitoring and troubleshooting
- Rollback procedures

---

## 🎯 Daily Workflow (Automated)

```
Every day at 6 PM:
  └─> Task Scheduler runs script
      └─> ETL fetches fresh data
          └─> Git commits changes
              └─> Git pushes to GitHub
                  └─> GitHub Pages deploys
                      └─> Site updated! (1-2 min)
```

---

## ⏭️ Next Steps

1. ✅ Test manual run: `.\update-data-to-github.ps1`
2. ✅ Schedule daily task
3. ✅ Test scheduled task once
4. ✅ Check site updates correctly
5. ✅ Monitor for a week to ensure reliability

**You're done!** Your site will now automatically update daily with fresh market data! 🎉
