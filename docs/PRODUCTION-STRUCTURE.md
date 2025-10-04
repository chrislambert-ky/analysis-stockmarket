# Production Structure Documentation
**Last Updated:** October 4, 2025  
**Version:** V2 Architecture  
**Status:** ✅ Clean Production State

---

## 📂 Production Folder Structure

```
analysis-stockmarket/
├── .github/
│   └── workflows/
│       └── update-data.yml          # GitHub Actions automation (daily ETL)
│
├── css/
│   ├── about.css                    # About page styles
│   ├── metrics.css                  # Metrics dashboard styles
│   ├── style.css                    # Main stylesheet
│   └── ticker-metrics.css           # Ticker-specific styles
│
├── data/
│   └── tickers/
│       ├── tickers_index.json       # Metadata (26 tickers, date ranges)
│       └── {SYMBOL}/
│           └── {SYMBOL}-{YEAR}.csv  # Per-ticker, per-year data files
│
├── docs/
│   ├── examples/
│   │   └── slider-demo.html         # Slider component demo
│   ├── cleanup-plan.md              # This cleanup documentation
│   ├── github-pages-automation-summary.md
│   ├── github-pages-deployment.md
│   ├── PRODUCTION-STRUCTURE.md      # ← This file
│   ├── QUICK-SETUP-GITHUB-PAGES.md
│   ├── QUICK-TEST.md
│   ├── slider-implementation-summary.md
│   ├── slider-migration-examples.md
│   ├── v2-migration-complete.md
│   ├── v2-slider-usage.md
│   └── v2-transition-plan.md
│
├── html/
│   ├── aboutv2.html                 # About page
│   ├── bodv2.html                   # Buy-on-dip calculator
│   ├── bod-stratv2.html             # Advanced BOD strategy
│   ├── bod-tickersv2.html           # BOD multi-ticker grid
│   ├── dcav2.html                   # Dollar cost average calculator
│   ├── dca-stratv2.html             # Advanced DCA strategy
│   ├── dca-tickersv2.html           # DCA multi-ticker grid
│   └── metricsv2.html               # Ticker metrics dashboard
│
├── images/
│   └── [27 SVG files]               # Site images/icons
│
├── js/
│   ├── debug_dca_dates.js           # Debug utility (legacy)
│   └── v2-shared.js                 # V2 shared library (IndexedDB, slider)
│
├── index.html                       # Homepage (navigation to all V2 pages)
├── etl-market-data-v2.py           # ✅ PRODUCTION ETL
├── update-data-to-github.ps1       # Local automation (PowerShell)
├── update-data-to-github.bat       # Local automation (Batch)
├── requirements.txt                # Python dependencies
├── package.json                    # Project metadata
├── README.md                       # Project documentation
└── .gitignore                      # Git exclusions
```

---

## 🚀 Production Components

### **1. V2 HTML Pages** (`html/`)

All pages use **V2 architecture** with:
- IndexedDB caching for performance
- Per-ticker/year data loading
- Shared library (`v2-shared.js?v=4`)
- Responsive design

**Main Pages:**
- **DCA (Dollar Cost Averaging):**
  - `dcav2.html` - Single ticker calculator
  - `dca-tickersv2.html` - Multi-ticker comparison grid
  - `dca-stratv2.html` - Advanced with custom settings

- **BOD (Buy-on-Dip):**
  - `bodv2.html` - Single ticker calculator
  - `bod-tickersv2.html` - Multi-ticker comparison grid
  - `bod-stratv2.html` - Advanced with custom settings

- **Metrics:**
  - `metricsv2.html` - Comprehensive ticker metrics dashboard

- **Info:**
  - `aboutv2.html` - About page

### **2. V2 ETL** (`etl-market-data-v2.py`)

**Purpose:** Fetch Yahoo Finance data and generate V2 data structure

**Features:**
- Per-ticker folders: `data/tickers/{SYMBOL}/`
- Per-year CSV files: `{SYMBOL}-{YEAR}.csv`
- Metadata in `tickers_index.json` (date ranges, last updated)
- Force refresh: `--force` flag
- Configurable ticker list in script

**Usage:**
```bash
python etl-market-data-v2.py          # Update all tickers
python etl-market-data-v2.py --force  # Force refresh all data
```

**Last Run:** October 3, 2025, 11:07 PM  
**Current Tickers:** 26 symbols

### **3. V2 Data Structure** (`data/tickers/`)

**Format:**
```
data/tickers/
├── tickers_index.json              # Metadata file
│   {
│     "AAPL": {
│       "earliest_date": "2020-01-02",
│       "latest_date": "2025-10-03",
│       "last_updated": "2025-10-03T23:07:15"
│     },
│     ...
│   }
│
└── AAPL/
    ├── AAPL-2020.csv
    ├── AAPL-2021.csv
    ├── AAPL-2022.csv
    ├── AAPL-2023.csv
    ├── AAPL-2024.csv
    └── AAPL-2025.csv
```

**Benefits:**
- Smaller file downloads (only needed years)
- Faster page loads
- IndexedDB caching per file
- Easy to update individual years

### **4. V2 Shared Library** (`js/v2-shared.js`)

**Version:** v=4  
**Features:**
- `V2Shared.loadTickerData(symbol, years)` - Smart data loading
- IndexedDB caching with version management
- Cache expiration (7 days)
- Automatic cache rebuilds
- Slider component for date ranges
- Utility functions for calculations

**Usage in pages:**
```html
<script src="../js/v2-shared.js?v=4"></script>
<script>
  V2Shared.loadTickerData('AAPL', [2023, 2024, 2025])
    .then(data => {
      // Process ticker data
    });
</script>
```

### **5. Automation**

**Local Automation (Windows):**
- `update-data-to-github.ps1` - PowerShell script
- `update-data-to-github.bat` - Batch wrapper

**Cloud Automation (GitHub Actions):**
- `.github/workflows/update-data.yml`
- Runs daily at 6 PM UTC
- Auto-commits and pushes data updates

**Process:**
1. Run ETL v2 script
2. Git add updated data files
3. Git commit with timestamp
4. Git push to main branch
5. GitHub Pages auto-deploys

---

## 🗄️ Archived Files

### **Archive Structure:**

```
archive/
├── v1-backup-2025-10-04/
│   ├── pages/                       # V1 HTML pages (8 files)
│   │   ├── about.html
│   │   ├── bod.html
│   │   ├── bod-strat.html
│   │   ├── bod-tickers.html
│   │   ├── dca.html
│   │   ├── dca-strat.html
│   │   ├── dca-tickers.html
│   │   └── metrics.html
│   └── etl-market-data.py           # V1 ETL script
│
└── development-2025-10-04/
    ├── py/                          # ETL development versions (11 files)
    ├── scripts/                     # Testing scripts (25 files)
    ├── notebooks/                   # Jupyter notebooks (4 files)
    ├── data-old/                    # Old V1 CSV files (3 files)
    ├── etl-market-data.py           # V1 ETL (duplicate)
    └── analysis-framework.ipynb     # Development notebook
```

### **What Was Archived:**

**V1 Components (v1-backup-2025-10-04/):**
- All V1 HTML pages
- V1 ETL script
- Used flat CSV files (`etl-data-*.csv`)

**Development Files (development-2025-10-04/):**
- **py/**: 11 ETL iterations (etl.py, etlv1-5.py, etl-v4 through v8-final.py)
- **scripts/**: 25 testing/analysis scripts
- **notebooks/**: Jupyter notebooks for analysis
- **data-old/**: Old flat CSV data files

**Why Archived:**
- No longer used in production
- Preserved for reference/history
- Keeps production workspace clean
- Can be restored if needed

---

## ✅ Production Checklist

### **Website Functionality:**
- [ ] Homepage (`index.html`) loads
- [ ] All 8 V2 pages accessible from nav
- [ ] DCA calculators work
- [ ] BOD calculators work
- [ ] Metrics dashboard displays data
- [ ] Multi-ticker grids load correctly
- [ ] Advanced strategy pages function

### **Data & ETL:**
- [ ] `data/tickers/` contains 26 ticker folders
- [ ] `tickers_index.json` exists and is valid
- [ ] ETL v2 runs without errors: `python etl-market-data-v2.py`
- [ ] Data updates reflect in website

### **Automation:**
- [ ] PowerShell script runs: `.\update-data-to-github.ps1`
- [ ] GitHub Actions workflow enabled
- [ ] Daily updates commit automatically

### **Performance:**
- [ ] IndexedDB caching works (check DevTools → Application → IndexedDB)
- [ ] Pages load quickly after initial cache
- [ ] No console errors in browser

---

## 📊 Before & After Cleanup

### **Before Cleanup:**
```
Root level: 8+ files
Folders:
- pages/ (8 V1 HTML files)
- py/ (11 old ETL versions)
- scripts/ (25 testing scripts)
- notebooks/ (4 Jupyter notebooks)
- html/ (10 files including test)

Total: ~70+ files scattered across development/production
```

### **After Cleanup:**
```
Root level: 8 essential production files
Folders:
- html/ (8 V2 production pages)
- data/tickers/ (V2 data structure)
- docs/ (organized documentation)
- archive/ (all legacy files preserved)

Total: ~25 essential production files
Reduction: 65% fewer files in production workspace!
```

---

## 🔄 Maintenance

### **Regular Tasks:**

**Daily (Automated):**
- ETL runs via GitHub Actions at 6 PM UTC
- Data auto-commits and pushes
- GitHub Pages auto-deploys

**Weekly:**
- Monitor GitHub Actions for failures
- Check data quality in `tickers_index.json`
- Verify website functionality

**Monthly:**
- Review cache performance
- Check for new ticker additions needed
- Update documentation if needed

### **Manual ETL Run:**

```bash
# Navigate to project folder
cd c:\Apps\gh\analysis-stockmarket

# Run ETL
python etl-market-data-v2.py

# Or force refresh all data
python etl-market-data-v2.py --force

# Commit and push
git add data/
git commit -m "Update market data"
git push
```

### **Adding New Tickers:**

1. Edit `etl-market-data-v2.py`
2. Add ticker symbol to `TICKERS` list
3. Run ETL: `python etl-market-data-v2.py --force`
4. Verify in `data/tickers/` and `tickers_index.json`
5. Commit and push changes

---

## 🛠️ Troubleshooting

### **Website Not Loading Data:**
1. Check browser console for errors
2. Verify `tickers_index.json` exists
3. Clear IndexedDB cache (DevTools → Application → IndexedDB)
4. Hard refresh: Ctrl+Shift+R

### **ETL Fails:**
1. Check Python version: `python --version` (needs 3.x)
2. Verify dependencies: `pip install -r requirements.txt`
3. Check Yahoo Finance API availability
4. Try with `--force` flag

### **Automation Not Working:**
1. **Local:** Check Task Scheduler for errors
2. **GitHub Actions:** Review workflow run logs in GitHub
3. Verify git credentials configured
4. Check for merge conflicts

---

## 📚 Key Documentation

- **[cleanup-plan.md](cleanup-plan.md)** - Full cleanup documentation
- **[v2-migration-complete.md](v2-migration-complete.md)** - V2 migration report
- **[github-pages-deployment.md](github-pages-deployment.md)** - Automation guide
- **[QUICK-TEST.md](QUICK-TEST.md)** - Quick testing checklist
- **[v2-slider-usage.md](v2-slider-usage.md)** - Slider component API

---

## 🎯 Production URLs

Assuming GitHub Pages at: `https://{username}.github.io/analysis-stockmarket/`

- **Homepage:** `/index.html`
- **DCA Calculator:** `/html/dcav2.html`
- **BOD Calculator:** `/html/bodv2.html`
- **DCA Tickers:** `/html/dca-tickersv2.html`
- **BOD Tickers:** `/html/bod-tickersv2.html`
- **Metrics Dashboard:** `/html/metricsv2.html`
- **About:** `/html/aboutv2.html`

---

## ✨ Architecture Benefits

**V2 Improvements over V1:**
1. **Performance:** IndexedDB caching, smaller file downloads
2. **Scalability:** Easy to add new tickers and years
3. **Maintenance:** Modular structure, clear separation of concerns
4. **Automation:** Daily data updates without manual intervention
5. **Code Quality:** Shared library reduces duplication
6. **Developer Experience:** Clean workspace, clear documentation

---

**Questions or Issues?**
Refer to documentation in `docs/` folder or check archived files for reference implementations.
