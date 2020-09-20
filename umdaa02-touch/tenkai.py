import pickle
import pandas as pd


# df.to_pickle('TrainEventDictionary_70.pkl')

df_from_pkl = pd.read_pickle('TrainEventDictionary_70.pkl')

print(df_from_pkl)
print(df_from_pkl.index)

