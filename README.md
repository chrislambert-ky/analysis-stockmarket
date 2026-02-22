# Stock Market Analysis Toolkit

**Interactive tools for analyzing Dollar Cost Averaging and Buy-on-Dip investment strategies**

Interactive tools for analyzing investment strategies including Dollar Cost Averaging and Buy-on-Dip approaches. Includes calculators and visualizations to help understand different investment methodologies and their historical performance.

## 🚀 Live Demo

[View the interactive analysis tools here](https://chrislambert-ky.github.io/analysis-stockmarket/)

## Quick Links

- Local site entry: `index.html`
- Pages: `html/dcav2.html`, `html/bodv2.html`, `html/dca-stratv2.html`, `html/bod-stratv2.html`, `html/dca-tickersv2.html`, `html/bod-tickersv2.html`, `html/metricsv2.html`, `html/aboutv2.html`
- ETL: `etl-market-data-v2.py` (generates `data/etl-data-processed.csv` and `data/etl-data-bod.csv`)

## Minimum Requirements

- Python 3.8+
- pip packages: see `requirements.txt`
- A modern browser for the frontend (ECharts)

## Getting Started (Local)

1. Clone the repo and enter it:
   ```powershell
   git clone https://github.com/chrislambert-ky/analysis-stockmarket.git
   cd analysis-stockmarket
   ```

2. Create a virtual environment and install dependencies:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\pip.exe install -r requirements.txt
   ```

3. Run the ETL to generate data files:
   ```powershell
   .\.venv\Scripts\python.exe .\etl-market-data-v2.py
   ```
   This will overwrite `data/etl-data-processed.csv` and `data/etl-data-bod.csv`.

4. Serve the site locally and open the pages:
   ```powershell
   .\.venv\Scripts\python.exe -m http.server 8000
   # Open http://localhost:8000/html/dcav2.html or http://localhost:8000/html/bodv2.html
   ```

## 📊 Investment Strategies Analyzed

### Dollar Cost Averaging (DCA)
- **Method**: Regular periodic investments of fixed dollar amounts regardless of market conditions
- **Default Strategy**: Invests $25 weekly with customizable investment days (Monday–Friday)
- **Benefits**: Reduces impact of market volatility through consistent investing
- **Advanced Features**: Configurable investment amounts, selectable investment days, and week-over-week profitability tracking

### Buy-on-Dip (BOD)
- **Method**: Purchase shares when the stock price declines by specified percentages from the previous day's close
- **Default Strategy**: Buys 1 share per 1–5% decline with configurable decline thresholds
- **Benefits**: Capitalizes on market downturns and temporary price reductions
- **Advanced Features**: Up to 10 customizable decline percentages (1%–10%) with individual share quantities per threshold

### Strategy Comparison
- Side-by-side analysis of DCA vs BOD performance across different tickers and timeframes
- Interactive visualizations showing portfolio growth patterns and trade timing
- Historical backtesting across multiple market conditions with detailed performance metrics

## 🛠️ Features

- **Multi-Ticker Analysis**: Compare strategy performance across multiple ETFs simultaneously with unified charting
- **Advanced Calculators**: Fully customizable tools for testing investment amounts, frequencies, decline percentages, and date ranges
- **Interactive Charts**: ECharts-powered visualizations showing portfolio growth, purchase timing, and comparative analysis
- **Metrics Dashboard**: Comprehensive statistical analysis page with price drop frequency, volatility metrics, and individual ticker performance analytics
- **Market Pattern Analytics**:
  - **Up Days vs Down Days**: Daily market direction analysis (open-to-close price comparison)
  - **Monday–Friday Success Rate**: Weekly trading pattern analysis (Monday close to Friday close profitability)
  - **Week-over-Week Success**: Short-term profitability tracking for investment timing optimization
- **CSV Export**: Download detailed transaction history with trade execution details and comprehensive performance metrics
- **Responsive Design**: Mobile-friendly interface that works across all device types
- **CSS Design System**: Unified styling with professional navigation, consistent title/subtitle formatting, and responsive design patterns

## What Each Page Does

- `html/dcav2.html` — Interactive DCA overview, per-ticker chart and single-ticker analysis.
- `html/dca-tickersv2.html` — Grid of per-ticker DCA mini-charts (YTD default).
- `html/dca-stratv2.html` — Advanced DCA configurator (custom weekly amounts, day selection).
- `html/bodv2.html` — Buy-on-Dip overview (grid of tickers, per-ticker detail, timeframe controls).
- `html/bod-tickersv2.html` — Grid of per-ticker BOD mini-charts (YTD default).
- `html/bod-stratv2.html` — Advanced BOD configurator (configure declines 1%–10% and share quantities). Uses `data/etl-data-bod.csv` fast-path when available.
- `html/metricsv2.html` — Comprehensive metrics dashboard with statistical analysis, price drop frequency, and individual ticker performance analytics.
- `html/dca-vs-bod.html` — Side-by-side strategy comparison visualization.
- `html/aboutv2.html` — Project explanation, methodology, contact.

## Data Files (Produced by ETL)

- `data/etl-data-processed.csv` — Per-ticker daily OHLC with weekday and auxiliary fields used to compute time-filtered metrics.
- `data/etl-data-bod.csv` — Precomputed buy-on-dip events (Buy_Price, Buy_Level, Executed_Price, Executed_Level, Shares Purchased, Dollars Invested, cumulative fields). The frontend uses this as a fast path for advanced strategy simulations.
- `data/tickers/<TICKER>/<TICKER>-<YEAR>.csv` — Per-ticker, per-year CSV files for targeted fetching.
- `data/tickers/tickers_index.json` — Metadata index with per-ticker last-updated timestamps and available years.

## 🔧 Technical Implementation

### Data Processing
- **Python ETL Pipeline**: Uses pandas and yfinance for historical data collection with enhanced CSV generation including weekday analysis and price averaging
- **Data Source**: Yahoo Finance historical price data via yfinance with comprehensive OHLCV data
- **Analysis Period**: Configurable date ranges with focus on multi-year performance comparisons

### Frontend Framework
- **HTML/CSS/JavaScript**: Responsive design with professional styling using CSS variables and modern layout techniques
- **ECharts 5.x Library**: Interactive visualizations and chart components with real-time data updates
- **Calculation Engine**: Advanced JavaScript-based portfolio calculations with precise currency formatting, trade tracking, and market pattern analysis
- **Analytics Integration**: Google Analytics tracking for usage insights and performance monitoring

### Key Implementation Notes
- The ETL script (`etl-market-data-v2.py`) pulls historical OHLC data and writes normalized CSVs. It intentionally overwrites the data files on each run.
- Frontend recomputes cumulative invested/value from per-row `Shares Purchased` and `Dollars Invested` within the user-selected timeframe. This avoids carrying full-history cumulative values into time-filtered views.
- **BOD semantics**:
  - Night-before limit orders at `previous close − N%` for N in 1..configured max.
  - A level is considered filled if the day Low ≤ target_limit.
  - Executed_Price is recorded as the level's target price (multiple fills on a single day remain distinct).
- **UI performance**:
  - CSV parsing is cached per page load.
  - When a single ticker is selected, the frontend takes a fast path and processes only that ticker's rows on period changes.

### UX Conventions Used Across Pages
- Default selection on load: ALL tickers + YTD period.
- Period and ticker controls are independent after load: selecting a ticker does not reset the period and vice versa.
- Tooltips show period-filtered cumulative Invested and Value and the number of Shares (no plotted shares series).

## 📁 Project Structure

```
analysis-stockmarket/
├── css/                       # Stylesheets
│   ├── style.css             # Main stylesheet with design system
│   ├── metrics.css           # Metrics page styling
│   ├── ticker-metrics.css    # Ticker metrics component styling
│   └── about.css             # About page styling
├── data/                      # Data files
│   ├── etl-data-processed.csv # Historical price data with weekday analysis
│   ├── etl-data-bod.csv       # Precomputed buy-on-dip events
│   └── tickers/               # Per-ticker, per-year CSV files
│       └── tickers_index.json # Metadata index
├── html/                      # Analysis pages (v2)
│   ├── dcav2.html            # Dollar Cost Averaging analysis
│   ├── bodv2.html            # Buy-on-Dip analysis
│   ├── dca-vs-bod.html       # Strategy comparison visualization
│   ├── dca-tickersv2.html    # DCA all-tickers comparison
│   ├── bod-tickersv2.html    # BOD all-tickers comparison
│   ├── dca-stratv2.html      # Advanced DCA calculator
│   ├── bod-stratv2.html      # Advanced BOD calculator
│   ├── metricsv2.html        # Comprehensive metrics dashboard
│   └── aboutv2.html          # About page with project documentation
├── js/                        # JavaScript utilities
│   └── v2-shared.js          # Shared utilities for v2 pages
├── scripts/                   # Utility scripts
├── etl-market-data-v2.py      # Main data collection script
├── index.html                 # Homepage with strategy navigation
├── requirements.txt           # Python dependencies
└── README.md                  # This documentation
```

## 🔬 Advanced Analytics Features

### Market Pattern Analytics
- **Up Days vs Down Days**: Comprehensive analysis of daily market direction by comparing opening to closing prices, providing insights into overall trend patterns and volatility within selected date ranges
- **Monday–Friday Success Rate**: Measures how often buying at Monday's closing price and selling at Friday's closing price would be profitable, revealing weekly market cycles and trading patterns
- **Week-over-Week Profitability**:
  - **DCA Strategy**: Analyzes market performance between consecutive weeks based on total weeks available in the selected date range, not just investment weeks
  - **BOD Strategy**: Tracks individual trade profitability after one week from execution, measuring trade timing effectiveness
- **Date Range Filtering**: All metrics are calculated based on user-selected start and end dates, ensuring accurate analysis within chosen time periods

## 🆕 Recent Updates

- **Metrics Dashboard**: New comprehensive metrics page with statistical analysis for individual tickers including price drop frequency, volatility metrics, and performance analytics
- **Enhanced Week-over-Week Analysis**: DCA strategy now calculates week-over-week success based on total weeks available in the selected date range, providing more accurate market trend analysis
- **CSS Design System**: Implemented consistent styling across all pages with unified navigation classes and standardized title/subtitle formatting
- **Professional Navigation**: Updated all pages with `.main-nav` and `.nav-link` classes for consistent user experience
- **Improved Mobile Responsiveness**: Enhanced responsive design patterns for better mobile and tablet experience
- **Advanced Metrics Precision**: All analytics calculations now properly filter data within user-selected date ranges for accurate time-period analysis

## Version 2 Roadmap

Version 2 is a focused modernization and performance pass. Goals include:

- Use a modern CSS framework (Bootstrap 5 or Tailwind CSS) — decision TBD.
- Prioritize HTML5-first over JavaScript for core functionality. Pages should work with semantic HTML and progressive enhancement.
- Split JavaScript out of HTML pages into modular files under `js/` (e.g., `js/bod.js`, `js/dca.js`, `js/ticker-loader.js`).
- Use the smaller per-ticker data files generated by the ETL instead of loading full-history CSVs in the browser.
- Add additional daily-derived metrics for each ticker:
  - Moving averages (SMA/EMA) over configurable windows
  - Linear regression trend line and slope
  - Optional upper/lower bands (e.g., regression channel or simple volatility bands)
- Implement IndexedDB for client-side caching:
  - Cache per-ticker/per-year data keyed by ticker + year and a data-version or timestamp
  - On page load, check last-updated metadata and only refresh stale data
  - Implement a stale-while-revalidate flow: serve cached data immediately, then refresh in the background
- Continue using Apache ECharts; migrate chart initialization and options into the new JS modules.

**Implementation quick wins**
- Change the ETL to optionally emit per-ticker JSON to avoid browser CSV parsing.
- Extract current inline scripts into discrete files in `js/` — low risk, enables incremental refactors.
- Add a small IndexedDB helper and embed `last_updated` in `tickers_index.json` so the client can decide whether to refresh data.

**Layout and compatibility**
- Version 2 HTML files live in `/html/`. Version 1 pages are preserved in the archive for reference.

## ⚠️ Important Disclaimers

- **Not Financial Advice**: This is not financial advice or investment recommendations.
- **Educational Purpose**: Personal project for learning web development and financial data analysis.
- **No Professional Guidance**: I am not a licensed financial advisor or professional investment manager.
- **Past Performance**: Past performance does not guarantee future results.
- **Investment Risk**: All investment strategies carry risk, including potential loss of principal.
- **Dividend Limitation**: Dividend payments are **not** included in this analysis.
- **Real-World Costs**: Calculations do not account for dividends, transaction fees, taxes, or other real-world trading costs.
- **Consult Professionals**: Please consult with a qualified financial advisor before making investment decisions.

## ETF & Stock Summary

| Ticker | Name & Strategy |
|--------|-----------------|
| **TQQQ** | ProShares UltraPro QQQ – 3× daily leveraged exposure to NASDAQ-100 (short-term use only). |
| **UPRO** | ProShares UltraPro S&P 500 – 3× daily leveraged exposure to the S&P 500 (short-term use only). |
| **GGLL** | Direxion Daily GOOGL Bull 2× – Leverages Alphabet's daily returns. |
| **MSFU** | Direxion Daily MSFT Bull – 2× (or possibly 1.5×) leveraged returns of Microsoft stock. |
| **QQQ** | Invesco QQQ – Nasdaq-100 index fund; tech-heavy, low-cost, long-term exposure. |
| **FBCG** | Fidelity Blue Chip Growth ETF – Actively managed large-cap growth equity ETF. |
| **QTOP** | iShares Nasdaq Top 30 ETF – Tracks top 30 NASDAQ-100 companies. |
| **MGK** | Vanguard Mega Cap Growth ETF – Mega-cap U.S. growth stocks exposure. |
| **VGT** | Vanguard Information Technology ETF – Broad tech-sector index fund across all market caps. |
| **SPLG** | SPDR Portfolio S&P 500 ETF – Low-cost S&P 500 index tracker. |
| **XLG** | Invesco S&P 500 Top 50 ETF – Concentrated top-50 S&P 500 companies exposure. |
| **TOPT** | iShares Top 20 U.S. Stocks ETF – Focuses on the 20 largest U.S. companies. |
| **MSFT** | Microsoft Corp – Large-cap tech and cloud services leader. |
| **GOOGL** | Alphabet Inc. (Class A) – Parent of Google; ad and AI giant. |
| **HSBC** | HSBC Holdings plc – Global banking and financial services. |
| **ALLY** | Ally Financial Inc. – Digital-first auto finance and banking services. |

## Developer Notes: tickers_index.json Schema

The ETL emits a compact index at `data/tickers/tickers_index.json` that the frontend uses for targeted per-year fetches and to provide instant metadata (date ranges and record counts) without fetching CSVs.

Example excerpt:

```json
{
  "AAPL": {
    "years": [2005, 2006, 2007],
    "last_updated": "2025-09-17T23:13:28.567456",
    "files": {
      "2025": {
        "path": "data/tickers/AAPL/AAPL-2025.csv",
        "min_date": "2025-01-02",
        "max_date": "2025-09-17",
        "row_count": 184,
        "size_bytes": 12345,
        "last_updated": "2025-09-17T23:13:28.567456"
      },
      "2024": { }
    }
  }
}
```

**Fields:**
- `years`: list of available years for the ticker (integers)
- `last_updated`: timestamp for when the ticker's files were last (re)generated
- `files["<YEAR>"]`: object for the per-year file with:
  - `path` (string): relative path to the CSV file
  - `min_date` / `max_date` (ISO `yyyy-mm-dd`): earliest and latest dates present in that file
  - `row_count` (int): number of data rows (excludes header)
  - `size_bytes` (int | null): file size in bytes when available
  - `last_updated` (ISO timestamp): when this file was written

**Why this helps:**
- Allows the UI to show exact date range and record counts instantly, avoiding network probes or CSV parsing when the user adjusts the timeframe slider.
- Enables smarter caching: clients compare `last_updated` timestamps and only fetch stale files.

**Per-ticker file naming convention:** `<SYMBOL>-<YEAR>.csv` (or `.json`). This makes it simple to request only the newest files (e.g., `AAPL/AAPL-2025.csv`).

## CI Suggestion (Optional): Nightly Data Refresh

Create a GitHub Actions workflow that runs `etl-market-data-v2.py` on a cron schedule and either commits the updated per-year CSVs and `tickers_index.json` back to the repository, or uploads them to blob storage / S3.

Example steps:
1. Checkout repository
2. Set up Python and install requirements
3. Run ETL: `python etl-market-data-v2.py --force`
4. If files changed, commit `data/tickers/*` and push (or sync to storage bucket)

> **Security note:** If you store credentials for S3 or a private host, use repository secrets and restrict write access appropriately.

## Troubleshooting

- If a page appears blank after local edits, ensure the HTML file is present and the browser console shows no JS exceptions. Use the `.venv` Python server and inspect network requests for CSV files.
- To force the ETL to include new tickers, edit `etf_list` in `etl-market-data-v2.py` and re-run it (the script overwrites the data files on each run).

## Contributing

This is a personal project; PRs and issues are welcome. For larger performance improvements, consider generating per-ticker JSON outputs from the ETL to eliminate CSV parsing in the browser.

## License

MIT License (see LICENSE)

## Contact

- LinkedIn: https://www.linkedin.com/in/chrislambertky/
- GitHub: https://github.com/chrislambert-ky
