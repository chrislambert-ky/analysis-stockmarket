import csv
from datetime import datetime

HIST = r"c:\Apps\gh\analysis-stockmarket\data\history_tickers.csv"

PERIODS = {
    'YTD': ('2025-01-01', '2025-09-01'),
    '5Y': ('2020-09-02', '2025-09-01'),
    '10Y': ('2015-09-02', '2025-09-01')
}

SYMBOLS = ['SPLG', 'QQQ']


def load_history_for_symbol(symbol):
    rows = []
    with open(HIST, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if (r.get('Symbol') or '').strip() != symbol:
                continue
            date = (r.get('Date_add') or r.get('Date') or '').strip()
            if not date:
                continue
            # parse numeric fields safely
            def parse_num(k):
                v = r.get(k)
                if v is None or v == '':
                    return None
                try:
                    return float(v)
                except:
                    return None
            prev = parse_num('Previous_Close')
            # Some historical rows may have Previous_Close empty; use previous row's Close fallback later
            low = parse_num('Low')
            close = parse_num('Close')
            rows.append({'Date': date, 'Previous_Close': prev, 'Low': low, 'Close': close})
    rows.sort(key=lambda x: x['Date'])
    return rows


def simulate_events(rows, start_date, end_date):
    # filter by date range
    rows_in_range = [r for r in rows if start_date <= r['Date'] <= end_date]
    if not rows_in_range:
        return 0,0,0.0
    # Ensure we can use previous-close: iterate pairs
    events = 0
    cum_shares = 0
    cum_invested = 0.0
    # find index range relative to full rows to ensure previous day exists
    all_dates = [r['Date'] for r in rows]
    for i in range(1, len(rows)):
        date = rows[i]['Date']
        if date < start_date or date > end_date:
            continue
        today = rows[i]
        yesterday = rows[i-1]
        prev = yesterday['Close'] if (yesterday.get('Close') is not None) else yesterday.get('Previous_Close')
        low = today.get('Low')
        if prev is None or low is None:
            continue
        for level in range(1,6):
            limit = prev * (1 - level/100.0)
            if low <= limit:
                events += 1
                cum_shares += 1
                cum_invested += limit
    return events, cum_shares, cum_invested


if __name__ == '__main__':
    print('Running BOD history-based simulation for symbols:', ', '.join(SYMBOLS))
    for sym in SYMBOLS:
        print('\nSymbol:', sym)
        rows = load_history_for_symbol(sym)
        if not rows:
            print(' No history rows found for', sym)
            continue
        for pname, (s,e) in PERIODS.items():
            ev, sh, inv = simulate_events(rows, s, e)
            print(f" {pname}: events={ev}, shares={sh}, invested={inv:.2f}")
