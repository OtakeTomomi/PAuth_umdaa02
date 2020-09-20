import pandas as pd

# data_event_change.csvの読み込み
df_e_change = pd.read_csv('orignal_data/data_event_change.csv')
print(df_e_change.head(16))

print(df_e_change.info())