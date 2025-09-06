import csv
from datetime import datetime
import re

path = r"c:\Apps\gh\analysis-stockmarket\all_buy_on_dip_TQQQ (1).csv"

def parse_local_date(s):
    s = (s or '').strip()
    if not s:
        return None
    m = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})$', s)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r'^(\d{1,2})\/(\d{1,2})\/(\d{4})$', s)
    if m:
        return datetime(int(m.group(3)), int(m.group(1)), int(m.group(2)))
    try:
        dt = datetime.fromisoformat(s)
        return datetime(dt.year, dt.month, dt.day)
    except Exception:
        try:
            dt = datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
            return datetime(dt.year, dt.month, dt.day)
        except Exception:
            return None

mismatches = []
rows_total = 0
with open(path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows_total += 1
        date_str = row.get('Date_add') or row.get('Date')
        csv_weekday = (row.get('Weekday') or '').strip()
        dt = parse_local_date(date_str)
        if not dt:
            continue
        computed = dt.strftime('%A')
        if csv_weekday != computed:
            mismatches.append((date_str, csv_weekday, computed, row))

print(f"Total rows checked: {rows_total}")
print(f"Mismatches: {len(mismatches)}")
for i, (date_str, csv_wd, comp_wd, row) in enumerate(mismatches[:30], 1):
    print(f"{i}. {date_str}: CSV='{csv_wd}'  computed='{comp_wd}'")

if len(mismatches) > 0:
    print('\nSample full row of first mismatch:')
    import json
    print(json.dumps(mismatches[0][3], indent=2))
