# Stock Market Analysis Toolkit

**Interactive tools for analyzing Dollar Cost Averaging and Buy-on-Dip investment strategies**

Interactive tools for analyzing investment strategies including Dollar Cost Averaging and Buy-on-Dip approaches. Includes calculators and visualizations to help understand different investment methodologies and their historical performance.

## 🚀 Live Demo

[View the interactive analysis tools here](https://chrislambert-ky.github.io/analysis-stockmarket/)

## Quick Links

- Local site entry: `index.html`
- Pages: `html/dcav2.html`, `html/bodv2.html`, `html/dca-stratv2.html`, `html/bod-stratv2.html`, `html/dca-tickersv2.html`, `html/bod-tickersv2.html`, `html/metricsv2.html`, `html/aboutv2.html`
- ETL: `etl-market-data-v2.py` (generates Parquet datasets under `data/`)

## Minimum Requirements

- Python 3.15.2
- pip packages: see `requirements.txt`
- A modern browser for the frontend (DuckDB-Wasm and ECharts)

## Getting Started (Local)

1. Clone the repo and enter it:
   ```powershell
   git clone https://github.com/chrislambert-ky/analysis-stockmarket.git
   cd analysis-stockmarket
   ```

2. Create a Python 3.15 virtual environment and install the pinned dependencies:
   ```powershell
   pymanager.exe exec -3.15.2 -m venv .venv
   .\.venv\Scripts\pip.exe install -r requirements.txt
   ```

3. Run the ETL to generate data files:
   ```powershell
   .\.venv\Scripts\python.exe .\etl-market-data-v2.py
   ```
   This writes compressed Parquet files and updates `data/tickers/tickers_index.json`.

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
- `html/bod-stratv2.html` — Advanced BOD configurator (configure declines 1%–10% and share quantities).
- `html/metricsv2.html` — Comprehensive metrics dashboard with statistical analysis, price drop frequency, and individual ticker performance analytics.
- `html/dca-vs-bod.html` — Side-by-side strategy comparison visualization.
- `html/aboutv2.html` — Project explanation, methodology, contact.

## Data Files (Produced by ETL)

- `data/etl-data-raw.parquet` — Combined raw daily OHLCV history.
- `data/etl-data-processed.parquet` — Per-ticker daily OHLC with weekday and auxiliary fields used to compute time-filtered metrics.
- `data/etl-data-bod.parquet` — Per-ticker history with precomputed buy-on-dip levels and execution flags.
- `data/tickers/<TICKER>/<TICKER>-<YEAR>.parquet` — Per-ticker, per-year files queried on demand by DuckDB-Wasm.
- `data/tickers/tickers_index.json` — Metadata index with per-ticker last-updated timestamps and available years.

## 🔧 Technical Implementation

### Data Processing
- **Python ETL Pipeline**: Uses pandas, NumPy, PyArrow, and yfinance for historical data collection and compressed Parquet generation
- **Data Source**: Yahoo Finance historical price data via yfinance with comprehensive OHLCV data
- **Analysis Period**: Configurable date ranges with focus on multi-year performance comparisons

### Frontend Framework
- **HTML/CSS/JavaScript**: Responsive design with professional styling using CSS variables and modern layout techniques
- **DuckDB-Wasm 1.32.0**: Browser-side queries over per-ticker Parquet data
- **ECharts 5.x Library**: Interactive visualizations and chart components
- **Calculation Engine**: Advanced JavaScript-based portfolio calculations with precise currency formatting, trade tracking, and market pattern analysis
- **Analytics Integration**: Google Analytics tracking for usage insights and performance monitoring

### Key Implementation Notes
- The ETL script (`etl-market-data-v2.py`) pulls historical OHLC data and writes Parquet datasets. It removes the corresponding generated CSV datasets after a successful run.
- Frontend recomputes cumulative invested/value from per-row `Shares Purchased` and `Dollars Invested` within the user-selected timeframe. This avoids carrying full-history cumulative values into time-filtered views.
- **BOD semantics**:
  - Night-before limit orders at `previous close − N%` for N in 1..configured max.
  - A level is considered filled if the day Low ≤ target_limit.
  - Executed_Price is recorded as the level's target price (multiple fills on a single day remain distinct).
- **UI performance**:
  - DuckDB-Wasm queries only the selected ticker/year Parquet files.
  - Query results are cached in IndexedDB and invalidated using index metadata.

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
├── data/                      # Parquet data files and ticker metadata
│   ├── etl-data-processed.parquet # Historical price data with weekday analysis
│   ├── etl-data-bod.parquet       # Precomputed buy-on-dip levels and flags
│   └── tickers/                   # Per-ticker, per-year Parquet files
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

## Data Architecture

- The nightly ETL fetches daily historical prices and writes raw, processed, and buy-on-dip datasets as compressed Parquet.
- The ETL also writes per-ticker/per-year Parquet files and a JSON index containing paths, date bounds, row counts, and update times.
- Browser pages fetch only the selected years concurrently, query those Parquet buffers together with DuckDB-Wasm, and cache per-year results in IndexedDB.
- CSV remains the format for user-downloaded analysis exports; generated source datasets are Parquet.

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

The ETL emits a compact index at `data/tickers/tickers_index.json` that the frontend uses for targeted per-year queries and instant metadata (date ranges and record counts) without downloading Parquet files.

Example excerpt:

```json
{
  "AAPL": {
    "years": [2005, 2006, 2007],
    "last_updated": "2025-09-17T23:13:28.567456",
    "files": {
      "2025": {
        "path": "data/tickers/AAPL/AAPL-2025.parquet",
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
  - `path` (string): relative path to the Parquet file
  - `min_date` / `max_date` (ISO `yyyy-mm-dd`): earliest and latest dates present in that file
  - `row_count` (int): number of data rows (excludes header)
  - `size_bytes` (int | null): file size in bytes when available
  - `last_updated` (ISO timestamp): when this file was written

**Why this helps:**
- Allows the UI to show exact date range and record counts instantly, without downloading data files just to populate the timeframe controls.
- Enables smarter caching: clients compare `last_updated` timestamps and only fetch stale files.

**Per-ticker file naming convention:** `<SYMBOL>-<YEAR>.parquet`. This makes it simple to query only the requested ticker and years (e.g., `AAPL/AAPL-2025.parquet`).

## CI Suggestion (Optional): Nightly Data Refresh

The GitHub Actions workflow runs `etl-market-data-v2.py` on a cron schedule and commits the updated per-year Parquet files and `tickers_index.json` back to the repository.

Example steps:
1. Checkout repository
2. Set up Python and install requirements
3. Run ETL: `python etl-market-data-v2.py`
4. If files changed, commit the Parquet data and `tickers_index.json` and push (or sync to storage bucket)

> **Security note:** If you store credentials for S3 or a private host, use repository secrets and restrict write access appropriately.

## Troubleshooting

- If a page appears blank after local edits, ensure the HTML file is present and the browser console shows no JS exceptions. Use the `.venv` Python server and inspect Parquet requests and DuckDB-Wasm worker errors.
- To force the ETL to include new tickers, edit `etf_list` in `etl-market-data-v2.py` and re-run it (the script overwrites the data files on each run).

## Contributing

This is a personal project; PRs and issues are welcome. For larger performance improvements, benchmark DuckDB-Wasm query plans and Parquet layout against the current per-ticker/year workflow.

## License

MIT License (see LICENSE)

## Contact

- LinkedIn: https://www.linkedin.com/in/chrislambertky/
- GitHub: https://github.com/chrislambert-ky
