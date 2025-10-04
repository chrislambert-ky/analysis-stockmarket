import pandas as pd

BOD='data/all_buy_on_dip.csv'
print('Loading', BOD)
df = pd.read_csv(BOD)
# normalize columns
for c in ['Shares_Purchased','Shares Purchased']:
    if c in df.columns:
        df['Shares'] = pd.to_numeric(df[c], errors='coerce')
        break
else:
    df['Shares'] = 1

for c in ['Executed_Price','Executed_Price']:
    if c in df.columns:
        df['Exec_Price'] = pd.to_numeric(df.get('Executed_Price'), errors='coerce')
        break

for c in ['Dollars_Invested','Dollars Invested']:
    if c in df.columns:
        df['Invested'] = pd.to_numeric(df[c], errors='coerce')
        break

# fallback: if Invested missing, compute Exec_Price * Shares
mask = df['Invested'].isna() & df['Exec_Price'].notna() & df['Shares'].notna()
if mask.any():
    df.loc[mask, 'Invested'] = (df.loc[mask, 'Exec_Price'] * df.loc[mask, 'Shares']).round(4)

summary = df.groupby('Symbol').agg(
    events=('Date', 'count'),
    total_shares=('Shares', 'sum'),
    total_invested=('Invested', 'sum'),
    mean_exec_price=('Exec_Price', 'mean'),
    weighted_avg_price=('Exec_Price', lambda x: (x * df.loc[x.index, 'Shares']).sum() / df.loc[x.index, 'Shares'].sum() if df.loc[x.index, 'Shares'].sum() else float('nan'))
).reset_index()

# format
summary['total_shares'] = summary['total_shares'].astype(int)
summary['total_invested'] = summary['total_invested'].round(4)
summary['mean_exec_price'] = summary['mean_exec_price'].round(4)
summary['weighted_avg_price'] = summary['weighted_avg_price'].round(4)

print('\nBOD aggregates (v2):')
print(summary.to_string(index=False))

# totals
tot_events = int(df['Date'].count())
tot_shares = int(df['Shares'].sum())
tot_invested = float(df['Invested'].sum())
print(f"\nTotals: events={tot_events}, shares={tot_shares}, invested={round(tot_invested,4)}")
