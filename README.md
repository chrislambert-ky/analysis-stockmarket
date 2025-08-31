# Stock Market Analysis Toolkit

**Interactive tools for analyzing Dollar Cost Averaging and Buy-on-Dip investment strategies**

*This project provides interactive tools for analyzing investment strategies including Dollar Cost Averaging and Buy-on-Dip approaches. It includes various calculators and visualizations to help users understand different investment methodologies and their historical performance.*

## 🚀 Live Demo

[View the interactive analysis tools here](https://chrislambert-ky.github.io/analysis-stockmarket/) *(Update this URL when deployed)*

## 📊 Investment Strategies Analyzed

### Dollar Cost Averaging (DCA)
- **Method**: Regular periodic investments of fixed dollar amounts regardless of market conditions
- **Default Strategy**: Invests $25 weekly
- **Benefits**: Reduces impact of market volatility through consistent investing

### Buy-on-Dip (BOD)
- **Method**: Purchase shares when stock price declines by specified percentages
- **Default Strategy**: Buys 1 share per 1-5% decline
- **Benefits**: Capitalizes on market downturns and temporary price reductions

### Strategy Comparison
- Side-by-side analysis of DCA vs BOD performance across different tickers and timeframes
- Interactive visualizations showing portfolio growth patterns
- Historical backtesting across multiple market conditions

## 🛠️ Features

- **Multi-Ticker Analysis**: Compare strategy performance across multiple ETFs (QQQ, SPLG, XLG) simultaneously
- **Advanced Calculators**: Customizable tools allowing users to test their own investment amounts, frequencies, and trigger conditions
- **Interactive Charts**: ECharts-powered visualizations showing portfolio growth, purchase timing, and strategy comparisons
- **CSV Export**: Download detailed transaction history for further analysis
- **Responsive Design**: Mobile-friendly interface that works across all device types

## 🔧 Technical Implementation

### Data Processing
- **Python ETL Pipeline**: Uses pandas and yfinance for historical data collection and CSV generation
- **Data Source**: Yahoo Finance historical price data via yfinance Python library
- **Analysis Period**: Configurable date ranges with focus on multi-year performance comparisons

### Frontend Framework
- **HTML/CSS/JavaScript**: Responsive design with professional styling
- **ECharts Library**: Interactive visualizations and chart components
- **Calculation Engine**: JavaScript-based portfolio calculations with precise currency formatting and trade tracking
- **Analytics Integration**: Google Analytics tracking for usage insights and performance monitoring

## 📁 Project Structure

```
analysis-stockmarket/
├── css/                    # Stylesheets
│   ├── style.css          # Main stylesheet
│   └── about.css          # About page styling
├── data/                  # CSV data files
├── js/                    # JavaScript utilities
├── pages/                 # Analysis pages
│   ├── dca.html          # Dollar Cost Averaging analysis
│   ├── bod.html          # Buy-on-Dip analysis
│   ├── dca-tickers.html  # DCA all tickers comparison
│   ├── bod-tickers.html  # BOD all tickers comparison
│   ├── dca-strat.html    # Advanced DCA calculator
│   ├── bod-strat.html    # Advanced BOD calculator
│   └── about.html        # About page
├── py/                   # Python ETL scripts
├── etl-market-data.py    # Main data collection script
├── index.html            # Homepage
└── requirements.txt      # Python dependencies
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

## 💾 Data Sources and Methodology

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