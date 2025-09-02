import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# =============================
# CONFIGURATION
# =============================
output_folder = "data"
etl_history_csv = "etl_history.csv"

import os
from datetime import datetime
import yfinance as yf
import pandas as pd

# =============================
# CONFIG
# =============================
OUTPUT_FOLDER = "data"
RAW_COMBINED_CSV = os.path.join(OUTPUT_FOLDER, "etl-data-raw.csv")
PROC_COMBINED_CSV = os.path.join(OUTPUT_FOLDER, "etl-data-proc.csv")
ALL_BOD_CSV = os.path.join(OUTPUT_FOLDER, "all_buy_on_dip.csv")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# list of tickers to fetch
etf_list = [
    "ALLY",
    "GGLL",
    "GOOGL",
    "HSBC",
    "MSFT",
    "MSFU",
    "FBCG",
    "FMAG",
    "MGK",
    "OEF",
    "QQQM",
    "QTOP",
    "SPLG",
    "TOPT",
    "VGT",
    "XLG",
    "QQUP",
    "QQXL",
    "TQQQ",
    "UPRO"
]

# Buy-on-dip configuration for ETL (we generate levels 1% .. dip_max_pct %)
dip_step_pct = 1
dip_max_pct = 30  # ETL will emit levels up to this percent (frontend may only allow 1..10)


# =============================
# HELPERS
# =============================
def safe_str_date(dt):
    if pd.isna(dt):
        return ""
    if hasattr(dt, "strftime"):
        return dt.strftime("%Y-%m-%d")
    return str(dt)


def round2(v):
    try:
        return round(float(v), 4)
    except Exception:
        return v


# =============================
# STEP 1: Fetch 20 years of history and write etl-data-raw.csv
# =============================
def fetch_all_history(tickers):
    rows = []
    for sym in tickers:
        print(f"[fetch] {sym}")
        try:
            t = yf.Ticker(sym)
            # 20y daily history
            # Use adjusted prices so ETL v2 aligns with legacy adjusted data (avoids manual split handling)
            df = t.history(period="20y", interval="1d", auto_adjust=True)
            if df is None or df.empty:
                print(f"  no data for {sym}, skipping")
                continue
            df = df.reset_index()
            df["Symbol"] = sym
            # Keep only standard OHLCV columns if present
            keep_cols = ["Date", "Open", "High", "Low", "Close", "Volume", "Symbol"]
            for c in keep_cols:
                if c not in df.columns:
                    df[c] = pd.NA
            df = df[keep_cols]
            rows.append(df)
        except Exception as e:
            print(f"  error fetching {sym}: {e}")

    if not rows:
        print("No data downloaded.")
        return pd.DataFrame()

    combined = pd.concat(rows, ignore_index=True)
    # Normalize Date column to YYYY-MM-DD
    combined["Date"] = combined["Date"].apply(safe_str_date)
    combined.to_csv(RAW_COMBINED_CSV, index=False)
    print(f"Wrote raw combined CSV -> {RAW_COMBINED_CSV}")
    return combined


# =============================
# STEP 2: Process combined data -> etl-data-proc.csv
#  - add Year, Month, Week, Weekday
#  - compute avg_daily_price
#  - compute Previous_Close (per-symbol shift)
#  - compute percent metrics and mx_percent_decline
# =============================
def process_combined(raw_df=None):
    if raw_df is None:
        if not os.path.exists(RAW_COMBINED_CSV):
            raise FileNotFoundError(f"{RAW_COMBINED_CSV} not found; run fetch_all_history() first")
        raw_df = pd.read_csv(RAW_COMBINED_CSV)

    df = raw_df.copy()
    # parse Date to datetime when possible
    df["Date_parsed"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Year"] = df["Date_parsed"].dt.year
    df["Month"] = df["Date_parsed"].dt.month
    df["Week"] = df["Date_parsed"].dt.isocalendar().week
    df["Weekday"] = df["Date_parsed"].dt.day_name()

    # average daily price (simple mean of OHLC where available)
    df[["Open", "High", "Low", "Close"]] = df[["Open", "High", "Low", "Close"]].apply(pd.to_numeric, errors="coerce")
    df["avg_daily_price"] = df[["Open", "High", "Low", "Close"]].mean(axis=1).round(4)

    # previous close per symbol
    df = df.sort_values(["Symbol", "Date_parsed"])
    df["Previous_Close"] = df.groupby("Symbol")["Close"].shift(1)

    # percent calculations relative to previous close (guard missing)
    df["Daily_Gain_Loss_Pct"] = pd.NA
    df["Open_vs_PrevClose_Pct"] = pd.NA
    df["Low_vs_PrevClose_Pct"] = pd.NA
    df["Close_vs_PrevClose_Pct"] = pd.NA
    df["mx_percent_decline"] = pd.NA

    mask = df["Previous_Close"].notna() & (df["Previous_Close"] != 0)
    if mask.any():
        prev = df.loc[mask, "Previous_Close"].astype(float)
        df.loc[mask, "Daily_Gain_Loss_Pct"] = ((df.loc[mask, "Close"].astype(float) - prev) / prev * 100).round(2)
        df.loc[mask, "Open_vs_PrevClose_Pct"] = ((df.loc[mask, "Open"].astype(float) - prev) / prev * 100).round(2)
        df.loc[mask, "Low_vs_PrevClose_Pct"] = ((df.loc[mask, "Low"].astype(float) - prev) / prev * 100).round(2)
        df.loc[mask, "Close_vs_PrevClose_Pct"] = df.loc[mask, "Daily_Gain_Loss_Pct"]
        df.loc[mask, "mx_percent_decline"] = ((prev - df.loc[mask, "Low"].astype(float)) / prev * 100).round(2)

    # final Date normalization
    df["Date"] = df["Date_parsed"].apply(lambda x: x.strftime("%Y-%m-%d") if not pd.isna(x) else "")
    # drop helper column
    df = df.drop(columns=["Date_parsed"]) 

    df.to_csv(PROC_COMBINED_CSV, index=False)
    print(f"Wrote processed combined CSV -> {PROC_COMBINED_CSV}")
    return df


# =============================
# STEP 3: write per-ticker raw/proc files (ticker-data-raw.csv and ticker-data-dca.csv)
# =============================
def write_per_ticker_files(proc_df=None):
    if proc_df is None:
        if not os.path.exists(PROC_COMBINED_CSV):
            raise FileNotFoundError(f"{PROC_COMBINED_CSV} not found; run process_combined() first")
        proc_df = pd.read_csv(PROC_COMBINED_CSV)

    symbols = sorted(proc_df["Symbol"].dropna().unique())
    for sym in symbols:
        ticker_df = proc_df[proc_df["Symbol"] == sym].copy()
        out_raw = os.path.join(OUTPUT_FOLDER, f"{sym}-data-raw.csv")
        ticker_df.to_csv(out_raw, index=False)
        print(f"Wrote {out_raw} ({len(ticker_df)} rows)")

        # create a DCA placeholder file (same as raw processed for now)
        out_dca = os.path.join(OUTPUT_FOLDER, f"{sym}-data-dca.csv")
        ticker_df.to_csv(out_dca, index=False)
    return symbols


# =============================
# STEP 4: Generate per-ticker buy-on-dip events and consolidated all_buy_on_dip.csv
#  - For each day, create limit orders based on previous close for levels 1..dip_max_pct
#  - If day's Low <= limit_price, emit an event row with Executed_Price and Buy_Level
# =============================
def generate_bod_events(proc_df=None, symbols=None, dip_max=dip_max_pct, step=dip_step_pct):
    if proc_df is None:
        if not os.path.exists(PROC_COMBINED_CSV):
            raise FileNotFoundError(f"{PROC_COMBINED_CSV} not found; run process_combined() first")
        proc_df = pd.read_csv(PROC_COMBINED_CSV)

    if symbols is None:
        symbols = sorted(proc_df["Symbol"].dropna().unique())

    event_rows = []
    for sym in symbols:
        ticker_df = proc_df[proc_df["Symbol"] == sym].sort_values("Date")
        # ensure numeric types for price columns
        ticker_df["Previous_Close"] = pd.to_numeric(ticker_df["Previous_Close"], errors="coerce")
        ticker_df["Low"] = pd.to_numeric(ticker_df["Low"], errors="coerce")
        ticker_df["Close"] = pd.to_numeric(ticker_df["Close"], errors="coerce")
        bod_rows = []
        cumulative_shares = 0
        cumulative_invested = 0.0

        for _, row in ticker_df.iterrows():
            prev_close = row.get("Previous_Close")
            if pd.isna(prev_close) or prev_close == 0:
                continue
            day_low = row.get("Low")
            day_date = row.get("Date")
            day_close = row.get("Close")
            # weekday string when available
            try:
                weekday = pd.to_datetime(day_date).day_name()
            except Exception:
                weekday = ''

            # generate levels 1..dip_max inclusive
            for level in range(1, dip_max + 1, step):
                limit_price = prev_close * (1 - (level / 100.0))
                if pd.isna(day_low):
                    continue
                if day_low <= limit_price:
                    executed_price = round2(limit_price)
                    shares = 1
                    cost = round2(executed_price * shares)

                    cumulative_shares += shares
                    cumulative_invested += cost
                    cumulative_value = round2((cumulative_shares * day_close) if not pd.isna(day_close) else None)

                    # emit event with multiple field variants front-end expects
                    event = {
                        "Date": day_date,
                        "Date_add": day_date,
                        "Weekday": weekday,
                        "Symbol": sym,
                        "Strategy": "Buy_on_Dip",
                        "Buy_Level": level,
                        "Buy_Price": round2(limit_price),
                        "Buy Price": round2(limit_price),
                        "Executed": True,
                        "Executed_Price": executed_price,
                        "Shares_Purchased": shares,
                        "Shares Purchased": shares,
                        "Dollars_Invested": cost,
                        "Dollars Invested": cost,
                        "Cumulative Shares": cumulative_shares,
                        "Cumulative Invested": round2(cumulative_invested),
                        "Cumulative Value": cumulative_value,
                        "Close": round2(day_close) if not pd.isna(day_close) else None,
                        "Previous_Close": round2(prev_close) if not pd.isna(prev_close) else None,
                    }

                    bod_rows.append(event)
                    event_rows.append(event)

        # save per-ticker bod csv
        out_bod = os.path.join(OUTPUT_FOLDER, f"{sym}-data-bod.csv")
        if bod_rows:
            pd.DataFrame(bod_rows).to_csv(out_bod, index=False)
            print(f"Wrote BOD events for {sym} -> {out_bod} ({len(bod_rows)} rows)")
        else:
            # create empty file with headers expected by frontend
            pd.DataFrame(
                columns=[
                    "Date_add",
                    "Date",
                    "Weekday",
                    "Symbol",
                    "Strategy",
                    "Buy_Level",
                    "Buy_Price",
                    "Buy Price",
                    "Executed",
                    "Executed_Price",
                    "Shares_Purchased",
                    "Shares Purchased",
                    "Dollars_Invested",
                    "Dollars Invested",
                    "Cumulative Shares",
                    "Cumulative Invested",
                    "Cumulative Value",
                    "Close",
                    "Previous_Close",
                ]
            ).to_csv(out_bod, index=False)
            print(f"Wrote (empty) BOD file for {sym} -> {out_bod}")

    # consolidated all events
    if event_rows:
        all_df = pd.DataFrame(event_rows)
        all_df.to_csv(ALL_BOD_CSV, index=False)
        print(f"Wrote consolidated BOD CSV -> {ALL_BOD_CSV} ({len(all_df)} rows)")
    else:
        pd.DataFrame().to_csv(ALL_BOD_CSV, index=False)
        print(f"No BOD events generated; wrote empty {ALL_BOD_CSV}")


# =============================
# MAIN
# =============================
def main():
    print("ETL v2 starting")
    combined_raw = fetch_all_history(etf_list)
    if combined_raw.empty:
        print("No raw data, aborting.")
        return
    proc = process_combined(combined_raw)
    symbols = write_per_ticker_files(proc)
    generate_bod_events(proc, symbols)
    print("ETL v2 complete")


if __name__ == "__main__":
    main()


