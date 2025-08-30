# Added Excel file formats

import os
import yfinance as yf
import pandas as pd

# =============================
# CONFIGURATION
# =============================
output_folder = "data"
os.makedirs(output_folder, exist_ok=True)

etf_list = ["TQQQ","UPRO"]

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

    purchases['Strategy'] = 'DCA_Monthly'
    purchases['Buy_Price'] = purchases['avg_daily_price']
    purchases['Buy_Level'] = 'DCA'
    purchases['Shares Purchased'] = (monthly_investment / purchases['avg_daily_price']).round(6)
    purchases['Dollars Invested'] = monthly_investment
    purchases['Cumulative Shares'] = purchases['Shares Purchased'].cumsum()
    purchases['Cumulative Invested'] = purchases['Dollars Invested'].cumsum()
    purchases['Cumulative Value'] = (purchases['Cumulative Shares'] * purchases['Close']).round(2)
    purchases['Weekday'] = pd.to_datetime(purchases['Date_add']).dt.day_name()

    # Select and order columns for consistency
    return purchases[['Date_add', 'Weekday', 'Symbol', 'Strategy', 'Buy_Price', 'Buy_Level', 'Shares Purchased', 'Dollars Invested', 'Cumulative Shares', 'Cumulative Invested', 'Cumulative Value', 'Close']]


def transform_weekly(df):
    """Generate weekly DCA purchase history at $25/week."""
    first_trading_days = df.groupby(['Year', 'Week']).first().reset_index()

    purchases = first_trading_days[[
        'Date_add', 'Symbol', 'Open', 'High', 'Low', 'Close',
        'week_of_year', 'week_day', 'avg_daily_price'
    ]].copy()

    purchases['Strategy'] = 'DCA_Weekly'
    purchases['Buy_Price'] = purchases['avg_daily_price']
    purchases['Buy_Level'] = 'DCA'
    purchases['Shares Purchased'] = (weekly_investment / purchases['avg_daily_price']).round(6)
    purchases['Dollars Invested'] = weekly_investment
    purchases['Cumulative Shares'] = purchases['Shares Purchased'].cumsum()
    purchases['Cumulative Invested'] = purchases['Dollars Invested'].cumsum()
    purchases['Cumulative Value'] = (purchases['Cumulative Shares'] * purchases['Close']).round(2)
    purchases['Weekday'] = pd.to_datetime(purchases['Date_add']).dt.day_name()

    return purchases[['Date_add', 'Weekday', 'Symbol', 'Strategy', 'Buy_Price', 'Buy_Level', 'Shares Purchased', 'Dollars Invested', 'Cumulative Shares', 'Cumulative Invested', 'Cumulative Value', 'Close']]


# =============================
# TRANSFORM (BUY-ON-DIP)
# =============================
def transform_buy_on_dip(df):
    """Simulate Buy-on-Dip strategy (1 share per 1%-5% drop). Adds cumulative shares, invested, and value columns."""
    purchased_list = []

    for _, row in df.iterrows():
        open_price = row['Open']
        close_price = row['Close']
        low_price = row['Low']
        date = row['Date_add']
        weekday = pd.to_datetime(date).day_name()
        for level in sorted(dip_levels):  # Ensure buy levels are processed from smallest to largest
            target_price = open_price * level
            if low_price <= target_price:
                purchased_list.append({
                    'Date_add': date,
                    'Weekday': weekday,
                    'Symbol': row['Symbol'],
                    'Strategy': 'Buy_on_Dip',
                    'Buy_Price': round(target_price, 6),
                    'Buy_Level': f"{(1 - level) * 100:.0f}%",
                    'Shares Purchased': 1,
                    'Dollars Invested': round(target_price, 6),
                    'Close': close_price
                })

    if not purchased_list:
        return pd.DataFrame()

    df_bod = pd.DataFrame(purchased_list)
    df_bod = df_bod.sort_values(['Date_add', 'Buy_Level']).reset_index(drop=True)
    df_bod['Cumulative Shares'] = df_bod['Shares Purchased'].cumsum()
    df_bod['Cumulative Invested'] = df_bod['Dollars Invested'].cumsum()
    df_bod['Cumulative Value'] = (df_bod['Cumulative Shares'] * df_bod['Close']).round(2)
    return df_bod[['Date_add', 'Weekday', 'Symbol', 'Strategy', 'Buy_Price', 'Buy_Level', 'Shares Purchased', 'Dollars Invested', 'Cumulative Shares', 'Cumulative Invested', 'Cumulative Value', 'Close']]


# =============================
# LOAD
# =============================
def load_data(df, ticker_symbol, strategy):
    """Save purchase history to CSV and Excel."""
    if df.empty:
        return
    csv_name = os.path.join(output_folder, f"{ticker_symbol.lower()}_{strategy}.csv")
    xlsx_name = os.path.join(output_folder, f"{ticker_symbol.lower()}_{strategy}.xlsx")
    df.to_csv(csv_name, index=False)
    df.to_excel(xlsx_name, index=False)
    print(f"Saved {strategy} history for {ticker_symbol} → {csv_name} and {xlsx_name}")


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

    # Save complete history for each ticker, with Weekday column and formatted date
    if not df.empty:
        df['Weekday'] = pd.to_datetime(df['Date_add']).dt.day_name()
        df['Date_add'] = pd.to_datetime(df['Date_add']).dt.strftime('%Y-%m-%d')
        if 'Date' in df.columns:
            df = df.drop(columns=['Date'])
        col_order = ['Date_add', 'Weekday', 'Symbol'] + [col for col in df.columns if col not in ['Date_add', 'Weekday', 'Symbol']]
        df = df[col_order]
        csv_name = os.path.join(output_folder, f"{ticker_symbol.lower()}_full_history.csv")
        xlsx_name = os.path.join(output_folder, f"{ticker_symbol.lower()}_full_history.xlsx")
        df.to_csv(csv_name, index=False)
        df.to_excel(xlsx_name, index=False)
        print(f"Saved full history for {ticker_symbol} → {csv_name} and {xlsx_name}")
