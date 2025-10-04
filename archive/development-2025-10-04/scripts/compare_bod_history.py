import pandas as pd

BOD='data/all_buy_on_dip.csv'
PROC='data/etl-data-proc.csv'
HIST='data/history_tickers.csv'

print('Reading files...')
df_bod = pd.read_csv(BOD)
df_proc = pd.read_csv(PROC)
df_hist = pd.read_csv(HIST)

print('\nHeaders:')
print('all_buy_on_dip.csv:', list(df_bod.columns))
print('etl-data-proc.csv:', list(df_proc.columns))
print('history_tickers.csv:', list(df_hist.columns))

# Symbols
sym_bod = set(df_bod['Symbol'].dropna().unique())
sym_proc = set(df_proc['Symbol'].dropna().unique())
sym_hist = set(df_hist['Symbol'].dropna().unique())

print(f'\nCounts: rows BOD={len(df_bod)} proc={len(df_proc)} hist={len(df_hist)}')
print(f'Symbols: BOD({len(sym_bod)}), PROC({len(sym_proc)}), HIST({len(sym_hist)})')

print('\nSymbols present in BOD but not in history:')
print(sorted(sym_bod - sym_hist)[:50])
print('\nSymbols present in history but not in BOD:')
print(sorted(sym_hist - sym_bod)[:50])

# Per-symbol counts in BOD
print('\nTop per-symbol BOD counts:')
counts = df_bod['Symbol'].value_counts()
print(counts.head(20).to_string())

# Check SPY and SPLG samples
for s in ['SPY','SPLG']:
    print(f'\nSample BOD rows for {s}:')
    sub = df_bod[df_bod['Symbol']==s]
    if sub.empty:
        print('  (no BOD rows)')
    else:
        print(sub.head(5).to_string(index=False))

    print(f'\nSample history rows for {s}:')
    hsub = df_hist[df_hist['Symbol']==s]
    if hsub.empty:
        print('  (no history rows)')
    else:
        print(hsub.head(5).to_string(index=False))

# Quick integrity: ensure BOD dates exist in history for same symbol
print('\nChecking BOD -> history date coverage (per symbol):')
missing = {}
for s in sorted(sym_bod):
    bod_dates = set(df_bod[df_bod['Symbol']==s]['Date'].astype(str))
    hist_dates = set(df_hist[df_hist['Symbol']==s]['Date'].astype(str))
    miss = len(bod_dates - hist_dates)
    if miss>0:
        missing[s]=miss

if not missing:
    print('All BOD dates found in history for all symbols.')
else:
    print('Symbols with BOD dates missing in history (symbol: missing_dates_count):')
    for k,v in missing.items():
        print(f'  {k}: {v}')

print('\nDone.')
