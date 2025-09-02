import pandas as pd
import numpy as np

HIST='data/history_tickers.csv'
V2='data/all_buy_on_dip.csv'
SYMS=['SPLG','QQQ']
LEVEL_MIN=5
LEVEL_MAX=30

print('Loading files...')
dfh = pd.read_csv(HIST)
dfv = pd.read_csv(V2)

# normalize Date
if 'Date' not in dfh.columns and 'Date_add' in dfh.columns:
    dfh['Date']=dfh['Date_add']
dfh['Date']=dfh['Date'].astype(str)

if 'Date' not in dfv.columns and 'Date_add' in dfv.columns:
    dfv['Date']=dfv['Date_add']
dfv['Date']=dfv['Date'].astype(str)

# ensure Previous_Close
if 'Previous_Close' not in dfh.columns or dfh['Previous_Close'].isna().all():
    dfh['Close']=pd.to_numeric(dfh['Close'],errors='coerce')
    dfh = dfh.sort_values(['Symbol','Date'])
    dfh['Previous_Close'] = dfh.groupby('Symbol')['Close'].shift(1)

# numeric
dfh['Low'] = pd.to_numeric(dfh['Low'],errors='coerce')
dfh['Previous_Close'] = pd.to_numeric(dfh['Previous_Close'],errors='coerce')

def simulate_for_symbol(sym):
    g = dfh[dfh['Symbol']==sym].sort_values('Date')
    rows=[]
    for _,r in g.iterrows():
        prev = r['Previous_Close']
        if pd.isna(prev) or prev==0:
            continue
        low = r['Low']
        if pd.isna(low):
            continue
        for lvl in range(LEVEL_MIN, LEVEL_MAX+1):
            limit = prev*(1 - lvl/100.0)
            if low <= limit:
                rows.append({'Symbol':sym,'Date':r['Date'],'Buy_Level':lvl,'Executed_Price':round(limit,4),'Shares_Purchased':1,'Dollars_Invested':round(limit*1,4)})
    return pd.DataFrame(rows)

print('\nTotals per symbol:')
for sym in SYMS:
    sim = simulate_for_symbol(sym)
    sim_total_events = len(sim)
    sim_total_shares = sim['Shares_Purchased'].sum() if sim_total_events>0 else 0
    sim_total_invested = sim['Dollars_Invested'].sum() if sim_total_events>0 else 0.0

    v2s = dfv[dfv['Symbol']==sym].copy()
    # pick only Buy_Level >= LEVEL_MIN
    v2s['Buy_Level'] = pd.to_numeric(v2s['Buy_Level'],errors='coerce')
    v2s = v2s[v2s['Buy_Level'].notna() & (v2s['Buy_Level']>=LEVEL_MIN)]
    v2_total_events = len(v2s)
    # Shares Purchased field may be named 'Shares Purchased' or 'Shares_Purchased'
    if 'Shares Purchased' in v2s.columns:
        v2_shares = v2s['Shares Purchased'].fillna(0).astype(float).sum()
    elif 'Shares_Purchased' in v2s.columns:
        v2_shares = v2s['Shares_Purchased'].fillna(0).astype(float).sum()
    else:
        v2_shares = v2_total_events  # fallback; ETL used 1 share per event
    # Dollars invested field
    if 'Dollars Invested' in v2s.columns:
        v2_invested = v2s['Dollars Invested'].fillna(0).astype(float).sum()
    elif 'Dollars_Invested' in v2s.columns:
        v2_invested = v2s['Dollars_Invested'].fillna(0).astype(float).sum()
    else:
        v2_invested = 0.0

    # compare
    shares_match = (sim_total_shares == v2_shares)
    invested_diff = abs(sim_total_invested - v2_invested)
    invested_pct_diff = (invested_diff / sim_total_invested * 100) if sim_total_invested else 0.0

    print(f"\n{sym}:")
    print(f" sim events={sim_total_events}, sim shares={sim_total_shares}, sim invested={sim_total_invested:.4f}")
    print(f" v2 events={v2_total_events}, v2 shares={v2_shares}, v2 invested={v2_invested:.4f}")
    print(f" shares identical: {shares_match}")
    print(f" invested diff: {invested_diff:.4f} ({invested_pct_diff:.4f}%)")

print('\nDone.')
