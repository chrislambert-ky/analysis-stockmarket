import os
import yfinance as yf
import pandas as pd

# =============================
# CONFIGURATION
# =============================
output_folder = "data"
os.makedirs(output_folder, exist_ok=True)

etf_list = [
    "ALLY", "FBCG", "FMAG", "GGLL", "GOOGL", "HSBC", "MGK", "MSFT", "MSFU",
    "OEF", "QLD", "QQQ", "QQQM", "QQUP", "QQXL", "QTOP", "SPLG", "SPY",
    "SSO", "TQQQ", "TOPT", "UPRO", "VGT", "XLG"
]

monthly_investment = 100.0
weekly_investment = 25.0


# =============================
# EXTRACT
# =============================
def extract_data(ticker_symbol):
    """Pull 10 years of daily historical data from Yahoo Finance and enrich with fields."""
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="10y", interval="1d")

    if data.empty:
        return pd.DataFrame()

    df = data.copy()
    df.reset_index(inplace=True)

    # Keep only OHLC
    df = df.drop(['Dividends', 'Stock Splits', 'Volume'], axis=1)

    # Add enrichment
    df['Date_add'] = df['Date'].dt.strftime('%Y-%m-%d')
    df['Symbol'] = ticker_symbol
    df['week_of_year'] = df['Date'].dt.isocalendar().week
    df['week_day'] = df['Date'].dt.day_name()
    df['avg_daily_price'] = df[['Open', 'High', 'Low', 'Close']].mean(axis=1)
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Week'] = df['Date'].dt.isocalendar().week

    return df


# =============================
# TRANSFORM
# =============================
def transform_monthly(df):
    """Generate monthly DCA purchase history at $100/month."""
    first_trading_days = df.groupby(['Year', 'Month']).first().reset_index()

    purchases = first_trading_days[[
        'Date_add', 'Symbol', 'Open', 'High', 'Low', 'Close',
        'week_of_year', 'week_day', 'avg_daily_price'
    ]].copy()

    purchases['Dollars Invested'] = monthly_investment
    purchases['Shares Purchased'] = purchases['Dollars Invested'] / purchases['avg_daily_price']

    # Round
    for col in ['Open', 'High', 'Low', 'Close', 'avg_daily_price']:
        purchases[col] = purchases[col].round(6)
    purchases['Shares Purchased'] = purchases['Shares Purchased'].round(6)

    return purchases


def transform_weekly(df):
    """Generate weekly DCA purchase history at $25/week."""
    first_trading_days = df.groupby(['Year', 'Week']).first().reset_index()

    purchases = first_trading_days[[
        'Date_add', 'Symbol', 'Open', 'High', 'Low', 'Close',
        'week_of_year', 'week_day', 'avg_daily_price'
    ]].copy()

    purchases['Dollars Invested'] = weekly_investment
    purchases['Shares Purchased'] = purchases['Dollars Invested'] / purchases['avg_daily_price']

    # Round
    for col in ['Open', 'High', 'Low', 'Close', 'avg_daily_price']:
        purchases[col] = purchases[col].round(6)
    purchases['Shares Purchased'] = purchases['Shares Purchased'].round(6)

    return purchases


# =============================
# LOAD
# =============================
def load_data(df, ticker_symbol, suffix):
    """Save DataFrame to CSV."""
    csv_name = os.path.join(output_folder, f"{ticker_symbol.lower()}_{suffix}.csv")
    df.to_csv(csv_name, index=False)
    print(f"Saved {suffix} data for {ticker_symbol} → {csv_name}")


# =============================
# MAIN ETL LOOP
# =============================
for ticker_symbol in etf_list:
    df = extract_data(ticker_symbol)

    if df.empty:
        print(f"No data found for {ticker_symbol}, skipping...")
        continue

    # Daily history
    load_data(df, ticker_symbol, "history")

    # Monthly DCA
    monthly_df = transform_monthly(df)
    load_data(monthly_df, ticker_symbol, "dca_monthly")

    # Weekly DCA
    weekly_df = transform_weekly(df)
    load_data(weekly_df, ticker_symbol, "dca_weekly")
