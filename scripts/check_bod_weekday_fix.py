import csv
from datetime import datetime

path = r"c:\Apps\gh\analysis-stockmarket\all_buy_on_dip_TQQQ (1).csv"

with open(path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    seen = {}
    for row in reader:
        d = row.get('Date_add') or row.get('Date')
        if not d: continue
        # normalize YYYY-MM-DD or fallback
        try:
            if '-' in d and len(d.split('-')[0])==4:
                dt = datetime.strptime(d, '%Y-%m-%d')
            else:
                dt = datetime.strptime(d, '%m/%d/%Y')
        except Exception:
            try:
                dt = datetime.fromisoformat(d)
            except Exception:
                continue
        wd = dt.strftime('%A')
        if d not in seen:
            seen[d] = wd

for k in sorted(seen.keys()):
    print(k, seen[k])
