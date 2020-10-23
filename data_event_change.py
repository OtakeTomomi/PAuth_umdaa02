"""
手順としては２
data_user_session_change.pyでUSERとSESSIONの値を数値に変換したdata_user_session_change.csvを使用
ここではeventTypeの変更を行う
eventTypeの説明
532:touch down
533:move finger on screen

これを
touch down : 0
touch up : 1
move finger on screen : 2
のように値を変更する
frank datasetにおけるactionのようにする

出力はdata_event_change.csv(全体)

ここでorignalデータを元に特徴抽出するための処理はいったん完了するのでUSERの値を元にデータの切り分けを行う
保存先はorignal_data/train_ori_pre/user*_pre.csv
"""


import pandas as pd
from tqdm import tqdm
import os

# データの読み込み
df = pd.read_csv('orignal_data/data_user_session_change.csv')
# print(df.describe())
print(df.info())

# touch_eventの変換表
'''
0:touch down
1:touch up
2:move finger on screen
'''
print(df.head(16))


def touch_event(df):
    '''touch_event
    :param df: data_user_session_change.csv
    :return: eventTypeの532を0,533を2に書き換えたデータ
    '''
    df2 = df.copy()
    df2['eventType'] = df2['eventType'].replace(532, 0)
    df2['eventType'] = df2['eventType'].replace(533, 2)
    return df2


# touch_eventの実行
df2 = touch_event(df)

# touch up部分を1に書き換えるための処理→現在のeventTypeが2で次の行のeventTypeの値が0であれば値を1に書き換え
#  2754714/2754714 [1:03:59<00:00, 717.38it/s]
# リスト作ったんだからそれ使えばよかったのに...
for i in tqdm(range(len(df2)-1)):
    if df2.iloc[i, 6] == 2 and df2.iloc[i+1, 6] == 0:
        df2.loc[i, 'eventType'] = 1

# 一番最後の行だけは次の値に0がないため個別に書き換え
df2.loc[len(df2)-1, 'eventType'] = 1


# touch upのリストを使用した場合(このリストは一番最後の値も追加済み)未実行なので動くかはわからない
# tu_list = list(pd.read_csv('data_info/touch_up_list_train.csv'))
# for i in tqdm(tu_list):
#     df2.loc[i, 'eventType'] = 1

# data_event_change.csvに保存
df2.to_csv('orignal_data/data_event_change.csv', index=False)
# eventTypeが変更されているか確認
print(df2.head(16))
# 一番最後のeventTypeの値が1に変更されているかの確認
print(df2.tail())


# data_event_change.csvの読み込み
df_e_change = pd.read_csv('orignal_data/data_event_change.csv')
print(df_e_change.head(16))

# ディレクトリの作成
path = 'orignal_data/train_ori_pre'
os.makedirs(path, exist_ok=True)

# userのIDでデータの切り分けを行い保存
for i in tqdm(range(36)):
    df_us_change2 = df_e_change.query(f'USER == {i}')
    df_us_change2.to_csv(f'orignal_data/train_ori_pre/user{i}_pre.csv', index=False)
