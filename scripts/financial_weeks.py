#!/usr/bin/env python3
"""Financial market week numbering standards research."""

from datetime import datetime, timedelta

def financial_week_examples():
    """Show how different financial systems handle week numbering."""
    
    print("Financial Market Week Numbering Standards:")
    print("=" * 60)
    
    # Test the problematic dates
    test_dates = [
        ('2015-12-28', 'Monday - End of 2015'),
        ('2015-12-31', 'Thursday - Last day of 2015'), 
        ('2016-01-01', 'Friday - First day of 2016'),
        ('2016-01-04', 'Monday - First Monday of 2016'),
        ('2020-12-28', 'Monday - End of 2020'),
        ('2020-12-31', 'Thursday - Last day of 2020'),
        ('2021-01-01', 'Friday - First day of 2021'),
        ('2021-01-04', 'Monday - First Monday of 2021')
    ]
    
    print(f"{'Date':<12} {'Description':<25} {'ISO':<5} {'US':<5} {'Simple':<7} {'Financial'}")
    print("-" * 80)
    
    for date_str, desc in test_dates:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        
        # ISO week (Monday start, can have 53 weeks)
        iso_week = dt.isocalendar().week
        
        # US week (Sunday start)
        us_week = int(dt.strftime('%U'))
        
        # Simple week (1-52 based on day of year)
        simple_week = min(52, (dt.timetuple().tm_yday - 1) // 7 + 1)
        
        # Financial week (Monday start, but reset at year boundary)
        # Find first Monday of the year
        jan_1 = datetime(dt.year, 1, 1)
        days_since_jan_1 = (dt - jan_1).days
        # If Jan 1 is Monday (0), first Monday is Jan 1
        # If Jan 1 is Tue-Sun (1-6), first Monday is Jan 1 + (7 - weekday)
        if jan_1.weekday() == 0:
            first_monday = jan_1
        else:
            first_monday = jan_1 + timedelta(days=(7 - jan_1.weekday()))
        
        if dt >= first_monday:
            financial_week = ((dt - first_monday).days // 7) + 1
        else:
            # Before first Monday, belongs to previous year's last week
            financial_week = 1
            
        financial_week = min(52, financial_week)  # Cap at 52
        
        print(f"{date_str:<12} {desc:<25} {iso_week:<5} {us_week:<5} {simple_week:<7} {financial_week}")

if __name__ == "__main__":
    financial_week_examples()
    
    print("\n" + "=" * 60)
    print("FINANCIAL INDUSTRY STANDARDS:")
    print("=" * 60)
    
    print("🏦 NORTH AMERICAN MARKETS:")
    print("   • US/Canada: Often use Sunday-start weeks (%U format)")
    print("   • Trading week: Monday-Friday")
    print("   • Reporting: Calendar weeks, typically 52 weeks per year")
    
    print("\n🌍 EUROPEAN MARKETS:")
    print("   • EU: ISO 8601 standard (Monday-start, can have 53 weeks)")
    print("   • London Stock Exchange: ISO weeks")
    print("   • Frankfurt/Paris: ISO weeks")
    
    print("\n📊 INVESTMENT ANALYSIS:")
    print("   • DCA Analysis: Often uses 'investment weeks' (52 per year)")
    print("   • Portfolio Reporting: Calendar years with 52 weeks")
    print("   • Risk Management: ISO weeks for precise dating")
    
    print("\n💡 RECOMMENDATIONS:")
    print("   • For DCA/Investment: Use 52-week financial calendar")
    print("   • For Compliance: Use ISO weeks (current approach)")
    print("   • For US Clients: Consider Sunday-start weeks")
    
    print("\n🎯 YOUR CURRENT APPROACH:")
    print("   • ISO weeks (Monday start, 53 weeks possible)")
    print("   • ✅ Correct for international standards")
    print("   • ✅ Aligns with Monday DCA purchases")
    print("   • ⚠️  May confuse users expecting exactly 52 weeks")
