# Quick V2 Testing Guide

## ✅ Migration Complete - Now Test!

**Test URL:** `http://127.0.0.1:5500/index.html`

---

## Quick Test Checklist (5 Minutes)

### 1. Homepage ✓
- [ ] Opens without errors
- [ ] Shows 8 strategy cards with images
- [ ] All cards are clickable

### 2. Click "Dollar Cost Averaging" → dcav2.html
- [ ] Page loads
- [ ] Ticker dropdown shows tickers (AAPL, GOOGL, etc.)
- [ ] Select "AAPL" + "1Y" period + Click Calculate
- [ ] Results table appears with data
- **Expected:** Shows investment returns, shares, final value

### 3. Click "Metrics Dashboard" (from homepage) → metricsv2.html
- [ ] Ticker grid displays (26 tickers in boxes)
- [ ] Click "AAPL"
- [ ] Metrics display (Up Days, Down Days, streaks, success rates)
- [ ] Slider at top works (drag from YTD to 5Y)
- [ ] Metrics recalculate when slider changes

### 4. Check Browser Console (F12)
- [ ] No red errors
- [ ] Should see messages like:
  - `Loaded tickers index (per-ticker)`
  - `Loading AAPL 2024 (1/2)`
- [ ] ✅ = Working correctly!

### 5. Check IndexedDB Cache (F12 → Application → IndexedDB)
- [ ] Database: `stockmarket-cache` exists
- [ ] Store: `files` has entries
- [ ] Keys look like: `data/tickers/AAPL/AAPL-2024.csv::2025-10-03...`
- [ ] ✅ = Caching is working!

---

## Expected Behavior

### First Load:
- Ticker grid: **Instant** (from metadata)
- Data loading: **2-5 seconds** (fetching + parsing)
- Progress bar visible during load

### Second Load (Same Ticker):
- Ticker grid: **Instant**
- Data loading: **<1 second** (from IndexedDB cache)
- Much faster! 🚀

---

## If Something Doesn't Work:

### Ticker Grid Not Showing:
1. Check: `http://127.0.0.1:5500/data/tickers/tickers_index.json` opens
2. If 404: Run `python etl-market-data-v2.py`

### No Data Loads:
1. Open Console (F12), check for errors
2. Clear cache: Ctrl+Shift+Del → Clear browsing data
3. Hard refresh: Ctrl+Shift+R

### Performance Not Improved:
1. Check IndexedDB (F12 → Application)
2. If empty, try selecting a ticker again
3. Second load should be instant

---

## Quick Comparison Test

### Test V1 vs V2 Speed:

**V1 (Old - if still accessible):**
- URL: `http://127.0.0.1:5500/pages/metrics.html`
- Load time: ~5-10 seconds (every time)

**V2 (New):**
- URL: `http://127.0.0.1:5500/html/metricsv2.html`
- First load: ~5 seconds
- Second load: **<1 second** ⚡

---

## All V2 Pages to Test:

1. ✅ `html/dcav2.html` - Dollar Cost Averaging
2. ✅ `html/dca-tickersv2.html` - DCA All Tickers
3. ✅ `html/dca-stratv2.html` - Advanced DCA
4. ✅ `html/bodv2.html` - Buy on Dip
5. ✅ `html/bod-tickersv2.html` - BOD All Tickers
6. ✅ `html/bod-stratv2.html` - Advanced BOD
7. ✅ `html/metricsv2.html` - Metrics Dashboard
8. ✅ `html/aboutv2.html` - About Page

---

## Success! 🎉

If you can:
- ✅ Navigate through all pages
- ✅ See ticker data
- ✅ Calculate results
- ✅ Notice faster subsequent loads

**Then V2 migration is successful!**

---

## Full Details:

See `docs/v2-migration-complete.md` for:
- Complete test checklist
- Performance expectations
- ETL maintenance instructions
- Rollback procedures
- Troubleshooting guide
