# Stock Market Analysis Toolkit

**Interactive tools for analyzing Dollar Cost Averaging and Buy-on-Dip investment strategies**

*This project provides interactive tools for analyzing investment strategies including Dollar Cost Averaging and Buy-on-Dip approaches. It includes various calculators and visualizations to help users understand different investment methodologies and their historical performance.*

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
- **Professional UI**: Clean, modern design with intuitive navigation and real-time parameter adjustment
- **Real-time Calculations**: Instant strategy recalculation as users modify parameters with live chart updates

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

### Market Pattern Analysis
- **Up Days vs Down Days**: Comprehensive analysis of daily market direction by comparing opening to closing prices, providing insights into overall trend patterns and market volatility
- **Monday-Friday Success Rate**: Measures how often buying at Monday's closing price and selling at Friday's closing price would be profitable, revealing weekly market cycles
- **Week-over-Week Profitability**: 
  - **DCA Strategy**: Shows success rate of investments held for one week from the selected investment day
  - **BOD Strategy**: Tracks individual trade profitability after one week from execution

### Customizable Strategy Parameters
- **DCA Advanced Calculator**: 
  - Selectable investment day (Monday through Friday)
  - Any investment amount ($1 to unlimited)
  - Flexible date ranges for backtesting
- **BOD Advanced Calculator**:
  - Up to 10 different decline percentages (1%-10%)
  - Custom share quantities for each decline threshold
  - Precise limit order simulation based on daily low prices

### Real-time Analytics
- **Instant Recalculation**: Strategy metrics update immediately as users modify parameters
- **Live Chart Updates**: Interactive ECharts visualizations refresh automatically with parameter changes
- **Detailed Trade Tracking**: Complete transaction history with precise purchase prices, decline percentages, and cumulative performance metrics

## �💾 Data Sources and Methodology

This project analyzes historical stock market data to compare the effectiveness of different investment strategies. The analysis uses real historical price data from Yahoo Finance to simulate how these strategies would have performed over various time periods.

**Key Features:**
- Strategy simulation with precise calculation of share purchases, portfolio values, and performance metrics
- Interactive charts showing portfolio growth, purchase timing, and comparative analysis
- CSV download capability for detailed transaction history and further analysis
- Mobile optimization ensuring accessibility across all device types

## 🎯 Educational Purpose

This project serves as both a learning exercise in web development and a practical tool for understanding investment strategies. It demonstrates skills in data analysis, JavaScript programming, responsive web design, and financial calculation methodologies. The interactive nature of the tools helps users visualize how different approaches to investing might perform under various market conditions.

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Node.js (for development)
- Web browser

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/chrislambert-ky/analysis-stockmarket.git
   cd analysis-stockmarket
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the ETL script to collect data:
   ```bash
   python etl-market-data.py
   ```

4. Open `index.html` in your web browser or serve with a local web server

## ETF & Stock Summary

Below is an overview of selected ETFs and equities in our portfolio:

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

## 🤝 Contributing

This is a personal learning project, but suggestions and feedback are welcome! Feel free to open issues or submit pull requests.

## 📞 Connect

- **LinkedIn**: [Chris Lambert](https://www.linkedin.com/in/chrislambertky/)
- **GitHub**: [@chrislambert-ky](https://github.com/chrislambert-ky)
- **X.com**: [@ChrisLambertKY](https://x.com/ChrisLambertKY)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**About the Developer**: IT Project Manager, Data Analyst, Python ETL Developer, SQL Developer (Google BigQuery, Oracle), BI Dashboard Developer (Looker Studio, Tableau, PowerBI), and Investment Strategy Enthusiast.