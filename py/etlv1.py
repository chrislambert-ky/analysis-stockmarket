import os
import yfinance as yf 
import pandas as pd
import openpyxl
import datetime as dt

# Ensure /data folder exists
output_folder = "data"
os.makedirs(output_folder, exist_ok=True)

etf_list = [
    "ALLY",
    "FBCG",
    "FMAG",
    "GGLL",
    "GOOGL",
    "HSBC",
    "MGK",
    "MSFT",
    "MSFU",
    "OEF",
    "QLD",
    "QQQ",
    "QQQM",
    "QQUP",
    "QQXL",
    "QTOP",
    "SPLG",
    "SPY",
    "SSO",
    "TQQQ",
    "TOPT",
    "UPRO",
    "VGT",
    "XLG"
]

for ticker_symbol in etf_list:
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="10y", interval="1d")
    df = pd.DataFrame(data)
    df.drop(['Dividends', 'Stock Splits', 'Volume'], axis=1, inplace=True)
    df.insert(0, 'Date_add', df.index)
    df.insert(1, 'Symbol', ticker_symbol)
    df['week_of_year'] = df.index.isocalendar().week
    df['week_day'] = df.index.day_name()
    df['avg_daily_price'] = df[['Open', 'High', 'Low', 'Close']].mean(axis=1)
    df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')
    df['Date_add'] = pd.to_datetime(df['Date_add']).dt.strftime('%Y-%m-%d')
    csv_name = os.path.join(output_folder, f'{ticker_symbol.lower()}.csv')
    df.to_csv(csv_name, index=False)

