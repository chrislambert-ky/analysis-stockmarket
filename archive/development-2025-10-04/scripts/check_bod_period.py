import csv
from datetime import datetime

csv_path = r"c:\Apps\gh\analysis-stockmarket\data\all_buy_on_dip.csv"
symbol = 'FBCG'
start = '2025-01-01'
end = '2025-09-01'

rows = []
with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        if (r.get('Symbol') or '') != symbol:
            continue
        date = (r.get('Date_add') or r.get('Date') or '').strip()
        if not date:
            continue
        if date < start or date > end:
            continue
        # Robust numeric parsing
        try:
            shares = float(r.get('Shares Purchased') or r.get('Shares Purchased') or 1)
        except:
            shares = 1.0
        try:
            invested = float(r.get('Dollars Invested') or r.get('Dollars Invested') or r.get('Buy_Price') or 0)
        except:
            invested = 0.0
        close = None
        try:
            c = r.get('Close')
            if c and c.strip() != '':
                close = float(c)
        except:
            close = None
        rows.append((date, shares, invested, close))

rows.sort()

cum_shares = 0.0
cum_invested = 0.0
last_close = None
print(f"Found {len(rows)} BOD rows for {symbol} between {start} and {end}")
print("\nPer-date details and running totals:")
print("Date\tShares\tInvested\tClose\tCumShares\tCumInvested\tValue (CumShares*Close)")
for date, shares, invested, close in rows:
    cum_shares += shares
    cum_invested += invested
    if close is not None:
        last_close = close
    value = (cum_shares * last_close) if last_close is not None else None
    print(f"{date}\t{shares}\t{invested:.2f}\t{close if close is not None else 'NA'}\t{cum_shares}\t{cum_invested:.2f}\t{value if value is not None else 'NA'}")

print('\nFinal YTD totals:')
print(f"CumShares = {cum_shares}")
print(f"CumInvested = ${cum_invested:.2f}")
if last_close is not None:
    print(f"LastCloseInPeriod = {last_close}")
    print(f"CumValue = ${cum_shares * last_close:.2f}")
else:
    print("No Close available in period to compute value.")
