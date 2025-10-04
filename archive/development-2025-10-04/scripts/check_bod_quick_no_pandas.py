import csv

HIST='c:\\Apps\\gh\\analysis-stockmarket\\data\\history_tickers.csv'
V2='c:\\Apps\\gh\\analysis-stockmarket\\data\\all_buy_on_dip.csv'
LEVEL_MIN=5

# simulate >=5% events from history
sim_keys=set()
with open(HIST,newline='',encoding='utf-8') as f:
    r=csv.DictReader(f)
    prev_by_symbol={}
    for row in r:
        sym=row.get('Symbol')
        date=row.get('Date_add') or row.get('Date')
        if not sym or not date: continue
        prev = None
        try:
            prev = float(row.get('Previous_Close')) if row.get('Previous_Close') not in (None,'') else None
        except:
            prev=None
        low = None
        try:
            low = float(row.get('Low')) if row.get('Low') not in (None,'') else None
        except:
            low=None
        # sometimes Previous_Close missing; try using last seen Close for this symbol
        if prev is None and sym in prev_by_symbol:
            prev = prev_by_symbol[sym]
        # update last seen close for next row
        try:
            last_close = float(row.get('Close')) if row.get('Close') not in (None,'') else None
        except:
            last_close=None
        if last_close is not None:
            prev_by_symbol[sym]=last_close
        if prev is None or low is None or prev==0:
            continue
        for level in range(LEVEL_MIN,6):
            limit = prev*(1-level/100.0)
            if low <= limit:
                sim_keys.add(f"{sym}|{date}|{level}")

# count v2 >=5%
v2_keys=set()
with open(V2,newline='',encoding='utf-8') as f:
    r=csv.DictReader(f)
    for row in r:
        try:
            level_str = row.get('Buy_Level') or row.get('Buy Level') or ''
            # strip percent sign
            level = int(str(level_str).replace('%','').strip()) if level_str not in (None,'') else None
        except:
            level=None
        if level is None: continue
        if level>=LEVEL_MIN:
            date=row.get('Date_add') or row.get('Date')
            sym=row.get('Symbol')
            if not date or not sym: continue
            v2_keys.add(f"{sym}|{date}|{level}")

print('simulated >=5% events:', len(sim_keys))
print('v2 >=5% events:', len(v2_keys))
print('matched:', len(sim_keys & v2_keys))
print('only_sim:', len(sim_keys - v2_keys))
print('only_v2:', len(v2_keys - sim_keys))
