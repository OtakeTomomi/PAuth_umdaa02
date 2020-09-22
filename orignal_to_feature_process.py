"""
MATLABのコードをpythonに書き直さなければならない
参考：http://www.mariofrank.net/touchalytics/extractFeatures.m
MATLABは配列のインデックスがもしかして１はじまり？


使用されている端末は Nexus 5
137.84 × 69.17 × 8.59 mm


読み込むデータはストローク間時間の挙動？処理の仕方からみてユーザごと，
セッションごとが良いかも知れない


raw feature columns

0   index1         int64
1   index2         int64
2   eventTime      int64
3   USER           int64
4   SESSION        int64
5   eventPressure  float64
6   eventType      int64
7   positionX      int64
8   positionY      int64
9   tag            object


feature descriptors


"""

import pandas as pd
import numpy as np
import math

# read data
df = pd.read_csv('orignal_data/data_event_change.csv')
print(df.head())


def preprocess(df):
    df2 = df.copy()
    # convert ms to s
    df2.loc[:, 'eventTime'] = df2.loc[:, 'eventTime']/1000

    # flip sign of yaxis
    df2.loc[:, 'positionY'] = -df2.loc[:, 'positionY']

    # start counting from 1
    df2.loc[:, 'USER'] = df2.loc[:, 'USER'] + 1

    # global statistics
    indivPrctlVals = [20, 50, 80]

    # find beginning of strokes
    downInd = [i for i, x in enumerate(list(df2['eventType'])) if x == 0]

    # number of strokes
    Nstrokes = len(downInd)
    # downInd = [downInd; size(t, 1)]; # よくわからん

    # init feature output
    Nfeat = 35
    featMat = np.zeros([Nstrokes, Nfeat])
    featMat[:, :] = np.nan

    print(f'extracting features of  {Nstrokes}  strokes..')

    # extract features from each individual stroke
    for i in range(5):
        # ↑Nstrokes-1
        # strokeInd = df.loc[downInd(i):downInd(i + 1) - 1, :]
        x_stroke = df2.loc[downInd[i]:downInd[i + 1] - 1, :]

        # sanity check
        if df2.iloc[-1, 6] != 1:
            print(f'last point of stroke {i} is not "up"')
            continue

        # number of measurements of stroke
        npoints = len(x_stroke)

        # id stuff (do not use as features!)
        # user id
        featMat[i, 1] = x_stroke.iloc[1, 3]
        # session id
        featMat[i, 2] = x_stroke.iloc[1, 4]

        # features
        # convert from pixels to : ピクセルからmmへの変換
        # x_stroke[:, ['positionX', 'positionY']] = pixTommFac(featMat[i, 13]) * x_stroke[:, ['positionX', 'positionY'])
        x_stroke.loc[:, 'positionX'] = (1/445) * x_stroke.loc[:, 'positionX'] * 25.4
        x_stroke.loc[:, 'positionY'] = (1/445) * x_stroke.loc[:, 'positionY'] * 25.4

        # time to next stroke (0 if last stroke in dataset) : 次のストロークまでの時間 (データセット内の最後のストロークの場合は 0)
        # if last stroke in dset or last stroke of this user, set to Nan :
        # データセット内の一番最後もしくはユーザのなかでの最後のデータの場合は　NaN を代入
        if featMat[i, 3] == 0 || df2[downInd(i + 1), col_user] != featMat.iloc[i, 1]:
            featMat[i, 3] = 'NaN'
        else:
            featMat[i, 3] = df2(min([downInd(Nstrokes) downInd(i + 1)]), col_time) - x_stroke(1, col_time)

        # time to last point of this stroke : このストロークの最後のポイントまでの時間
        featMat[i, 4] = x_stroke.iloc[-1, 2] - x_stroke.iloc[0, 2]

        # x-pos start
        featMat[i, 5] = x_stroke.iloc[0, 7]
        # y-pos start
        featMat[i, 6] = x_stroke.iloc[0, 8]
        # x-pos end
        featMat[i, 7] = x_stroke.iloc[-1, 7]
        # y-pos start
        featMat[i, 8] = x_stroke.iloc[-1, 8]

        # full dist : 完全な歪み
        featMat[i, 9] = np.sqrt((featMat[i, 8] - featMat[i, 6]) ^ 2 + (featMat[i, 7] - featMat[i, 5]) ^ 2)

        # pairwise stuff→わからんので調査
        # x-displacement : X-変位
        xdispl = filter([1 - 1], 1, x_stroke.iloc[:, 7])
        xdispl[1] = []
        # y-displacement : Y-変位
        ydispl = filter([1 - 1], 1, x_stroke.iloc[:, 8])
        ydispl[1] = []

        # pairwise time diffs : ペアワイズ時間の差分
        tdelta = filter([1 - 1], 1, x_stroke[:, 2])
        tdelta[1] = []

        # pairw angle　: ペアの角度
        # (参考)https://mathwords.net/atan2
        angl = np.atan2[ydispl, xdispl]

        # Mean Resutlant Length (requires circular statistics toolbox)
        # 角度統計学あたりをみれば理解できそう…？
        # https://etiennecmb.github.io/brainpipe/_modules/brainpipe/stat/circstat.html
        import pingouin as pg
        featMat[i, 10] = pg.circ_r(angl)

        # pairwise displacements : ペアワイズ変位
        # C = sqrt(abs(A).^2 + abs(B).^2) は hypot(A, B)と同じ（matlab）
        # pairwDist = sqrt(xdispl.^2 + ydispl.^2);
        pairwDist = math.hypot(xdispl, ydispl)

        # speed histogram : 速度ヒストグラム



    print(df.head())
    print(downInd[:10])
    print(pd.DataFrame(featMat).head())


preprocess(df)
