import pandas as pd

df = pd.read_csv('MOCK_DATA.csv')
print(df.columns)
df = df[['transaction_date','transaction_amount','transaction_type','transaction_category','amount_before','amount_after','user']]
df = pd.get_dummies(df, columns=['transaction_type'])
print(df.head())
