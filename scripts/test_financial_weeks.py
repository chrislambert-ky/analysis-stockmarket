#!/usr/bin/env python3
"""Test the financial week numbering approach."""

from datetime import datetime, timedelta

def calculate_financial_week(date_str):
    """Calculate financial week (52 weeks max, Monday start)."""
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Find first Monday of the year
    jan_1 = datetime(dt.year, 1, 1)
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
    
    return financial_week

# Test with problematic dates
test_dates = [
    '2015-12-28', '2015-12-29', '2015-12-30', '2015-12-31',
    '2016-01-01', '2016-01-04',
    '2020-12-28', '2020-12-29', '2020-12-30', '2020-12-31', 
    '2021-01-01', '2021-01-04'
]

print("Financial Week Numbering Test:")
print("=" * 50)
print(f"{'Date':<12} {'ISO Week':<10} {'Financial Week':<15} {'Weekday'}")
print("-" * 50)

for date_str in test_dates:
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    iso_week = dt.isocalendar().week
    financial_week = calculate_financial_week(date_str)
    weekday = dt.strftime('%A')
    
    print(f"{date_str:<12} {iso_week:<10} {financial_week:<15} {weekday}")
