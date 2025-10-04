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

dip_levels = [0.99, 0.98, 0.97, 0.96, 0.95]  # 1% → 5% dips


# =============================
# EXTRACT
# =============================
def extract_data(ticker_symbol):
    """Pull 10 years of daily historical data from Yahoo Finance."""
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="10y", interval="1d")

    if data.empty:
        return pd.DataFrame()

    df = data.copy()
    df.reset_index(inplace=True)
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
# TRANSFORM (DCA)
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

    # Round for neatness
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

    # Round for neatness
    for col in ['Open', 'High', 'Low', 'Close', 'avg_daily_price']:
        purchases[col] = purchases[col].round(6)
    purchases['Shares Purchased'] = purchases['Shares Purchased'].round(6)

    return purchases


# =============================
# TRANSFORM (BUY-ON-DIP)
# =============================
def transform_buy_on_dip(df):
    """Simulate Buy-on-Dip strategy (1 share per 1%-5% drop)."""
    purchased_list = []

    for _, row in df.iterrows():
        open_price = row['Open']
        low_price = row['Low']

        for level in dip_levels:
            target_price = open_price * level
            if low_price <= target_price:
                purchased_list.append({
                    'Date': row['Date_add'],
                    'Symbol': row['Symbol'],
                    'Buy_Price': round(target_price, 6),
                    'Buy_Level': f"{(1 - level) * 100:.0f}%",
                    'Shares Purchased': 1,
                    'Dollars Invested': round(target_price, 6)  # cost of 1 share
                })

    if not purchased_list:
        return pd.DataFrame()

    bod_df = pd.DataFrame(purchased_list)

    # Compute cumulative stats
    bod_df['Cumulative Shares'] = bod_df['Shares Purchased'].cumsum()
    bod_df['Cumulative Dollars Invested'] = bod_df['Dollars Invested'].cumsum()

    return bod_df


# =============================
# LOAD
# =============================
def load_data(df, ticker_symbol, strategy):
    """Save purchase history to CSV."""
    if df.empty:
        return
    csv_name = os.path.join(output_folder, f"{ticker_symbol.lower()}_{strategy}.csv")
    df.to_csv(csv_name, index=False)
    print(f"Saved {strategy} history for {ticker_symbol} → {csv_name}")


# =============================
# MAIN ETL LOOP
# =============================
for ticker_symbol in etf_list:
    df = extract_data(ticker_symbol)

    if df.empty:
        print(f"No data found for {ticker_symbol}, skipping...")
        continue

    # DCA strategies
    monthly_df = transform_monthly(df)
    weekly_df = transform_weekly(df)

    # Buy-on-Dip strategy
    bod_df = transform_buy_on_dip(df)

    # Save results
    load_data(monthly_df, ticker_symbol, "dca_monthly")
    load_data(weekly_df, ticker_symbol, "dca_weekly")
    load_data(bod_df, ticker_symbol, "buy_on_dip")
