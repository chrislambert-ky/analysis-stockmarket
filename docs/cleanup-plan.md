# Production Code Cleanup Plan
**Date:** October 4, 2025  
**Goal:** Archive development/testing files, keep only production code

---

## 📊 Current State Analysis

### **✅ PRODUCTION (Keep Active)**

**Root Level:**
- ✅ `index.html` - Main homepage (V2 links)
- ✅ `etl-market-data-v2.py` - **PRODUCTION ETL** (current)
- ✅ `update-data-to-github.ps1` - Automation script
- ✅ `update-data-to-github.bat` - Automation script (batch)
- ✅ `requirements.txt` - Python dependencies
- ✅ `package.json` - Project metadata
- ✅ `README.md` - Project documentation
- ✅ `.gitignore` - Git configuration

**Folders:**
- ✅ `html/` - **V2 PAGES** (production)
- ✅ `css/` - Stylesheets
- ✅ `js/` - JavaScript (v2-shared.js)
- ✅ `images/` - Site images
- ✅ `data/tickers/` - **V2 DATA** (per-ticker/year structure)
- ✅ `docs/` - Documentation
- ✅ `.github/workflows/` - GitHub Actions

---

### **📦 TO ARCHIVE (Development/Testing Files)**

**Root Level:**
- ❌ `etl-market-data.py` - V1 ETL (replaced by v2)
- ❌ `analysis-framework.ipynb` - Development notebook
- ❌ `analysis-framework copy.ipynb` - Development notebook

**Folders:**
- ❌ `pages/` - **V1 PAGES** (already backed up in archive/)
- ❌ `py/` - **OLD ETL VERSIONS** (11 files - development iterations)
- ❌ `scripts/` - **TESTING SCRIPTS** (24 files - debugging/validation)
- ❌ `notebooks/` - **JUPYTER NOTEBOOKS** (development/analysis)

**Old Data Files:**
- ❌ `data/etl-data-raw.csv` - V1 flat file
- ❌ `data/etl-data-processed.csv` - V1 processed
- ❌ `data/etl-data-bod.csv` - V1 BOD analysis

---

### **🗑️ TO DELETE (Can be safely removed)**

- ❌ `__pycache__/` - Python cache (regenerates automatically)
- ❌ `.venv/` - Virtual environment (user-specific, in .gitignore)
- ❌ `html/test-v2.html` - Test file
- ❌ `html/slider-demo.html` - Demo file (keep in docs instead)

---

## 🎯 Cleanup Actions

### **Action 1: Archive Development Files**

Move to: `archive/development-2025-10-04/`

```
py/                    → All 11 ETL development versions
scripts/               → All 24 testing/validation scripts  
notebooks/             → All Jupyter notebooks
etl-market-data.py     → V1 ETL script
analysis-framework*.ipynb → Development notebooks
data/etl-data-*.csv    → V1 flat data files
```

### **Action 2: Keep V1 Pages Archive**

Already done: `archive/v1-backup-2025-10-04/pages/`

**Option:** Delete `pages/` folder from root (since it's archived)

### **Action 3: Delete Unnecessary Files**

```
__pycache__/           → Delete (cache, regenerates)
html/test-v2.html      → Delete (test file)
```

### **Action 4: Move Demo to Docs**

```
html/slider-demo.html  → Move to docs/examples/
```

---

## 📁 Proposed Final Structure

```
analysis-stockmarket/
├── .github/
│   └── workflows/
│       └── update-data.yml ✅ PRODUCTION
│
├── archive/                ✅ ARCHIVE ONLY
│   ├── v1-backup-2025-10-04/
│   └── development-2025-10-04/
│
├── css/                    ✅ PRODUCTION
│   ├── style.css
│   ├── metrics.css
│   └── ...
│
├── data/                   ✅ PRODUCTION
│   └── tickers/
│       ├── tickers_index.json
│       └── {SYMBOL}/
│           └── {SYMBOL}-{YEAR}.csv
│
├── docs/                   ✅ DOCUMENTATION
│   ├── examples/
│   │   └── slider-demo.html
│   ├── v2-transition-plan.md
│   ├── v2-migration-complete.md
│   ├── QUICK-TEST.md
│   ├── github-pages-deployment.md
│   ├── QUICK-SETUP-GITHUB-PAGES.md
│   └── github-pages-automation-summary.md
│
├── html/                   ✅ PRODUCTION V2 PAGES
│   ├── aboutv2.html
│   ├── bodv2.html
│   ├── bod-tickersv2.html
│   ├── bod-stratv2.html
│   ├── dcav2.html
│   ├── dca-tickersv2.html
│   ├── dca-stratv2.html
│   └── metricsv2.html
│
├── images/                 ✅ PRODUCTION
│   └── [all SVG files]
│
├── js/                     ✅ PRODUCTION
│   └── v2-shared.js
│
├── index.html              ✅ PRODUCTION
├── etl-market-data-v2.py   ✅ PRODUCTION ETL
├── update-data-to-github.ps1  ✅ PRODUCTION
├── update-data-to-github.bat  ✅ PRODUCTION
├── requirements.txt        ✅ PRODUCTION
├── package.json            ✅ PRODUCTION
├── README.md               ✅ PRODUCTION
└── .gitignore              ✅ PRODUCTION
```

---

## 📊 File Count Reduction

### **Before Cleanup:**
```
Root: 8 files
py/: 11 files
scripts/: 24 files
notebooks/: 4 files
pages/: 8 files (V1)
html/: 10 files
data/: 3 old CSVs + tickers/

Total clutter: ~68 development/legacy files
```

### **After Cleanup:**
```
Root: 8 production files
html/: 8 production V2 pages
data/: Only tickers/ (V2 structure)
archive/: All development files organized

Clean production: ~25 essential files
```

**Reduction:** ~65% fewer files in production workspace!

---

## ✅ Benefits of Cleanup

1. **Clearer Structure** - Only production code visible
2. **Easier Navigation** - No confusion about which ETL to use
3. **Better Git Performance** - Fewer files to track
4. **Cleaner Deployments** - Only production code in repo
5. **Safe Archives** - All development work preserved
6. **Better Documentation** - Clear "production state" docs

---

## 🚀 Execution Plan

### **Phase 1: Create Archive Structure**
```powershell
mkdir archive\development-2025-10-04
```

### **Phase 2: Move Development Files**
```powershell
# ETL development versions
xcopy py archive\development-2025-10-04\py /E /I

# Testing scripts
xcopy scripts archive\development-2025-10-04\scripts /E /I

# Jupyter notebooks
xcopy notebooks archive\development-2025-10-04\notebooks /E /I

# Old ETL
move etl-market-data.py archive\development-2025-10-04\

# Development notebooks
move "analysis-framework.ipynb" archive\development-2025-10-04\
move "analysis-framework copy.ipynb" archive\development-2025-10-04\

# Old V1 data files
move data\etl-data-*.csv archive\development-2025-10-04\data\
```

### **Phase 3: Delete Unnecessary**
```powershell
# Delete cache
rmdir /S /Q __pycache__

# Delete test file
del html\test-v2.html
```

### **Phase 4: Delete V1 Pages Folder**
```powershell
# Already archived in archive\v1-backup-2025-10-04\pages\
rmdir /S /Q pages
```

### **Phase 5: Move Demo to Docs**
```powershell
mkdir docs\examples
move html\slider-demo.html docs\examples\
```

### **Phase 6: Update .gitignore** (if needed)
Add archived folders to .gitignore if not committing them

---

## 📝 Documentation Updates Needed

After cleanup, update:

1. **README.md** - Reflect new structure
2. **Create:** `docs/PRODUCTION-STRUCTURE.md` - Document final structure
3. **Create:** `docs/ARCHIVED-FILES.md` - List what's archived and why

---

## ⚠️ Safety Notes

- ✅ All files are **moved to archive**, not deleted
- ✅ `archive/` folder is **safe to keep** in repo (documents history)
- ✅ Can **restore any file** from archive if needed
- ✅ Git history **preserves everything** even if deleted

---

## 🔙 Rollback Plan

If you need to restore anything:

```powershell
# Restore a specific file
copy archive\development-2025-10-04\py\etl-v8-final.py py\

# Restore entire folder
xcopy archive\development-2025-10-04\scripts scripts\ /E /I

# Restore V1 pages
xcopy archive\v1-backup-2025-10-04\pages pages\ /E /I
```

---

## ✅ Ready to Execute?

**Options:**

1. **Full Cleanup** - Archive all development files (recommended)
2. **Partial Cleanup** - Just archive `py/` and `scripts/`
3. **Conservative** - Only delete `__pycache__` and test files

**Recommendation:** Full cleanup (Option 1)
- Cleanest result
- Everything preserved in archive
- Easy to navigate production code
- Professional structure

---

## 📋 Checklist

Before executing:
- [ ] Backup important work (already done via git)
- [ ] Verify archive folder exists
- [ ] Confirm V1 backup is complete
- [ ] Review what's being archived
- [ ] Test that production still works after cleanup

After executing:
- [ ] Test website still loads
- [ ] Test ETL v2 still runs
- [ ] Test automation scripts work
- [ ] Update README.md
- [ ] Document new structure
- [ ] Commit cleanup changes

---

**Ready to proceed with cleanup?**
