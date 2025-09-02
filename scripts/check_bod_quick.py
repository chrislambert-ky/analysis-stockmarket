import pandas as pd
HIST='data/history_tickers.csv'
V2='data/all_buy_on_dip.csv'
LEVEL_MIN=5

h=pd.read_csv(HIST)
v=pd.read_csv(V2)
print('hist rows',len(h),'v2 rows',len(v))
if 'Date' not in h.columns and 'Date_add' in h.columns:
    h['Date']=h['Date_add']
h['Date']=h['Date'].astype(str)
if 'Previous_Close' not in h.columns or h['Previous_Close'].isna().all():
    h['Close']=pd.to_numeric(h['Close'],errors='coerce')
    h=h.sort_values(['Symbol','Date'])
    h['Previous_Close']=h.groupby('Symbol')['Close'].shift(1)
h['Low']=pd.to_numeric(h['Low'],errors='coerce')

sim=0
for sym,g in h.groupby('Symbol'):
    for _,r in g.iterrows():
        prev=r['Previous_Close']
        low=r['Low']
        if pd.isna(prev) or pd.isna(low) or prev==0:
            continue
        for level in range(LEVEL_MIN,31):
            limit=prev*(1-level/100.0)
            if low<=limit:
                sim+=1

print('simulated events >=5%:',sim)
# v2 filtered
v2=v.copy()
if 'Buy_Level' in v2.columns:
    v2['Buy_Level']=pd.to_numeric(v2['Buy_Level'],errors='coerce')
v2f=v2[v2['Buy_Level']>=LEVEL_MIN]
print('v2 events >=5%:',len(v2f))

# build keys
sim_rows=[]
for sym,g in h.groupby('Symbol'):
    for _,r in g.iterrows():
        prev=r['Previous_Close']
        low=r['Low']
        if pd.isna(prev) or pd.isna(low) or prev==0:
            continue
        for level in range(LEVEL_MIN,31):
            limit=prev*(1-level/100.0)
            if low<=limit:
                sim_rows.append(f"{sym}|{r['Date']}|{level}")

sim_keys=set(sim_rows)
v2_keys=set(v2f['Symbol'].astype(str)+'|'+v2f['Date'].astype(str)+'|'+v2f['Buy_Level'].astype(int).astype(str))
print('sim keys',len(sim_keys),'v2 keys',len(v2_keys))
print('matched',len(sim_keys & v2_keys))
