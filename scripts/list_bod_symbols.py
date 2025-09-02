import pandas as pd
p='data/all_buy_on_dip.csv'
df=pd.read_csv(p)
print('rows',len(df))
syms=sorted(df['Symbol'].unique())
print(len(syms),'symbols')
print(','.join(syms))
