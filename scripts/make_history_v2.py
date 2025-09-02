import pandas as pd

PROC='data/etl-data-proc.csv'
OUT='data/history_tickers_v2.csv'

print('Loading', PROC)
df = pd.read_csv(PROC, dtype=str)
# ensure expected columns exist
# PROC has: Date,Open,High,Low,Close,Volume,Symbol,Year,Month,Week,Weekday,avg_daily_price,Previous_Close,...
# Target legacy schema:
cols = [
    'Date_add','Weekday','Symbol','Open','High','Low','Close','Previous_Close','Daily_Gain_Loss_Pct',
    'Open_vs_PrevClose_Pct','Low_vs_PrevClose_Pct','Close_vs_PrevClose_Pct','mx_percent_decline',
    'Date','Volume','Dividends','Stock Splits','Capital Gains','Year','Month','Week','avg_daily_price'
]

# Prepare output df
out = pd.DataFrame()
# Date_add = Date
out['Date_add'] = df.get('Date', '')
# Weekday prefer existing Weekday column
out['Weekday'] = df.get('Weekday', '')
out['Symbol'] = df.get('Symbol', '')
out['Open'] = df.get('Open', '')
out['High'] = df.get('High', '')
out['Low'] = df.get('Low', '')
out['Close'] = df.get('Close', '')
out['Previous_Close'] = df.get('Previous_Close', '')
out['Daily_Gain_Loss_Pct'] = df.get('Daily_Gain_Loss_Pct', '')
out['Open_vs_PrevClose_Pct'] = df.get('Open_vs_PrevClose_Pct', '')
out['Low_vs_PrevClose_Pct'] = df.get('Low_vs_PrevClose_Pct', '')
out['Close_vs_PrevClose_Pct'] = df.get('Close_vs_PrevClose_Pct', '')
out['mx_percent_decline'] = df.get('mx_percent_decline', '')
out['Date'] = df.get('Date', '')
out['Volume'] = df.get('Volume', '')
# Legacy columns not present in proc: fill with zeros
out['Dividends'] = 0.0
out['Stock Splits'] = 0.0
out['Capital Gains'] = 0.0
out['Year'] = df.get('Year', '')
out['Month'] = df.get('Month', '')
out['Week'] = df.get('Week', '')
out['avg_daily_price'] = df.get('avg_daily_price', '')

print('Writing', OUT)
out.to_csv(OUT, index=False)
print('Wrote', OUT, 'rows', len(out))
