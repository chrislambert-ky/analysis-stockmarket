#!/usr/bin/env python3
"""Compare different week numbering systems."""

from datetime import datetime

test_dates = [
    '2015-12-28', '2015-12-29', '2015-12-30', '2015-12-31',
    '2016-01-01', '2016-01-04',
    '2020-12-28', '2020-12-29', '2020-12-30', '2020-12-31',
    '2021-01-01', '2021-01-04'
]

print("Week Numbering Comparison:")
print("=" * 80)
print(f"{'Date':<12} {'ISO Week':<10} {'Simple Week':<12} {'US Week':<10} {'Weekday'}")
print("-" * 80)

for date_str in test_dates:
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    
    # ISO week (current method)
    iso_week = dt.isocalendar().week
    
    # Simple week (day of year / 7)
    simple_week = (dt.timetuple().tm_yday - 1) // 7 + 1
    
    # US week (starts Sunday)
    us_week = int(dt.strftime('%U'))
    
    weekday = dt.strftime('%A')
    
    print(f"{date_str:<12} {iso_week:<10} {simple_week:<12} {us_week:<10} {weekday}")
