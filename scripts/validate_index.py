#!/usr/bin/env python3
import json
from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / 'data' / 'tickers' / 'tickers_index.json'

if not INDEX_PATH.exists():
    print(f"Index file not found: {INDEX_PATH}")
    sys.exit(2)

with INDEX_PATH.open('r', encoding='utf-8') as f:
    idx = json.load(f)

TOTAL_TICKERS = 0
TOTAL_FILES = 0
missing_files = []
mismatch_rows = []
mismatch_dates = []

# Limit output clutter: record first N mismatches
MAX_SAMPLE = 20

for ticker, entry in sorted(idx.items()):
    TOTAL_TICKERS += 1
    years = entry.get('years') or []
    files = entry.get('files') or {}
    for y in years:
        TOTAL_FILES += 1
        fe = files.get(str(y))
        if fe is None:
            # maybe legacy path under entry directly?
            # try entry.get('path') or entry.get('file')
            missing_files.append((ticker, y, 'no entry'))
            continue
        # determine path
        if isinstance(fe, str):
            p = ROOT / fe
        elif isinstance(fe, dict):
            p = ROOT / (fe.get('path') or '')
        else:
            p = ROOT / ''
        if not p.exists():
            missing_files.append((ticker, y, str(p)))
            continue

        # open CSV and compute actual row counts and min/max dates
        try:
            with p.open('r', encoding='utf-8') as fh:
                lines = [ln for ln in (l.rstrip('\n') for l in fh) if ln.strip()]
            if len(lines) <= 1:
                actual_rows = 0
                header = []
            else:
                header = [h.strip() for h in lines[0].split(',')]
                actual_rows = len(lines) - 1
                # find date idx
            date_idx = None
            if header:
                for i,h in enumerate(header):
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
                        # Accept YYYY-MM-DD or ISO
                        from datetime import datetime
                        d = datetime.fromisoformat(raw)
                    except Exception:
                        try:
                            from datetime import datetime
                            d = datetime.strptime(raw, '%Y-%m-%d')
                        except Exception:
                            continue
                    if file_min is None or d < file_min: file_min = d
                    if file_max is None or d > file_max: file_max = d

            # Compare with metadata if present
            meta_row_count = None
            meta_min = None
            meta_max = None
            if isinstance(fe, dict):
                meta_row_count = fe.get('row_count')
                meta_min = fe.get('min_date')
                meta_max = fe.get('max_date')

            if meta_row_count is not None and int(meta_row_count) != int(actual_rows):
                if len(mismatch_rows) < MAX_SAMPLE:
                    mismatch_rows.append((ticker, y, meta_row_count, actual_rows, str(p)))

            # Compare dates: normalize meta strings to date objects
            from datetime import datetime
            def parse_meta_date(s):
                if not s: return None
                try:
                    return datetime.fromisoformat(s)
                except Exception:
                    try:
                        return datetime.strptime(s, '%Y-%m-%d')
                    except Exception:
                        return None
            mmin = parse_meta_date(meta_min)
            mmax = parse_meta_date(meta_max)
            if mmin and file_min and mmin.date() != file_min.date():
                if len(mismatch_dates) < MAX_SAMPLE:
                    mismatch_dates.append((ticker, y, 'min_date', meta_min, file_min.strftime('%Y-%m-%d'), str(p)))
            if mmax and file_max and mmax.date() != file_max.date():
                if len(mismatch_dates) < MAX_SAMPLE:
                    mismatch_dates.append((ticker, y, 'max_date', meta_max, file_max.strftime('%Y-%m-%d'), str(p)))

        except Exception as e:
            missing_files.append((ticker, y, f'error reading: {e}'))

# Print summary
print('Index validation summary')
print('Tickers in index:', TOTAL_TICKERS)
print('Files referenced (by year entries):', TOTAL_FILES)
print('Missing files count:', len(missing_files))
if missing_files:
    print('\nSample missing files:')
    for t,y,p in missing_files[:MAX_SAMPLE]:
        print(f'  {t} {y} -> {p}')

print('\nRow count mismatches (meta vs actual):', len(mismatch_rows))
for t in mismatch_rows:
    print(' ', t)

print('\nDate mismatches (meta vs actual):', len(mismatch_dates))
for t in mismatch_dates:
    print(' ', t)

if missing_files or mismatch_rows or mismatch_dates:
    print('\nValidation completed with issues')
    sys.exit(2)
else:
    print('\nValidation passed: all referenced files exist and metadata matches CSV content (for checked items).')
    sys.exit(0)
