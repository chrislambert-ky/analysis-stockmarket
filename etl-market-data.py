import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# =============================
# CONFIGURATION
# =============================
output_folder = "data"
os.makedirs(output_folder, exist_ok=True)

etf_list = [
    "QQQ","FBCG","QTOP","MGK","VGT",
    "SPLG","XLG","TOPT","FMAG"
]

weekly_investment = 25.0

dip_levels = [0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.90]  # 1% → 10% dips


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
        data = ticker.history(period="10y", interval="1d")

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
    
    # Add daily gain/loss calculations for buy-on-dip troubleshooting
    def calculate_daily_metrics(row):
        """Calculate daily performance metrics."""
        if pd.isna(row['Previous_Close']) or row['Previous_Close'] == 0:
            return pd.Series({
                'Daily_Gain_Loss_Pct': None,
                'Open_vs_PrevClose_Pct': None, 
                'Low_vs_PrevClose_Pct': None,
                'Close_vs_PrevClose_Pct': None,
                'Max_Decline_Pct': None
            })
        
        prev_close = row['Previous_Close']
        open_price = row['Open']
        low_price = row['Low'] 
        close_price = row['Close']
        
        # Calculate percentage changes from previous close
        daily_gain_loss = ((close_price - prev_close) / prev_close) * 100
        open_vs_prev = ((open_price - prev_close) / prev_close) * 100
        low_vs_prev = ((low_price - prev_close) / prev_close) * 100
        close_vs_prev = ((close_price - prev_close) / prev_close) * 100
        
        # Maximum decline during the day - specifically comparing Previous_Close to Low
        # This represents the deepest dip during the trading day
        max_decline = low_vs_prev
        
        return pd.Series({
            'Daily_Gain_Loss_Pct': round(daily_gain_loss, 2),
            'Open_vs_PrevClose_Pct': round(open_vs_prev, 2),
            'Low_vs_PrevClose_Pct': round(low_vs_prev, 2), 
            'Close_vs_PrevClose_Pct': round(close_vs_prev, 2),
            'Max_Decline_Pct': round(max_decline, 2)
        })
    
    # Apply the calculations
    daily_metrics = combined_history.apply(calculate_daily_metrics, axis=1)
    combined_history = pd.concat([combined_history, daily_metrics], axis=1)
    
    # Apply date transformation using datetime to ensure 'yyyy-mm-dd' format
    combined_history['Date'] = combined_history['Date'].apply(lambda x: x.strftime('%Y-%m-%d') if hasattr(x, 'strftime') else str(x))
    
    # Reorder columns to start with key fields and group related metrics
    column_order = [
        'Date_add', 'Weekday', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Previous_Close',
        'Daily_Gain_Loss_Pct', 'Open_vs_PrevClose_Pct', 'Low_vs_PrevClose_Pct', 
        'Close_vs_PrevClose_Pct', 'Max_Decline_Pct'
    ] + [col for col in combined_history.columns if col not in [
        'Date_add', 'Weekday', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Previous_Close',
        'Daily_Gain_Loss_Pct', 'Open_vs_PrevClose_Pct', 'Low_vs_PrevClose_Pct', 
        'Close_vs_PrevClose_Pct', 'Max_Decline_Pct'
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


# =============================
# TRANSFORM (DCA) - FROM HISTORICAL DATA
# =============================
def transform_weekly_from_historical(historical_data):
    """Generate weekly DCA purchase history at $25/week on Mondays from consolidated historical data."""
    all_weekly = []
    
    # Process each ticker separately
    for ticker_symbol in historical_data['Symbol'].unique():
        print(f"Processing weekly DCA for {ticker_symbol}...")
        ticker_data = historical_data[historical_data['Symbol'] == ticker_symbol].copy()
        ticker_data = ticker_data.sort_values('Date_add')
        
        # Convert Date_add to datetime using datetime library for more efficient grouping
        def parse_and_group_date(date_str):
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            return f"{dt.year}-{dt.isocalendar().week:02d}"
        
        ticker_data['year_week'] = ticker_data['Date_add'].apply(parse_and_group_date)
        
        weekly_purchases = []
        
        # Group by year-week and find Monday or closest trading day
        for year_week, week_data in ticker_data.groupby('year_week'):
            week_data = week_data.sort_values('Date_add')
            
            # Use datetime library to find Monday more efficiently
            monday_data = []
            for _, row in week_data.iterrows():
                dt = datetime.strptime(row['Date_add'], '%Y-%m-%d')
                if dt.weekday() == 0:  # Monday = 0 in datetime
                    monday_data.append(row)
            
            if monday_data:
                # Use the first Monday found
                selected_day = monday_data[0]
            else:
                # If no Monday, use the first trading day of the week
                selected_day = week_data.iloc[0]
            
            weekly_purchases.append(selected_day)
        
        if not weekly_purchases:
            continue
            
        purchases_df = pd.DataFrame(weekly_purchases)
        
        purchases = purchases_df[[
            'Date_add', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Previous_Close',
            'Week', 'Weekday', 'avg_daily_price'
        ]].copy()

        purchases['Strategy'] = 'DCA_Weekly'
        purchases['Buy_Price'] = purchases['avg_daily_price']
        purchases['Buy_Level'] = 'DCA'
        purchases['Shares Purchased'] = (weekly_investment / purchases['avg_daily_price']).round(6)
        purchases['Dollars Invested'] = weekly_investment
        purchases['Cumulative Shares'] = purchases['Shares Purchased'].cumsum()
        purchases['Cumulative Invested'] = purchases['Dollars Invested'].cumsum()
        purchases['Cumulative Value'] = (purchases['Cumulative Shares'] * purchases['Close']).round(2)

        result_df = purchases[['Date_add', 'Weekday', 'Symbol', 'Strategy', 'Buy_Price', 'Buy_Level', 'Shares Purchased', 'Dollars Invested', 'Cumulative Shares', 'Cumulative Invested', 'Cumulative Value', 'Close', 'Previous_Close']]
        all_weekly.append(result_df)
    
    if not all_weekly:
        return pd.DataFrame()
    
    return pd.concat(all_weekly, ignore_index=True)


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
            
            for level in sorted(dip_levels):  # Ensure buy levels are processed from smallest to largest
                # Calculate target price based on PREVIOUS DAY'S CLOSE (limit order set previous night)
                target_price = previous_close * level
                if low_price <= target_price:
                    purchased_list.append({
                        'Date_add': date,
                        'Weekday': weekday,
                        'Symbol': row['Symbol'],
                        'Strategy': 'Buy_on_Dip',
                        'Buy_Price': round(target_price, 6),
                        'Buy_Level': f"{(1 - level) * 100:.0f}%",
                        'Shares Purchased': 1,
                        'Dollars Invested': round(target_price, 6),
                        'Close': close_price,
                        'Previous_Close': previous_close
                    })

        if not purchased_list:
            continue

        df_bod = pd.DataFrame(purchased_list)
        df_bod = df_bod.sort_values(['Date_add', 'Buy_Level']).reset_index(drop=True)
        df_bod['Cumulative Shares'] = df_bod['Shares Purchased'].cumsum()
        df_bod['Cumulative Invested'] = df_bod['Dollars Invested'].cumsum()
        df_bod['Cumulative Value'] = (df_bod['Cumulative Shares'] * df_bod['Close']).round(2)
        
        result_df = df_bod[['Date_add', 'Weekday', 'Symbol', 'Strategy', 'Buy_Price', 'Buy_Level', 'Shares Purchased', 'Dollars Invested', 'Cumulative Shares', 'Cumulative Invested', 'Cumulative Value', 'Close', 'Previous_Close']]
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
    
    # Phase 1: Extract or load all historical data
    historical_data = load_historical_data()
    if historical_data.empty:
        historical_data = extract_all_historical_data()
        if historical_data.empty:
            print("No historical data available. Exiting.")
            return
    
    print(f"Phase 2: Processing strategies from {len(historical_data)} historical records...")
    
    # Phase 2: Calculate strategies from historical data
    weekly_df = transform_weekly_from_historical(historical_data)
    bod_df = transform_buy_on_dip_from_historical(historical_data)
    
    # Phase 3: Save strategy results
    consolidations = [
        (weekly_df, 'all_dca_weekly'),
        (bod_df, 'all_buy_on_dip'),
    ]

    def round_columns(df):
        # 5 decimals for shares, 2 decimals for dollar columns
        share_cols = ['Shares Purchased', 'Cumulative Shares']
        dollar_cols = [
            'Buy_Price', 'Dollars Invested', 'Cumulative Invested', 'Cumulative Value', 'Close', 'Previous_Close'
        ]
        for col in share_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').round(5)
        for col in dollar_cols:
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
