#!/usr/bin/env python3
"""
Inventory data/tickers using tickers_index.json. Produce data/data_report.json summarizing totals and anomalies.
"""
import json
from pathlib import Path
from datetime import datetime
import sys

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / 'data' / 'tickers' / 'tickers_index.json'
OUT_PATH = ROOT / 'data' / 'data_report.json'

if not INDEX_PATH.exists():
    print('tickers_index.json not found', INDEX_PATH)
    sys.exit(1)

with INDEX_PATH.open('r', encoding='utf-8') as f:
    index = json.load(f)

report = {
    'generated_at': datetime.utcnow().isoformat() + 'Z',
    'tickers': {},
    'totals': {
        'tickers': 0,
        'files': 0,
        'rows': 0,
        'size_bytes': 0
    },
    'anomalies': {
        'missing_files': [],
        'row_mismatches': [],
        'date_mismatches': [],
        'zero_row_files': []
    }
}

for ticker, entry in sorted(index.items()):
    tentry = {'years': entry.get('years', []), 'last_updated': entry.get('last_updated'), 'files': {}, 'summary': {}}
    total_rows = 0
    total_size = 0
    files_count = 0

    files = entry.get('files') or {}
    for year in tentry['years']:
        files_count += 1
        fe = files.get(str(year))
        if fe is None:
            report['anomalies']['missing_files'].append({'ticker': ticker, 'year': year})
            tentry['files'][str(year)] = {'present': False}
            continue
        # determine path and metadata
        if isinstance(fe, str):
            path = ROOT / fe
            meta_row = None
            meta_min = None
            meta_max = None
            meta_size = None
            last_up = None
        else:
            path = ROOT / (fe.get('path') or '')
            meta_row = fe.get('row_count')
            meta_min = fe.get('min_date')
            meta_max = fe.get('max_date')
            meta_size = fe.get('size_bytes')
            last_up = fe.get('last_updated')

        file_info = {'path': str(path), 'present': path.exists(), 'meta_row': meta_row, 'meta_min': meta_min, 'meta_max': meta_max, 'meta_size': meta_size, 'last_updated': last_up}

        if not path.exists():
            report['anomalies']['missing_files'].append({'ticker': ticker, 'year': year, 'path': str(path)})
            tentry['files'][str(year)] = file_info
            continue

        # read file to compute rows and min/max dates
        try:
            with path.open('r', encoding='utf-8') as fh:
                lines = [ln.rstrip('\n') for ln in fh if ln.strip()]
            if len(lines) <= 1:
                actual_rows = 0
                headers = []
            else:
                headers = [h.strip() for h in lines[0].split(',')]
                actual_rows = len(lines) - 1

            date_idx = None
            if headers:
                for i, h in enumerate(headers):
                    if h.lower() == 'date':
                        date_idx = i
                        break
            file_min = None
            file_max = None
            if date_idx is not None:
                for row in lines[1:]:
                    cols = row.split(',')
                    if len(cols) <= date_idx: continue
                    raw = cols[date_idx].strip()
                    if not raw: continue
                    try:
                        d = datetime.fromisoformat(raw)
                    except Exception:
                        try:
                            d = datetime.strptime(raw, '%Y-%m-%d')
                        except Exception:
                            continue
                    if file_min is None or d < file_min: file_min = d
                    if file_max is None or d > file_max: file_max = d

            file_info.update({'actual_rows': actual_rows, 'actual_min': file_min.isoformat()[:10] if file_min else None, 'actual_max': file_max.isoformat()[:10] if file_max else None, 'size_bytes': path.stat().st_size})

            # totals
            total_rows += actual_rows
            report['totals']['rows'] += actual_rows
            size_bytes = path.stat().st_size
            total_size += size_bytes
            report['totals']['size_bytes'] += size_bytes
            report['totals']['files'] += 1

            # anomalies
            if meta_row is not None and int(meta_row) != int(actual_rows):
                report['anomalies']['row_mismatches'].append({'ticker': ticker, 'year': year, 'meta_row': meta_row, 'actual_rows': actual_rows, 'path': str(path)})
            if meta_min and file_min and meta_min != (file_min.isoformat()[:10]):
                report['anomalies']['date_mismatches'].append({'ticker': ticker, 'year': year, 'meta_min': meta_min, 'actual_min': file_min.isoformat()[:10], 'path': str(path)})
            if meta_max and file_max and meta_max != (file_max.isoformat()[:10]):
                report['anomalies']['date_mismatches'].append({'ticker': ticker, 'year': year, 'meta_max': meta_max, 'actual_max': file_max.isoformat()[:10], 'path': str(path)})
            if actual_rows == 0:
                report['anomalies']['zero_row_files'].append({'ticker': ticker, 'year': year, 'path': str(path)})

            tentry['files'][str(year)] = file_info
        except Exception as e:
            tentry['files'][str(year)] = {'path': str(path), 'error': str(e)}
            report['anomalies']['missing_files'].append({'ticker': ticker, 'year': year, 'path': str(path), 'error': str(e)})

    tentry['summary'] = {'files': files_count, 'rows': total_rows, 'size_bytes': total_size}
    report['tickers'][ticker] = tentry
    report['totals']['tickers'] += 1

# compute largest tickers by rows and size
rows_sorted = sorted(((t, report['tickers'][t]['summary']['rows']) for t in report['tickers']), key=lambda x: x[1], reverse=True)
size_sorted = sorted(((t, report['tickers'][t]['summary']['size_bytes']) for t in report['tickers']), key=lambda x: x[1], reverse=True)
report['largest_by_rows'] = rows_sorted[:10]
report['largest_by_size'] = size_sorted[:10]

# write report
with OUT_PATH.open('w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)

print('Report written to', OUT_PATH)
print('Tickers:', report['totals']['tickers'], 'Files:', report['totals']['files'], 'Rows:', report['totals']['rows'], 'SizeBytes:', report['totals']['size_bytes'])

# Print a short anomalies summary
print('\nAnomalies:')
for k,v in report['anomalies'].items():
    print(f'  {k}: {len(v)}')

if report['anomalies']['missing_files'] or report['anomalies']['row_mismatches'] or report['anomalies']['date_mismatches']:
    print('\nSome anomalies found; see data/data_report.json for details')
    sys.exit(2)
else:
    print('\nNo anomalies detected')
    sys.exit(0)
