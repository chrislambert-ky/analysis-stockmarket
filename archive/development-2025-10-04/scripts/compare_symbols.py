import pandas as pd

HIST='data/history_tickers.csv'
HIST_V2='data/history_tickers_v2.csv'
SYMBOLS=['SPLG','QQQ']

print('Loading files...')
df1 = pd.read_csv(HIST, dtype=str)
df2 = pd.read_csv(HIST_V2, dtype=str)

# normalize Date column
for df in (df1, df2):
    if 'Date' in df.columns:
        df['Date'] = df['Date'].astype(str)
    elif 'Date_add' in df.columns:
        df['Date'] = df['Date_add'].astype(str)

num_cols = ['Open','High','Low','Close','Previous_Close','avg_daily_price']

for s in SYMBOLS:
    print('\n' + '='*40)
    print(f'Comparing symbol: {s}')
    s1 = df1[df1['Symbol']==s].copy()
    s2 = df2[df2['Symbol']==s].copy()
    print(f'Rows: original {len(s1)}, v2 {len(s2)}')
    if s1.empty and s2.empty:
        print('Both empty; skipping')
        continue

    set1 = set(s1['Date'].astype(str))
    set2 = set(s2['Date'].astype(str))
    common = sorted(list(set1 & set2))
    only1 = sorted(list(set1 - set2))
    only2 = sorted(list(set2 - set1))
    print(f'Common dates: {len(common)}; only in original: {len(only1)}; only in v2: {len(only2)}')

    # parse numeric
    for c in num_cols:
        for df in (s1,s2):
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce')
            else:
                df[c] = pd.NA

    if len(common)==0:
        continue

    m1 = s1.set_index('Date')
    m2 = s2.set_index('Date')
    merged = m1.join(m2, lsuffix='_orig', rsuffix='_v2', how='inner')

    diffs = {}
    for c in num_cols:
        a = f'{c}_orig'
        b = f'{c}_v2'
        if a in merged.columns and b in merged.columns:
            merged['diff_'+c] = (merged[b] - merged[a]).abs()
            diffs[c] = {
                'max_abs_diff': merged['diff_'+c].max(),
                'mean_abs_diff': merged['diff_'+c].mean(),
            }

    print('\nNumeric diffs on common dates:')
    for c,stats in diffs.items():
        print(f" {c}: max_abs_diff={stats['max_abs_diff']}, mean_abs_diff={stats['mean_abs_diff']}")

    # show first mismatches if any
    mask = False
    for c in num_cols:
        if 'diff_'+c in merged.columns:
            mask = mask | (merged['diff_'+c] != 0)
    sample = merged[mask].head(10)
    if sample.empty:
        print('No material numeric differences found on common dates.')
    else:
        print('\nSample mismatches (up to 10 rows):')
        cols_show = []
        for c in num_cols:
            cols_show += [c+'_orig', c+'_v2', 'diff_'+c]
        print(sample[cols_show].head(10).to_string())

print('\nDone.')
