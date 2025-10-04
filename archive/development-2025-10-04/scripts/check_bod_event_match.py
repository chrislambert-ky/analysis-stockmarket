import pandas as pd
import math

# Config
HIST = 'data/history_tickers.csv'   # legacy
V2_BOD = 'data/all_buy_on_dip.csv'  # v2 events
LEVEL_MIN = 5
LEVEL_MAX = 30
LEVEL_STEP = 1

print('Loading legacy history:', HIST)
df_hist = pd.read_csv(HIST)
print('Loading v2 BOD events:', V2_BOD)
df_v2 = pd.read_csv(V2_BOD)
print('legacy rows=', len(df_hist), 'v2 rows=', len(df_v2))

# Normalize dates and numeric
for df in (df_hist, df_v2):
    if 'Date' not in df.columns and 'Date_add' in df.columns:
        df['Date'] = df['Date_add']
    df['Date'] = df['Date'].astype(str)

# Ensure Previous_Close exists in history; compute if missing
if 'Previous_Close' not in df_hist.columns or df_hist['Previous_Close'].isna().all():
    print('Computing Previous_Close from Close in legacy history')
    df_hist['Close'] = pd.to_numeric(df_hist['Close'], errors='coerce')
    df_hist = df_hist.sort_values(['Symbol','Date'])
    df_hist['Previous_Close'] = df_hist.groupby('Symbol')['Close'].shift(1)

# Ensure numeric Low and Previous_Close
df_hist['Low'] = pd.to_numeric(df_hist['Low'], errors='coerce')
df_hist['Previous_Close'] = pd.to_numeric(df_hist['Previous_Close'], errors='coerce')

# Simulate events from legacy history for levels >= LEVEL_MIN
sim_rows = []
levels = list(range(LEVEL_MIN, LEVEL_MAX+1, LEVEL_STEP))
for sym, g in df_hist.groupby('Symbol'):
    g = g.sort_values('Date')
    for _, r in g.iterrows():
        prev = r['Previous_Close']
        if pd.isna(prev) or prev == 0:
            continue
        low = r['Low']
        if pd.isna(low):
            continue
        for level in levels:
            limit = prev * (1 - level/100.0)
            if low <= limit:
                exec_price = round(limit,4)
                sim_rows.append({
                    'Date': r['Date'],
                    'Symbol': sym,
                    'Buy_Level': int(level),
                    'Executed_Price': exec_price,
                    'Close': round(r['Close'],4) if not pd.isna(r['Close']) else None,
                    'Previous_Close': round(prev,4)
                })

sim_df = pd.DataFrame(sim_rows)
print('\nSimulated events (legacy) with level>=%d: %d' % (LEVEL_MIN, len(sim_df)))

# Prepare v2 dataframe filtered to same levels
v2 = df_v2.copy()
# normalize Buy_Level to int
if 'Buy_Level' in v2.columns:
    v2['Buy_Level'] = pd.to_numeric(v2['Buy_Level'], errors='coerce').astype('Int64')
else:
    v2['Buy_Level'] = pd.NA
# normalize Executed_Price
if 'Executed_Price' in v2.columns:
    v2['Executed_Price'] = pd.to_numeric(v2['Executed_Price'], errors='coerce')
else:
    v2['Executed_Price'] = pd.NA

v2_filtered = v2[v2['Buy_Level'].notna() & (v2['Buy_Level'] >= LEVEL_MIN)].copy()
print('V2 BOD events with level>=%d: %d' % (LEVEL_MIN, len(v2_filtered)))

# Build keys for matching: Symbol, Date, Buy_Level
sim_df['key'] = sim_df['Symbol'].astype(str) + '|' + sim_df['Date'].astype(str) + '|' + sim_df['Buy_Level'].astype(str)
v2_filtered['key'] = v2_filtered['Symbol'].astype(str) + '|' + v2_filtered['Date'].astype(str) + '|' + v2_filtered['Buy_Level'].astype(str)

sim_keys = set(sim_df['key'])
v2_keys = set(v2_filtered['key'])

matched_keys = sim_keys & v2_keys
only_sim = sorted(sim_keys - v2_keys)
only_v2 = sorted(v2_keys - sim_keys)

print('\nMatch summary for levels >= %d:' % LEVEL_MIN)
print(' simulated events: %d' % len(sim_keys))
print(' v2 events:        %d' % len(v2_keys))
print(' matched keys:     %d' % len(matched_keys))
print(' only in sim:      %d' % len(only_sim))
print(' only in v2:       %d' % len(only_v2))

# Show sample mismatches
N = 10
print('\nSample events present in sim but not v2 (up to %d):' % N)
for k in only_sim[:N]:
    sym,date,lev = k.split('|')
    row = sim_df[sim_df['key']==k].iloc[0]
    print(f" {sym} {date} level={lev} exec={row['Executed_Price']}")

print('\nSample events present in v2 but not sim (up to %d):' % N)
for k in only_v2[:N]:
    sym,date,lev = k.split('|')
    row = v2_filtered[v2_filtered['key']==k].iloc[0]
    print(f" {sym} {date} level={lev} exec={round(row['Executed_Price'],4) if not pd.isna(row['Executed_Price']) else 'NA'}")

# For matched keys, compare executed price diffs
import numpy as np
if matched_keys:
    diffs = []
    for k in list(matched_keys)[:10000]:
        s,d,l = k.split('|')
        a = sim_df[(sim_df['Symbol']==s)&(sim_df['Date']==d)&(sim_df['Buy_Level']==int(l))].iloc[0]
        b = v2_filtered[(v2_filtered['Symbol']==s)&(v2_filtered['Date']==d)&(v2_filtered['Buy_Level']==int(l))].iloc[0]
        pa = float(a['Executed_Price'])
        pb = float(b['Executed_Price'])
        diffs.append(abs(pa-pb))
    diffs = np.array(diffs)
    print('\nExecuted price diffs for matched events:')
    print(' max diff:', diffs.max())
    print(' mean diff:', diffs.mean())
    print(' >0.0001 count:', (diffs>0.0001).sum())

# Per-symbol summary for SPLG and QQQ
for sym in ['SPLG','QQQ']:
    sim_count = sim_df[sim_df['Symbol']==sym].shape[0]
    v2_count = v2_filtered[v2_filtered['Symbol']==sym].shape[0]
    matched = len([k for k in matched_keys if k.startswith(sym+'|')])
    print(f"\n{sym}: sim={sim_count}, v2={v2_count}, matched={matched}, match_rate={(matched/sim_count*100) if sim_count else 0:.2f}%")

print('\nDone.')
