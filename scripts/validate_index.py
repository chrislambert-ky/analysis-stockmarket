#!/usr/bin/env python3
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
INDEX_PATH = DATA_DIR / "tickers" / "tickers_index.json"
REPORT_PATH = DATA_DIR / "data_report.json"
MAX_SAMPLE = 20


def main():
    if not INDEX_PATH.exists():
        print(f"Index file not found: {INDEX_PATH}")
        return 2

    with INDEX_PATH.open("r", encoding="utf-8") as index_file:
        index = json.load(index_file)

    missing_files = []
    row_mismatches = []
    date_mismatches = []
    total_files = 0

    for ticker, entry in sorted(index.items()):
        files = entry.get("files") or {}
        for year in entry.get("years") or []:
            total_files += 1
            metadata = files.get(str(year))
            if metadata is None:
                missing_files.append(f"{ticker} {year}: no file entry")
                continue

            relative_path = metadata.get("path") if isinstance(metadata, dict) else metadata
            if not relative_path:
                missing_files.append(f"{ticker} {year}: no path in index")
                continue

            path = ROOT / relative_path
            if not path.is_file():
                missing_files.append(f"{ticker} {year}: missing {relative_path}")
                continue

            try:
                dates = pd.read_parquet(path, columns=["Date"])["Date"]
                parsed_dates = pd.to_datetime(dates, errors="coerce", utc=True).dropna()
                actual_rows = len(dates)
                min_date = parsed_dates.min().date().isoformat() if not parsed_dates.empty else None
                max_date = parsed_dates.max().date().isoformat() if not parsed_dates.empty else None
            except Exception as error:
                missing_files.append(f"{ticker} {year}: unable to read {relative_path}: {error}")
                continue

            if isinstance(metadata, dict):
                expected_rows = metadata.get("row_count")
                if expected_rows is not None and int(expected_rows) != actual_rows:
                    row_mismatches.append({
                        "ticker": ticker,
                        "year": year,
                        "expected": int(expected_rows),
                        "actual": actual_rows,
                        "path": relative_path,
                    })

                for field, actual in (("min_date", min_date), ("max_date", max_date)):
                    expected = metadata.get(field)
                    if expected and actual and expected != actual:
                        date_mismatches.append({
                            "ticker": ticker,
                            "year": year,
                            "field": field,
                            "expected": expected,
                            "actual": actual,
                            "path": relative_path,
                        })

    errors = missing_files + row_mismatches + date_mismatches
    report = {
        "ok": not errors,
        "tickers": len(index),
        "files": total_files,
        "missing_files": missing_files[:MAX_SAMPLE],
        "row_mismatches": row_mismatches[:MAX_SAMPLE],
        "date_mismatches": date_mismatches[:MAX_SAMPLE],
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print("Parquet index validation summary")
    print("Tickers:", report["tickers"])
    print("Files referenced:", total_files)
    print("Missing/unreadable files:", len(missing_files))
    print("Row count mismatches:", len(row_mismatches))
    print("Date range mismatches:", len(date_mismatches))
    print("Report:", REPORT_PATH)

    if errors:
        print("Validation completed with issues.")
        return 2

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
