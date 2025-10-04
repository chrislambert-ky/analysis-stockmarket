#!/usr/bin/env python3
"""Analyze why 4% and 5% dip levels didn't trigger for ALLY on 2015-09-01."""

# ALLY 2015-09-01 data from our historical file
prev_close = 16.95
open_price = 16.73
low_price = 16.10
close_price = 16.22

print("ALLY 2015-09-01 Buy-on-Dip Analysis")
print("=" * 50)
print(f"Previous Close: ${prev_close}")
print(f"Open: ${open_price}")
print(f"Low: ${low_price}") 
print(f"Close: ${close_price}")
print()

print("Buy-on-Dip Trigger Analysis (CORRECTED - From Previous Close):")
print("-" * 55)

# Our current dip levels from the ETL
dip_levels = [0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.90]

for i, level in enumerate(dip_levels):
    pct = (1 - level) * 100
    target_price = prev_close * level  # CHANGED: Use previous close instead of open
    triggered = low_price <= target_price
    
    print(f"{pct:2.0f}% dip: Prev Close ${prev_close} × {level} = ${target_price:.2f}")
    print(f"      Low ${low_price} <= ${target_price:.2f}? {triggered}")
    if triggered:
        print(f"      ✅ TRIGGERED - Should buy 1 share at ${target_price:.2f}")
    else:
        print(f"      ❌ NOT TRIGGERED")
    print()

print("Summary:")
print(f"Max decline from open: {((low_price - open_price) / open_price) * 100:.2f}%")
print(f"Max decline from prev close: {((low_price - prev_close) / prev_close) * 100:.2f}%")
