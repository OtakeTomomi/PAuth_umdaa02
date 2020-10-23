# PAuth_umdaa02

## データを収集している機器の情報

Nexus 5	        1080 x 1920	xxhdpi	360 x 640 

## 元データ
TrainEventDictionary_70.csv

### Columnの内訳
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 2754715 entries, 0 to 2754714
Data columns (total 10 columns):
    Column         Dtype
---  ------         -----
 0   index1         int64
 1   index2         int64
 2   eventTime      int64
 3   USER           object
 4   SESSION        object
 5   eventPressure  float64
 6   eventType      int64
 7   positionX      int64
 8   positionY      int64
 9   tag            object
dtypes: float64(1), int64(6), object(3)
memory usage: 210.2+ MB

 各Columnの説明もどき：
index1→SESSION内でのタッチデータの順番を表していると思われる
index2→各SESSON内のindexごとのデータの長さを表している感じがする
eventTime→時間
USER→ユーザ
SESSION→セッション
eventPressure→圧力かな？
eventType→532がtouch down, ５３３がmove finger on screen
positionX→位置ｘ
positionY→位置ｙ
tag →要らんというか全部０なので意味がない



### USERの詳細 :
{'Ph09USER001', 'Ph06USER005', 'Ph09USER003', 'Ph01USER001', 'Ph04USER002', 'Takeout', 'Ph06USER002', 'Ph05USER001',
'Ph01USER004', 'Ph04USER001', 'Ph02USER004', 'Ph02USER003', 'Ph06USER001', 'Ph09USER002', 'Ph05USER002', 'Ph04USER003',
'Ph05USER003', 'Ph10USER003', 'Ph08USER002', 'Ph06USER003', 'Ph02USER001', 'Ph05USER004', 'Ph02USER005', 'Ph10USER004',
'Ph03USER001', 'Ph03USER003', 'Ph08USER003', 'Ph03USER002', 'Ph09USER004', 'Ph10USER002', 'Ph04USER004', 'Ph01USER002',
'Ph08USER001', 'Ph10USER001', 'Ph02USER002', 'Ph01USER003'}

### USER情報の変更(object→int)
Ph01USER001 → 0 Ph01USER002 → 1 Ph01USER003 → 2 Ph01USER004 → 3 Ph02USER001 → 4 Ph02USER002 → 5 Ph02USER003 → 6
Ph02USER004 → 7 Ph02USER005 → 8 Ph03USER001 → 9 Ph03USER002 → 10 Ph03USER003 → 11 Ph04USER001 → 12 Ph04USER002 → 13
Ph04USER003 → 14 Ph04USER004 → 15 Ph05USER001 → 16 Ph05USER002 → 17 Ph05USER003 → 18 Ph05USER004 → 19 Ph06USER001 → 20
Ph06USER002 → 21 Ph06USER003 → 22 Ph06USER005 → 23 Ph08USER001 → 24 Ph08USER002 → 25 Ph08USER003 → 26 Ph09USER001 → 27
Ph09USER002 → 28 Ph09USER003 → 29 Ph09USER004 → 30 Ph10USER001 → 31 Ph10USER002 → 32 Ph10USER003 → 33 Ph10USER004 → 34
Takeout → 35
48人のユーザとあるがもしかするとTakeoutなかに13人分まとまっているのかもしれない




