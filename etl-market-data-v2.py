# %%
# =============================
# Imports
# =============================
import os
import json
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

# =============================
# Configuration
# =============================
OUTPUT_FOLDER = "data"
RAW_COMBINED_PARQUET = os.path.join(OUTPUT_FOLDER, "etl-data-raw.parquet")
PROCESSED_PARQUET = os.path.join(OUTPUT_FOLDER, "etl-data-processed.parquet")
BOD_PARQUET = os.path.join(OUTPUT_FOLDER, "etl-data-bod.parquet")
TICKERS_INDEX = os.path.join(OUTPUT_FOLDER, "tickers", "tickers_index.json")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

legacy_csv_paths = [
    os.path.join(OUTPUT_FOLDER, "etl-data-raw.csv"),
    os.path.join(OUTPUT_FOLDER, "etl-data-processed.csv"),
    os.path.join(OUTPUT_FOLDER, "etl-data-bod.csv"),
]
if os.path.exists(TICKERS_INDEX):
    with open(TICKERS_INDEX, encoding="utf-8") as index_file:
        old_index = json.load(index_file)
    for ticker_entry in old_index.values():
        for file_info in ticker_entry.get("files", {}).values():
            path = file_info.get("path") if isinstance(file_info, dict) else file_info
            if isinstance(path, str) and path.lower().endswith(".csv"):
                legacy_csv_paths.append(path)

# List of tickers to fetch
etf_list = ["AAPL","ALLY","AMZN","FBCG","FMAG",
            "GOOGL","HSBC","MGK","MSFT","NVDA","OEF",
            "QQQ","QQQJ","QTOP","SPYM","TOPT","TSLA",
            "VGT","VTI","XLG"]


# %%
#def safe_str_date(dt):
#    if pd.isna(dt):
#        return ""
#    if hasattr(dt, "strftime"):
#        return dt.strftime("%Y-%m-%d")
#    return str(dt)

rows = []
print("Downloading raw combined Parquet data...")
for sym in etf_list:
    try:
        t = yf.Ticker(sym)
        # Fetch full history from 2005-01-01 through tomorrow (UTC) to include today's row when available
        start_date = "2005-01-01"
        today_utc = datetime.now(timezone.utc).date()
        end_date = (today_utc + timedelta(days=1)).strftime("%Y-%m-%d")
        df = t.history(start=start_date, end=end_date, interval="1d", auto_adjust=True)
        if df is None or df.empty:
            print(f"  no data for {sym}")
            continue

        df = df.reset_index()
        df["Symbol"] = sym

        keep_cols = ["Symbol", "Date", "Open", "High", "Low", "Close", "Volume"]
        for c in keep_cols:
            if c not in df.columns:
                df[c] = pd.NA
        df = df[keep_cols]

        rows.append(df)
        print(f"  fetched {len(df)} rows for {sym}")
    except Exception as e:
        print(f"  error fetching {sym}: {e}")

if rows:
    combined = pd.concat(rows, ignore_index=True)
    combined.to_parquet(RAW_COMBINED_PARQUET, index=False, compression="zstd")
    print(f"Wrote raw combined Parquet -> {RAW_COMBINED_PARQUET}")
else:
    raise RuntimeError("No market data downloaded; existing outputs were left unchanged.")


# %%
from datetime import datetime, timedelta

# Load raw Parquet
df = pd.read_parquet(RAW_COMBINED_PARQUET)

# Ensure Date is parsed as datetime (use utc=True to avoid mixed timezone FutureWarning)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True)

def extract_date_components(date_val):
    if pd.isna(date_val):
        return {'year': None, 'month': None, 'week_of_year': None, 'weekday': None}
    
    # Convert to naive datetime (drop timezone info if present)
    if hasattr(date_val, 'to_pydatetime'):
        dt = date_val.to_pydatetime()
        if dt.tzinfo is not None:
            dt = dt.tz_convert(None) if hasattr(dt, 'tz_convert') else dt.replace(tzinfo=None)
    else:
        dt = date_val
    
    # If dt is pandas Timestamp with tzinfo, convert to naive by normalizing to date in local time
    try:
        if getattr(dt, 'tzinfo', None) is not None:
            dt = dt.tz_convert(None) if hasattr(dt, 'tz_convert') else dt.replace(tzinfo=None)
    except Exception:
        pass

    # First Monday of the year
    jan_1 = datetime(dt.year, 1, 1)
    if jan_1.weekday() == 0:  # Monday
        first_monday = jan_1
    else:
        days_to_monday = 7 - jan_1.weekday()
        first_monday = jan_1 + timedelta(days=days_to_monday)

    # Financial week (1–52)
    if dt >= first_monday:
        financial_week = min(52, ((dt - first_monday).days // 7) + 1)
    else:
        financial_week = 1

    return {
        "year": dt.year,
        "month": dt.month,
        "week_of_year": financial_week,
        "weekday": dt.strftime("%A"),
    }

# --- Apply date components ---
date_components = df["Date"].apply(extract_date_components)
df["Year"] = [comp["year"] for comp in date_components]
df["Month"] = [comp["month"] for comp in date_components]
df["Week"] = [comp["week_of_year"] for comp in date_components]
df["Weekday"] = [comp["weekday"] for comp in date_components]

# --- Numeric conversions ---
df[["Open", "High", "Low", "Close"]] = df[["Open", "High", "Low", "Close"]].apply(pd.to_numeric, errors="coerce")

# --- Avg daily price ---
df["avg_daily_price"] = df[["Open", "High", "Low", "Close"]].mean(axis=1).round(4)

# --- Previous close per symbol ---
df = df.sort_values(["Symbol", "Date"])
df["Previous_Close"] = df.groupby("Symbol")["Close"].shift(1)

# --- Percent metrics ---
mask = df["Previous_Close"].notna() & (df["Previous_Close"] != 0)
if mask.any():
    prev = df.loc[mask, "Previous_Close"].astype(float)

    df.loc[mask, "Daily_Gain_Loss_Pct"] = ((df.loc[mask, "Close"] - prev) / prev * 100).round(2)
    df.loc[mask, "Open_vs_PrevClose_Pct"] = ((df.loc[mask, "Open"] - prev) / prev * 100).round(2)
    df.loc[mask, "Low_vs_PrevClose_Pct"] = ((df.loc[mask, "Low"] - prev) / prev * 100).round(2)
    df.loc[mask, "Close_vs_PrevClose_Pct"] = df.loc[mask, "Daily_Gain_Loss_Pct"]
    df.loc[mask, "mx_percent_decline"] = ((prev - df.loc[mask, "Low"]) / prev * 100).round(2)

df.to_parquet(PROCESSED_PARQUET, index=False, compression="zstd")

# %%
# Load processed daily history (from prior cell output)
df = pd.read_parquet(PROCESSED_PARQUET)

# Parse and ensure numeric types
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df[["Previous_Close", "Low"]] = df[["Previous_Close", "Low"]].apply(pd.to_numeric, errors="coerce")

# --- Define BOD levels as factor multipliers (Previous_Close * factor) ---
bod_levels = {
    "BOD99-1": 0.99,
    "BOD98-2": 0.98,
    "BOD97-3": 0.97,
    "BOD96-4": 0.96,
    "BOD95-5": 0.95,
    "BOD94-6": 0.94,
    "BOD93-7": 0.93,
    "BOD92-8": 0.92,
    "BOD91-9": 0.91,
    "BOD90-10": 0.90,
    "BOD89-11": 0.89,
    "BOD88-12": 0.88,
    "BOD87-13": 0.87,
    "BOD86-14": 0.86,
    "BOD85-15": 0.85,
    "BOD84-16": 0.84,
    "BOD83-17": 0.83,
    "BOD82-18": 0.82,
    "BOD81-19": 0.81,
    "BOD80-20": 0.80,
    "BOD79-21": 0.79,
    "BOD78-22": 0.78,
    "BOD77-23": 0.77,
    "BOD76-24": 0.76,
    "BOD75-25": 0.75,
}

import numpy as np
cols = list(bod_levels.keys())
factors = np.array(list(bod_levels.values()), dtype=float)

# Vectorized computation of limit prices (rows x levels)
prev = df['Previous_Close'].to_numpy(dtype=float)  # NaN where unavailable
low = df['Low'].to_numpy(dtype=float)
limits = (prev[:, None] * factors[None, :])  # shape (n_rows, n_levels)
limits_rounded = np.round(limits, 4)

# Write per-level limit price columns into dataframe
for i, col in enumerate(cols):
    df[col] = limits_rounded[:, i]

# Executed when: low <= limit_price (and prev/low are numeric)
# Note: limits <= prev is always true (all factors < 1.0) so it is omitted
executed_mask = (~np.isnan(prev))[:, None] & (~np.isnan(low))[:, None] & (limits >= low[:, None])

# Compute shares purchased (1 share per executed bucket) and total invested (sum of executed limit prices)
shares = executed_mask.sum(axis=1).astype(int)
total_value = np.round((executed_mask * limits).sum(axis=1), 4)
df['Shares_Purchased'] = shares
df['Total_Value_Purchased'] = total_value

# Add per-level boolean executed columns (e.g., 'BOD99-1_Executed')
for i, col in enumerate(cols):
    exec_col = f"{col}_Executed"
    df[exec_col] = executed_mask[:, i]
    # ensure dtype bool for CSV clarity
    df[exec_col] = df[exec_col].astype(bool)

# Sort by symbol and date for consistent ordering
df = df.sort_values(['Symbol', 'Date'])

# --- Save BOD-enhanced file ---
df.to_parquet(BOD_PARQUET, index=False, compression="zstd")
print(f"Wrote BOD-enhanced data -> {BOD_PARQUET}")

# %%
# Export per-ticker Parquet files for UI consumption
import os
import json

# Read the BOD-enhanced Parquet we just wrote
combined = pd.read_parquet(BOD_PARQUET)

# Ensure avg_daily_price exists (compute if missing)
if 'avg_daily_price' not in combined.columns:
    combined[["Open", "High", "Low", "Close"]] = combined[["Open", "High", "Low", "Close"]].apply(pd.to_numeric, errors='coerce')
    combined['avg_daily_price'] = combined[["Open", "High", "Low", "Close"]].mean(axis=1).round(4)

# Create output directory for tickers (per-symbol folders)
tickers_dir = os.path.join(OUTPUT_FOLDER, 'tickers')
os.makedirs(tickers_dir, exist_ok=True)

# Build index metadata mapping symbol -> { years: [...], last_updated: ISO8601 }
index = {}
for sym, grp in combined.groupby('Symbol'):
    sym_dir = os.path.join(tickers_dir, sym)
    os.makedirs(sym_dir, exist_ok=True)

    # Ensure Date is parsed; convert UTC timestamps to Eastern Time, then format as YYYY-MM-DD
    _dates = pd.to_datetime(grp['Date'], errors='coerce', utc=True)
    grp = grp.copy()
    grp['Date'] = _dates.dt.tz_convert('America/New_York').dt.strftime('%Y-%m-%d')
    grp = grp.sort_values('Date')

    years = sorted(grp['Date'].str[:4].dropna().astype(int).unique().tolist())
    index[sym] = {
        'years': years,
        'last_updated': datetime.now(timezone.utc).isoformat(),
        'files': {}
    }

    # For each year, write a per-year Parquet file for this symbol
    for year in years:
        year_grp = grp[grp['Date'].str.startswith(str(year))]
        if year_grp.empty:
            continue
        fname = f"{sym}-{year}.parquet"
        path = os.path.join(sym_dir, fname)
        # Find possible column variants
        def find_variant(preferred_names, available_cols):
            for n in preferred_names:
                if n in available_cols:
                    return n
            norm_map = {c.lower().replace(' ', '').replace('_', ''): c for c in available_cols}
            for n in preferred_names:
                key = n.lower().replace(' ', '').replace('_', '')
                if key in norm_map:
                    return norm_map[key]
            return None

        available_cols = list(year_grp.columns)
        shares_col = find_variant(['Shares_Purchased', 'Shares Purchased', 'shares_purchased', 'SharesPurchased'], available_cols)
        total_col = find_variant(['Total_Value_Purchased', 'Total Value Purchased', 'TotalValuePurchased', 'total_value_purchased'], available_cols)

        bod_cols = [c for c in available_cols if isinstance(c, str) and (c.startswith('BOD') or 'BOD[' in c or c.upper().startswith('BOD'))]

        if (shares_col or total_col):
            remaining = [c for c in available_cols if c not in (shares_col, total_col)]
            if bod_cols:
                bod_indices = [remaining.index(b) for b in bod_cols if b in remaining]
                insert_idx = min(bod_indices) if bod_indices else 0
            else:
                insert_idx = 0

            insert_cols = []
            if shares_col:
                insert_cols.append(shares_col)
            if total_col and total_col != shares_col:
                insert_cols.append(total_col)

            new_order = remaining[:insert_idx] + insert_cols + remaining[insert_idx:]
            new_order = [c for c in new_order if c in year_grp.columns]
            year_grp = year_grp.reindex(columns=new_order)

        year_grp.to_parquet(path, index=False, compression="zstd")

        # compute file metadata
        try:
            min_date_s = year_grp['Date'].min() or ''
            max_date_s = year_grp['Date'].max() or ''
        except Exception:
            min_date_s = ''
            max_date_s = ''

        row_count = int(len(year_grp))
        size_bytes = None
        try:
            size_bytes = os.path.getsize(path)
        except Exception:
            size_bytes = None

        index[sym]['files'][str(year)] = {
            'path': os.path.join(OUTPUT_FOLDER, 'tickers', sym, fname).replace('\\', '/'),
            'min_date': min_date_s,
            'max_date': max_date_s,
            'row_count': row_count,
            'size_bytes': size_bytes,
            'last_updated': datetime.now(timezone.utc).isoformat()
        }

# Save tickers_index.json in data/tickers
index_path = os.path.join(tickers_dir, 'tickers_index.json')
with open(index_path, 'w') as f:
    json.dump(index, f, indent=2)

for legacy_path in set(legacy_csv_paths):
    if os.path.isfile(legacy_path):
        os.remove(legacy_path)

print(f"Wrote per-ticker per-year Parquet files -> {tickers_dir}")
print(f"Tickers index file -> {index_path}")
