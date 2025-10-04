import pandas as pd
v2 = pd.read_csv('data/all_buy_on_dip.csv')
print('v2 columns:', list(v2.columns))
print('rows:', len(v2))
if 'Buy_Level' in v2.columns:
    print('Buy_Level dtype:', v2['Buy_Level'].dtype)
    print('Buy_Level unique sample:', sorted(v2['Buy_Level'].dropna().unique())[:20])
else:
    print('Buy_Level missing')
print('Date column sample:', v2['Date'].astype(str).head(5).tolist())
print('Executed_Price sample:', v2.get('Executed_Price').head(5).tolist())
