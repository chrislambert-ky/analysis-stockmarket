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
print('rows hist=',len(dfh),'v2=',len(dfv))

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
                rows.append({'Symbol':sym,'Date':r['Date'],'Buy_Level':lvl,'Executed_Price':round(limit,4)})
    return pd.DataFrame(rows)

# simulate and compare per symbol
report = {}
for sym in SYMS:
    print('\nProcessing', sym)
    sim = simulate_for_symbol(sym)
    print(' simulated events:', len(sim))
    # prepare v2 subset
    v2s = dfv[dfv['Symbol']==sym].copy()
    if 'Buy_Level' in v2s.columns:
        v2s['Buy_Level'] = pd.to_numeric(v2s['Buy_Level'],errors='coerce').astype('Int64')
    else:
        v2s['Buy_Level'] = pd.NA
    v2s = v2s[v2s['Buy_Level'].notna() & (v2s['Buy_Level']>=LEVEL_MIN)]
    print(' v2 events >=5%:', len(v2s))

    # build keys
    sim['key'] = sim['Symbol'] + '|' + sim['Date'].astype(str) + '|' + sim['Buy_Level'].astype(str)
    v2s['key'] = v2s['Symbol'].astype(str) + '|' + v2s['Date'].astype(str) + '|' + v2s['Buy_Level'].astype(str)

    sim_keys = set(sim['key'])
    v2_keys = set(v2s['key'])
    matched = sim_keys & v2_keys
    only_sim = sorted(sim_keys - v2_keys)
    only_v2 = sorted(v2_keys - sim_keys)

    print(' matched:', len(matched), 'only_sim:', len(only_sim), 'only_v2:', len(only_v2))

    # price diffs for matched
    diffs = []
    for k in list(matched):
        s,d,l = k.split('|')
        a = sim[(sim['Symbol']==s)&(sim['Date']==d)&(sim['Buy_Level']==int(l))].iloc[0]
        b = v2s[(v2s['Symbol']==s)&(v2s['Date']==d)&(v2s['Buy_Level']==int(l))].iloc[0]
        pa = float(a['Executed_Price'])
        pb = float(b['Executed_Price'])
        diffs.append(abs(pa-pb))
    diffs = np.array(diffs) if len(diffs)>0 else np.array([])
    print(' exec price diffs: max=', diffs.max() if diffs.size else 0, 'mean=', diffs.mean() if diffs.size else 0)

    # samples
    print('\nSample sim-only (up to 5):')
    for k in only_sim[:5]:
        s,d,l = k.split('|')
        row = sim[sim['key']==k].iloc[0]
        print(' ',s,d,'lvl',l,'exec',row['Executed_Price'])
    print('\nSample v2-only (up to 5):')
    for k in only_v2[:5]:
        s,d,l = k.split('|')
        row = v2s[v2s['key']==k].iloc[0]
        print(' ',s,d,'lvl',l,'exec',round(float(row['Executed_Price']),4) if not pd.isna(row['Executed_Price']) else 'NA')

    report[sym] = {'sim':len(sim),'v2':len(v2s),'matched':len(matched),'only_sim':len(only_sim),'only_v2':len(only_v2),'diff_max':float(diffs.max()) if diffs.size else 0,'diff_mean':float(diffs.mean()) if diffs.size else 0}

print('\nSummary:')
for k,v in report.items():
    print(k, v)

print('\nDone.')
