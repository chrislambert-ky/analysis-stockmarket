import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# =============================
# CONFIGURATION
# =============================
output_folder = "data"
os.makedirs(output_folder, exist_ok=True)

etf_list = ["SPLG","XLG","TOPT","QQQ","VGT","QTOP","FBCG","MSFT","GOOGL","UPRO","TQQQ","QQUP","GGLL","MSFU"]

# Buy-on-dip configuration: generate limit orders at 1% steps up to dip_max_pct.
# This ensures very deep single-day declines will have additional limit orders recorded.
dip_step_pct = 1  # step in percent (1% increments)
dip_max_pct = 30  # generate orders from 1% down to dip_max_pct (e.g., 30% deep days)


# =============================
# EXTRACT ALL HISTORICAL DATA FIRST
# =============================
def extract_all_historical_data():
    """Download and consolidate all historical data first, then perform calculations."""
    print("Phase 1: Downloading all historical data...")
    all_history = []
    
    for ticker_symbol in etf_list:
        print(f"Downloading data for {ticker_symbol}...")
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period="20y", interval="1d")

        if data.empty:
            print(f"No data found for {ticker_symbol}, skipping...")
            continue

        df = data.copy()
        df.reset_index(inplace=True)
        
        # Use datetime library for more efficient date extraction
        df['Date_add'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        df['Symbol'] = ticker_symbol
        
        # Extract date components using datetime methods (Financial Calendar approach)
        def extract_date_components(date_val):
            # Convert to naive datetime for comparison
            if hasattr(date_val, 'to_pydatetime'):
                dt = date_val.to_pydatetime()
                if dt.tzinfo is not None:
                    dt = dt.replace(tzinfo=None)  # Remove timezone for comparison
            else:
                dt = date_val
            
            # Calculate financial week (52 weeks max, Monday start)
            jan_1 = datetime(dt.year, 1, 1)
            # Find first Monday of the year
            if jan_1.weekday() == 0:  # Jan 1 is Monday
                first_monday = jan_1
            else:  # Jan 1 is Tue-Sun, find next Monday
                days_to_monday = 7 - jan_1.weekday()
                first_monday = jan_1 + timedelta(days=days_to_monday)
            
            if dt >= first_monday:
                financial_week = min(52, ((dt - first_monday).days // 7) + 1)
            else:
                # Before first Monday of year, belongs to week 1
                financial_week = 1
            
            return {
                'year': dt.year,
                'month': dt.month, 
                'week_of_year': financial_week,
                'weekday': dt.strftime('%A')
            }
        
        date_components = df['Date'].apply(extract_date_components)
        df['Year'] = [comp['year'] for comp in date_components]
        df['Month'] = [comp['month'] for comp in date_components]
        df['Week'] = [comp['week_of_year'] for comp in date_components]
        df['Weekday'] = [comp['weekday'] for comp in date_components]
        
        df['avg_daily_price'] = df[['Open', 'High', 'Low', 'Close']].mean(axis=1)
        
        all_history.append(df)
    
    if not all_history:
        return pd.DataFrame()
    
    # Combine all historical data
    combined_history = pd.concat(all_history, ignore_index=True)
    
    # Sort by Symbol and Date to ensure proper order for previous close calculation
    combined_history = combined_history.sort_values(['Symbol', 'Date']).reset_index(drop=True)
    
    # Add previous day's close price
    combined_history['Previous_Close'] = combined_history.groupby('Symbol')['Close'].shift(1)
    
    # Compute percent metrics relative to previous close using vectorized operations
    # Guard against missing or zero previous close
    mask = combined_history['Previous_Close'].notna() & (combined_history['Previous_Close'] != 0)
    # Initialize columns with NA
    combined_history['Daily_Gain_Loss_Pct'] = pd.NA
    combined_history['Open_vs_PrevClose_Pct'] = pd.NA
    combined_history['Low_vs_PrevClose_Pct'] = pd.NA
    combined_history['Close_vs_PrevClose_Pct'] = pd.NA
    combined_history['mx_percent_decline'] = pd.NA

    # Compute where valid
    if mask.any():
        prev = combined_history.loc[mask, 'Previous_Close']
        combined_history.loc[mask, 'Daily_Gain_Loss_Pct'] = ((combined_history.loc[mask, 'Close'] - prev) / prev * 100).round(2)
        combined_history.loc[mask, 'Open_vs_PrevClose_Pct'] = ((combined_history.loc[mask, 'Open'] - prev) / prev * 100).round(2)
        combined_history.loc[mask, 'Low_vs_PrevClose_Pct'] = ((combined_history.loc[mask, 'Low'] - prev) / prev * 100).round(2)
        combined_history.loc[mask, 'Close_vs_PrevClose_Pct'] = combined_history.loc[mask, 'Daily_Gain_Loss_Pct']
        # mx_percent_decline: percent difference between previous close and the day's low
        combined_history.loc[mask, 'mx_percent_decline'] = ((prev - combined_history.loc[mask, 'Low']) / prev * 100).round(2)
    
    # Apply date transformation using datetime to ensure 'yyyy-mm-dd' format
    combined_history['Date'] = combined_history['Date'].apply(lambda x: x.strftime('%Y-%m-%d') if hasattr(x, 'strftime') else str(x))
    
    # Reorder columns to start with key fields and group related metrics
    column_order = [
        'Date_add', 'Weekday', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Previous_Close',
        'Daily_Gain_Loss_Pct', 'Open_vs_PrevClose_Pct', 'Low_vs_PrevClose_Pct', 
        'Close_vs_PrevClose_Pct', 'mx_percent_decline'
    ] + [col for col in combined_history.columns if col not in [
        'Date_add', 'Weekday', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Previous_Close',
        'Daily_Gain_Loss_Pct', 'Open_vs_PrevClose_Pct', 'Low_vs_PrevClose_Pct', 
        'Close_vs_PrevClose_Pct', 'mx_percent_decline'
    ]]
    combined_history = combined_history[column_order]
    
    # Save the consolidated historical data
    combined_csv_path = os.path.join(output_folder, "history_tickers.csv")
    combined_history.to_csv(combined_csv_path, index=False)
    print(f"Saved consolidated historical data → {combined_csv_path}")
    
    return combined_history

def load_historical_data():
    """Load historical data from file if it exists."""
    combined_csv_path = os.path.join(output_folder, "history_tickers.csv")
    if os.path.exists(combined_csv_path):
        print("Loading existing historical data from file...")
        return pd.read_csv(combined_csv_path)
    return pd.DataFrame()


# (DCA transform removed - DCA calculations are performed client-side in JS)


# =============================
# TRANSFORM (BUY-ON-DIP) - FROM HISTORICAL DATA
# =============================
def transform_buy_on_dip_from_historical(historical_data):
    """Simulate Buy-on-Dip strategy from consolidated historical data."""
    all_bod = []
    
    # Process each ticker separately
    for ticker_symbol in historical_data['Symbol'].unique():
        print(f"Processing buy-on-dip for {ticker_symbol}...")
        ticker_data = historical_data[historical_data['Symbol'] == ticker_symbol].copy()
        ticker_data = ticker_data.sort_values('Date_add')
        
        purchased_list = []

        for _, row in ticker_data.iterrows():
            open_price = row['Open']
            close_price = row['Close']
            low_price = row['Low']
            previous_close = row['Previous_Close']
            date = row['Date_add']
            weekday = row['Weekday']
            
            # Skip first day of each ticker (no previous close)
            if pd.isna(previous_close):
                continue

            # Generate percent levels from 1% to dip_max_pct (1%, 2%, ...)
            for pct in range(dip_step_pct, dip_max_pct + 1, dip_step_pct):
                # level multiplier e.g., for pct=1 -> 0.99
                level = 1.0 - (pct / 100.0)
                # Calculate target price based on PREVIOUS DAY'S CLOSE (limit order set previous night)
                target_price = previous_close * level
                # If the day's low reached or went below the limit price, the order would fill
                if low_price <= target_price:
                    # Simulate fills occurring at each limit level as the market moves down.
                    # Use the level's target price as the executed price (limit orders fill at the limit or better).
                    # Using the day's low for all fills caused every level to show the same executed price;
                    # using target_price preserves distinct execution prices per level.
                    executed_price = target_price
                    # Executed level (percent decline from previous close to executed price)
                    executed_level = round((1.0 - (executed_price / previous_close)) * 100, 2) if previous_close and previous_close != 0 else None
                    purchased_list.append({
                        'Date_add': date,
                        'Weekday': weekday,
                        'Symbol': row['Symbol'],
                        'Strategy': 'Buy_on_Dip',
                        # Buy_Price remains the limit price derived from previous close
                        'Buy_Price': round(target_price, 6),
                        'Buy_Level': f"{pct}%",
                        'Executed_Price': round(executed_price, 6),
                        'Executed_Level': executed_level,
                        'Shares Purchased': 1,
                        # Dollars invested should reflect the actual executed price
                        'Dollars Invested': round(executed_price, 6),
                        'Close': close_price,
                        'Previous_Close': previous_close
                    })

        if not purchased_list:
            continue

        df_bod = pd.DataFrame(purchased_list)
        if df_bod.empty:
            continue
        # Within a day, sort fills by Buy_Price descending so higher-price fills (smaller dips)
        # are recorded first as the market falls.
        df_bod = df_bod.sort_values(['Date_add', 'Buy_Price'], ascending=[True, False]).reset_index(drop=True)
        df_bod['Cumulative Shares'] = df_bod['Shares Purchased'].cumsum()
        df_bod['Cumulative Invested'] = df_bod['Dollars Invested'].cumsum()
        df_bod['Cumulative Value'] = (df_bod['Cumulative Shares'] * df_bod['Close']).round(2)
        
        # Include executed fields if present
        cols = ['Date_add', 'Weekday', 'Symbol', 'Strategy', 'Buy_Price', 'Buy_Level']
        if 'Executed_Price' in df_bod.columns:
            cols += ['Executed_Price']
        if 'Executed_Level' in df_bod.columns:
            cols += ['Executed_Level']
        cols += ['Shares Purchased', 'Dollars Invested', 'Cumulative Shares', 'Cumulative Invested', 'Cumulative Value', 'Close', 'Previous_Close']
        result_df = df_bod[cols]
        all_bod.append(result_df)
    
    if not all_bod:
        return pd.DataFrame()
    
    return pd.concat(all_bod, ignore_index=True)


# =============================
# LOAD
# =============================
def load_data(df, ticker_symbol, strategy):
    """Save purchase history to CSV and Excel."""
    if df.empty:
        return
    csv_name = os.path.join(output_folder, f"{ticker_symbol.lower()}_{strategy}.csv")
    xlsx_name = os.path.join(output_folder, f"{ticker_symbol.lower()}_{strategy}.xlsx")
    df.to_csv(csv_name, index=False)
    df.to_excel(xlsx_name, index=False)
    print(f"Saved {strategy} history for {ticker_symbol} → {csv_name} and {xlsx_name}")


# =============================
# MAIN ETL PROCESS
# =============================
def main():
    """Main ETL process: Extract all historical data first, then calculate strategies."""
    
    # Phase 1: Always extract all historical data and overwrite the consolidated CSV
    print("Phase 1: Regenerating consolidated historical data (will overwrite existing file if present)...")
    historical_data = extract_all_historical_data()
    if historical_data.empty:
        print("No historical data available after extraction. Exiting.")
        return
    
    print(f"Phase 2: Processing strategies from {len(historical_data)} historical records...")
    
    # Phase 2: Calculate Buy-on-Dip strategy from historical data
    bod_df = transform_buy_on_dip_from_historical(historical_data)

    # Phase 3: Save Buy-on-Dip results
    consolidations = [
        (bod_df, 'all_buy_on_dip'),
    ]

    def round_columns(df):
        # 5 decimals for shares, 2 decimals for dollar columns
        share_cols = ['Shares Purchased', 'Cumulative Shares']
        dollar_cols = [
            'Buy_Price', 'Dollars Invested', 'Cumulative Invested', 'Cumulative Value', 'Close', 'Previous_Close'
        ]
        # Add executed price/level to dollar and percent formatting
        if 'Executed_Price' in df.columns:
            dollar_cols.append('Executed_Price')
        percent_cols = []
        if 'Executed_Level' in df.columns:
            percent_cols.append('Executed_Level')
        for col in share_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').round(5)
        for col in dollar_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').round(2)
        for col in percent_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').round(2)
        return df

    for df, name in consolidations:
        if df is None or df.empty:
            print(f"No data for {name}, skipping...")
            continue
        df = round_columns(df)
        csv_name = os.path.join(output_folder, f'{name}.csv')
        try:
            df.to_csv(csv_name, index=False)
            print(f"Saved consolidated {name} to {csv_name}")
        except PermissionError:
            print(f"Permission denied writing {csv_name}, file may be open in another application")
            continue

    print("ETL process completed successfully!")

if __name__ == "__main__":
    main()
