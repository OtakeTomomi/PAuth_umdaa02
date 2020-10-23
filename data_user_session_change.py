"""
TrainEventDictionary_70.csvのUSERとSESSIONを数値データに変更する
出力はdata_user_session_change.csv

手順的に１
"""
import pandas as pd
import pickle
# import os

from tqdm import tqdm
# import time


# データの読み込み
df_ori = pd.read_csv('umdaa02-touch/TrainEventDictionary_70.csv')
# print(df_ori.head(16))


# 各Columnに含まれる値？を確認
# USERでデータを分けたいのでユーザのリストを作成
print(f"USER : \n{set(df_ori['USER'])}")
user_list = list(set(df_ori['USER']))

# index1と関連してそうなのは分かった
print(f"SESSION : \n{set(df_ori['SESSION'])}")
session_list = list(set(df_ori['SESSION']))

# 要らない→{532, 533}
print(f"eventType : \n{set(df_ori['eventType'])}")
# 要らない→{'O'}
print(f"tag : \n{set(df_ori['tag'])}")


# user_listを保存
with open('data_info/user_list.binaryfile', 'wb') as web:
    pickle.dump(user_list, web)

# session_listを保存
with open('data_info/session_list.binaryfile', 'wb') as web:
    pickle.dump(session_list, web)


# 実行時間25分かかるので要注意
# SESSIONとUSERを番号で振り分けていく
def df_session_user_replace(df, session_ls, user_ls):
    df_ori2 = df.copy()
    session_list_sort = sorted(session_ls)
    print(session_list_sort[-1])
    user_list_sort = sorted(user_ls)
    for i, session in tqdm(enumerate(session_list_sort)):
        print(f'{session} → {i}')
        df_ori2 = df_ori2.replace(session, i)

    for i, user in tqdm(enumerate(user_list_sort)):
        print(f'{user} → {i}')
        df_ori2 = df_ori2.replace(user, i)

    return df_ori2


# 実行
df_ori2 = df_session_user_replace(df_ori, session_list, user_list)

# data_user_session_change.csvへ書き出し
df_ori2.to_csv('orignal_data/data_user_session_change.csv', index=False)
print(df_ori2.head())


# この時点でorignalデータに含まれていた文字列は全て数値データに変換されたはず
# Typeもしくはdiscribeで確認が必要
# orignal_data/user_ID_data内にはuserIDごとにデータを分割して保存済み
# 全体のデータとしてはdata_user_session_change.csvを参照
# これをtestデータにも適用する必要がある
# メモリ〜は2500だと足りないのでそれ以上にする必要がある気もする


"""
# USERを利用してユーザごとにデータの切り分け
def user_split(df_ori):
    for user in tqdm(user_list):
        df_ori_user = df_ori[df_ori['USER'].isin([user])]
        df_ori_user.to_csv(f'orignal_data/user_data/{user}.csv', index=False)

# user_split(df_ori)
"""
