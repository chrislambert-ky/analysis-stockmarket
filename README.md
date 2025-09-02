# Stock Market Analysis Toolkit

**Interactive tools for analyzing Dollar Cost Averaging and Buy-on-Dip investment strategies**

*This project provides interactive tools for analyzing investment strategies including Dollar Cost Averaging and Buy-on-Dip approaches. It includes various calculators and visualizations to help users understand different investment methodologies and their historical performance.*

## 🆕 Recent Updates

- **Enhanced Week-over-Week Analysis**: DCA strategy now calculates week-over-week success based on total weeks available in selected date range, providing more accurate market trend analysis
- **CSS Design System**: Implemented consistent styling across all strategy pages with unified navigation classes and standardized title/subtitle formatting
- **Professional Navigation**: Updated all pages with .main-nav and .nav-link classes for consistent user experience
- **Improved Mobile Responsiveness**: Enhanced responsive design patterns for better mobile and tablet experience
- **Advanced Metrics Precision**: All analytics calculations now properly filter data within user-selected date ranges for accurate time-period analysis

## 🚀 Live Demo

[View the interactive analysis tools here](https://chrislambert-ky.github.io/analysis-stockmarket/) *(Update this URL when deployed)*

## 📊 Investment Strategies Analyzed

### Dollar Cost Averaging (DCA)
- **Method**: Regular periodic investments of fixed dollar amounts regardless of market conditions
- **Default Strategy**: Invests $25 weekly with customizable investment days (Monday-Friday)
- **Benefits**: Reduces impact of market volatility through consistent investing
- **Advanced Features**: Configurable investment amounts, selectable investment days, and week-over-week profitability tracking

### Buy-on-Dip (BOD)
- **Method**: Purchase shares when stock price declines by specified percentages from previous day's close
- **Default Strategy**: Buys 1 share per 1-5% decline with configurable decline thresholds
- **Benefits**: Capitalizes on market downturns and temporary price reductions
- **Advanced Features**: Up to 10 customizable decline percentages (1%-10%) with individual share quantities for each threshold

### Strategy Comparison
- Side-by-side analysis of DCA vs BOD performance across different tickers and timeframes
- Interactive visualizations showing portfolio growth patterns and trade timing
- Historical backtesting across multiple market conditions with detailed performance metrics

## 🛠️ Features

- **Multi-Ticker Analysis**: Compare strategy performance across multiple ETFs (QQQ, SPLG, XLG) simultaneously with unified charting
- **Advanced Calculators**: Fully customizable tools allowing users to test their own investment amounts, frequencies, decline percentages, and date ranges
- **Interactive Charts**: ECharts-powered visualizations showing portfolio growth, purchase timing, and comparative analysis with real-time updates
- **Market Pattern Analytics**: Advanced metrics including:
  - **Up Days vs Down Days**: Daily market direction analysis (open to close price comparison)
  - **Monday-Friday Success Rate**: Weekly trading pattern analysis (Monday close to Friday close profitability)
  - **Week-over-Week Success**: Short-term profitability tracking for investment timing optimization
- **CSV Export**: Download detailed transaction history with trade execution details and comprehensive performance metrics
- **Responsive Design**: Mobile-friendly interface that works seamlessly across all device types
- **Professional UI**: Clean, modern design with intuitive navigation and real-time parameter adjustment featuring consistent styling across all pages
- **CSS Design System**: Unified styling with professional navigation classes, consistent title/subtitle formatting, and responsive design patterns
- **Cross-Platform Compatibility**: Mobile-friendly interface optimized for desktop, tablet, and mobile devices with adaptive layouts

## 🔧 Technical Implementation

### Data Processing
- **Python ETL Pipeline**: Uses pandas and yfinance for historical data collection with enhanced CSV generation including weekday analysis and price averaging
- **Data Source**: Yahoo Finance historical price data via yfinance Python library with comprehensive OHLCV data
- **Analysis Period**: Configurable date ranges with focus on multi-year performance comparisons and flexible time windows

### Frontend Framework
- **HTML/CSS/JavaScript**: Responsive design with professional styling using CSS variables and modern layout techniques
- **ECharts 5.x Library**: Interactive visualizations and chart components with real-time data updates
- **Calculation Engine**: Advanced JavaScript-based portfolio calculations with precise currency formatting, trade tracking, and market pattern analysis
- **Analytics Integration**: Google Analytics tracking (G-468B94S87K) for usage insights and performance monitoring

## 📁 Project Structure

```
analysis-stockmarket/
├── css/                    # Stylesheets
│   ├── style.css          # Main stylesheet with professional design system
│   └── about.css          # About page styling with responsive layout
├── data/                  # CSV data files
│   └── history_tickers.csv # Historical price data with weekday analysis
├── js/                    # JavaScript utilities
├── pages/                 # Analysis pages (8 total)
│   ├── dca.html          # Dollar Cost Averaging analysis ($25/week default)
│   ├── bod.html          # Buy-on-Dip analysis (1-5% decline default)
│   ├── dca-vs-bod.html   # Strategy comparison visualization
│   ├── dca-tickers.html  # DCA all tickers comparison
│   ├── bod-tickers.html  # BOD all tickers comparison
│   ├── dca-strat.html    # Advanced DCA calculator (customizable amounts/days)
│   ├── bod-strat.html    # Advanced BOD calculator (configurable decline %s)
│   └── about.html        # About page with project documentation
├── py/                   # Python ETL scripts
├── etl-market-data.py    # Main data collection script with yfinance
├── index.html            # Homepage with strategy navigation grid
├── requirements.txt      # Python dependencies (pandas, yfinance, etc.)
└── README.md            # This documentation
```

## ⚠️ Important Disclaimers

- **Not Financial Advice**: This is not financial advice or investment recommendations
- **Educational Purpose**: Personal project for learning web development and financial data analysis
- **No Professional Guidance**: I am not a licensed financial advisor or professional investment manager
- **Past Performance**: Past performance does not guarantee future results
- **Investment Risk**: All investment strategies carry risk, including potential loss of principal
- **Dividend Limitation**: Dividend payments are **not** included in this analysis, as the dataset does not contain dividend information
- **Real-World Costs**: All calculations do not account for dividends, transaction fees, taxes, or other real-world trading costs
- **Consult Professionals**: Please consult with a qualified financial advisor before making investment decisions

## � Advanced Analytics Features

### Market Pattern Analytics
- **Up Days vs Down Days**: Comprehensive analysis of daily market direction by comparing opening to closing prices, providing insights into overall trend patterns and market volatility within selected date ranges
- **Monday-Friday Success Rate**: Measures how often buying at Monday's closing price and selling at Friday's closing price would be profitable, revealing weekly market cycles and trading patterns
- **Week-over-Week Profitability**: 
  - **DCA Strategy**: Analyzes market performance between consecutive weeks based on total weeks available in the selected date range, not just investment weeks
  - **BOD Strategy**: Tracks individual trade profitability after one week from execution, measuring trade timing effectiveness
- **Date Range Filtering**: All metrics are calculated based on user-selected start and end dates, ensuring accurate analysis within chosen time periods
# Stock Market Analysis Toolkit

Interactive tools for analyzing Dollar Cost Averaging (DCA) and Buy‑on‑Dip (BOD) strategies using historical market data.

This repository contains a small ETL pipeline that collects OHLCV history and a set of client pages that simulate and visualize DCA and BOD strategies across multiple tickers and timeframes.

Quick links
- Local site entry: `index.html`
- Pages: `pages/dca.html`, `pages/bod.html`, `pages/dca-strat.html`, `pages/bod-strat.html`, `pages/dca-tickers.html`, `pages/bod-tickers.html`, `pages/about.html`
- ETL: `etl-market-data.py` (generates `data/history_tickers.csv` and `data/all_buy_on_dip.csv`)

Minimum requirements
- Python 3.8+
- pip packages: see `requirements.txt`
- A modern browser for the frontend (ECharts)

Getting started (local)
1. Clone the repo and enter it:
  ```powershell
  git clone https://github.com/chrislambert-ky/analysis-stockmarket.git
  cd analysis-stockmarket
  ```

2. Create and use your python venv, then install deps:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\pip.exe install -r requirements.txt
  ```

3. Run the ETL to regenerate CSVs:
  ```powershell
  .\.venv\Scripts\python.exe .\etl-market-data.py
  ```
  This will overwrite `data/history_tickers.csv` and `data/all_buy_on_dip.csv`.

4. Serve the site (simple static server) and open the pages:
  ```powershell
  .\.venv\Scripts\python.exe -m http.server 8000
  # Open http://localhost:8000/pages/dca.html and pages/bod.html
  ```

What each page does
- `pages/dca.html` — Interactive DCA overview, per‑ticker chart and single‑ticker analysis.
- `pages/dca-tickers.html` — Grid of per‑ticker DCA mini‑charts (YTD default).
- `pages/dca-strat.html` — Advanced DCA configurator (custom weekly amounts, day selection).
- `pages/bod.html` — Buy‑on‑Dip overview (grid of tickers, per‑ticker detail, timeframe controls).
- `pages/bod-tickers.html` — Grid of per‑ticker BOD mini‑charts (YTD default).
- `pages/bod-strat.html` — Advanced BOD configurator (configure declines 1%–10% and share quantities). Uses `data/all_buy_on_dip.csv` fast‑path when available.
- `pages/about.html` — Project explanation, methodology, contact.

Data files (produced by ETL)
- `data/history_tickers.csv` — Per‑ticker daily OHLC (Date_add), weekday and auxiliary fields used to compute time‑filtered metrics.
- `data/all_buy_on_dip.csv` — Precomputed buy‑on‑dip events (Buy_Price, Buy_Level, Executed_Price/Executed_Level, Shares Purchased, Dollars Invested, Cumulative fields). The frontend can use this file as a fast path for advanced strategy simulations.

Key implementation notes
- The ETL script (`etl-market-data.py`) pulls historical OHLC data and writes normalized CSVs. It intentionally overwrites `data/history_tickers.csv` on each run to ensure tickers in the current list are used.
- Frontend recomputes cumulative invested/value from per‑row 'Shares Purchased' and 'Dollars Invested' within the user selected timeframe (period buttons). This avoids carrying full-history cumulative values into time‑filtered views.
- BOD semantics:
  - Night‑before limit orders at previous close − N% for N in 1..configured max.
  - A level is considered filled if the day Low ≤ target_limit.
  - Executed_Price recorded as the level's target price (so multiple fills on a single day remain distinct).
- UI performance:
  - CSV parsing is cached per page load.
  - When a single ticker is selected, the frontend takes a fast path and processes only that ticker's rows on period changes.

UX conventions used across pages
- Default selection on load: ALL tickers + YTD period.
- Period and ticker controls are independent after load: selecting a ticker does not reset the period and vice‑versa.
- Tooltips show period‑filtered cumulative Invested and Value and the number of Shares (no plotted shares series).

Troubleshooting
- If a page appears blank after local edits, ensure the HTML file is present and that the browser console shows no JS exceptions. Use the `.venv` python server to serve files and inspect network requests for CSV files.
- To force the ETL to include current tickers, edit the etf_list in `etl-market-data.py` and re-run it (the script overwrites `data/history_tickers.csv` each run).

Contributing / notes
- This is a personal project; PRs and issues are welcome. For larger performance improvements, consider generating per‑ticker JSON outputs from the ETL to eliminate CSV parsing in the browser.

License
- MIT License (see LICENSE)


ETF & Stock Summary

Below is an overview of selected ETFs and equities analyzed in this project:

| Ticker | Name & Strategy |
|--------|------------------|
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

Contact
- LinkedIn: https://www.linkedin.com/in/chrislambertky/
- GitHub: https://github.com/chrislambert-ky
