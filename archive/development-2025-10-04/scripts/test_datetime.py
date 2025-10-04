#!/usr/bin/env python3
"""Test script to verify datetime library date extraction."""

import pandas as pd
from datetime import datetime

# Test with a small sample
test_dates = ['2015-08-31', '2015-09-01', '2015-09-02', '2015-09-03', '2015-09-04']

print("Testing datetime library for date component extraction:")
print("=" * 60)

for date_str in test_dates:
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    
    print(f"Date: {date_str}")
    print(f"  Year: {dt.year}")
    print(f"  Month: {dt.month}")
    print(f"  Week of Year: {dt.isocalendar().week}")
    print(f"  Weekday: {dt.strftime('%A')}")
    print(f"  Weekday Number: {dt.weekday()} (0=Monday)")
    print()

print("Datetime library working correctly!")
