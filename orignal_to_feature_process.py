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
from scipy import signal

# read data
df = pd.read_csv('orignal_data/data_event_change.csv')
print(df.head())


def preprocess(df):
    df2 = df.copy()
    # convert ms to s
    df2.loc[:, 'eventTime'] = df2.loc[:, 'eventTime']/1000

    # flip sign of y_axis
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
    Nfeat = 30
    featMat = np.zeros([Nstrokes, Nfeat])
    featMat[:, :] = np.nan

    print(f'extracting features of  {Nstrokes}  strokes..')

    # 実際は5→Nstrokesだがmatlabとインデックスの違いがありそうなので要確認
    # extract features from each individual stroke
    for i in range(5):
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
        featMat[i, 1] = x_stroke.iloc[0, 3]
        # session id
        featMat[i, 2] = x_stroke.iloc[0, 4]

        # features
        # convert from pixels to : ピクセルからmmへの変換
        # x_stroke[:, ['positionX', 'positionY']] = pixTommFac(featMat[i, 13]) * x_stroke[:, ['positionX', 'positionY'])
        x_stroke.loc[:, 'positionX'] = (1/445) * x_stroke.loc[:, 'positionX'] * 25.4
        x_stroke.loc[:, 'positionY'] = (1/445) * x_stroke.loc[:, 'positionY'] * 25.4

        # TODO: 動作確認未完了
        # time to next stroke (0 if last stroke in data_set) : 次のストロークまでの時間 (データセット内の最後のストロークの場合は 0)
        # if last stroke in data_set or last stroke of this user, set to Nan :
        # データセット内の一番最後もしくはユーザのなかでの最後のデータの場合は　NaN を代入
        if featMat[i, 3] == 0 or df2.loc[downInd[i+1], 'USER'] != featMat[i, 1]:
            featMat[i, 3] = 'NaN'
        else:
            featMat[i, 3] = df2.loc[min([downInd[Nstrokes], downInd[i + 1]]), 'eventTime'] - x_stroke.iloc[0, 2]

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
        featMat[i, 9] = np.sqrt((featMat[i, 8] - featMat[i, 6]) ** 2 + (featMat[i, 7] - featMat[i, 5]) ** 2)

        # TODO: 動作確認未完了
        # pairwise stuff→わからんので調査
        # x-displacement : X-変位
        xdispl = signal.lfilter(x_stroke[0:-1], 1, x_stroke.iloc[:, 7])
        # xdispl[1] = []
        # y-displacement : Y-変位
        ydispl = signal.lfilter(x_stroke[0:-1], 1, x_stroke.iloc[:, 8])
        # ydispl[1] = []

        # TODO: 動作確認未完了
        # pairwise time diffs : ペアワイズ時間の差分
        tdelta = signal.lfilter(x_stroke[0:-1], 1, x_stroke[:, 2])
        # tdelta[1] = []

        # TODO: 動作確認未完了
        # pairw angle　: ペアの角度
        # (参考)https://mathwords.net/atan2
        angl = np.atan2[ydispl, xdispl]

        # TODO: 動作確認未完了
        # Mean Resutlant Length (requires circular statistics toolbox)
        # 角度統計学あたりをみれば理解できそう…？
        # https://etiennecmb.github.io/brainpipe/_modules/brainpipe/stat/circstat.html
        # もしくはhttps://etiennecmb.github.io/brainpipe/_modules/brainpipe/stat/circstat.html
        import pingouin as pg
        featMat[i, 10] = pg.circ_r(angl)

        # TODO: 動作確認未完了
        # pairwise displacements : ペアワイズ変位
        # C = sqrt(abs(A).^2 + abs(B).^2) は hypot(A, B)と同じ（matlab）
        # pairwDist = sqrt(xdispl.^2 + ydispl.^2);
        pairwDist = math.hypot(xdispl, ydispl)

        # TODO: 動作確認未完了
        # speed histogram : 速度ヒストグラム
        v = pairwDist / tdelta
        featMat[i, 14:17] = np.percentile(v, indivPrctlVals, interpolation='midpoint')

        # TODO: 動作確認未完了
        # acceleration histogram : 加速度ヒストグラム
        a = signal.lfilter(v[0:-1], 1, v)
        a = a / tdelta
        # a[1] = []

        # TODO: 動作確認未完了
        # full stat stuff
        # numpyとmatlabでデフォルトのinterpolationが異なるっぽい
        # https://www.366service.com/jp/qa/e6eff47abbdd4bce6f0d93320f98aad3
        featMat[i, 17:20] = np.percentile(a, indivPrctlVals, interpolation='midpoint')

        # TODO: 未修正
        # median velocity of last 3 points : 最後の3点の中央値速度
        featMat[i, 20] = np.median(v[max(-4, 0):-1])

        # TODO: 動作確認未完了
        # max dist. beween direct line and true line (with sign):直線と真線の最大距離（符号あり
        xvek = x_stroke.iloc[:, 7] - x_stroke.iloc[0, 7]
        yvek = x_stroke.iloc[:, 8] - x_stroke.iloc[0, 8]

        # TODO: 不明
        # project each vector on straight line : 各ベクトルを直線上に投影
        # compute unit line perpendicular to straight connection and project on this
        # 直線接続に垂直な単位線を計算して、投影
        perVek = np.cross([xvek[-1], yvek[-1], 0], [0, 0, 1])
        perVek = perVek / np.sqrt([perVek[0], perVek[1]] * [perVek[0], perVek[1]])
        perVek[math.isnan(perVek)] = 0
        # happens if vectors have length 0

        # TODO: 動作確認未完了
        # all distances to direct line:直線までの全距離
        projectOnPerpStraight = (xvek * np.repmat(perVek(1), [len(xvek), 1]) +
                                 yvek * np.repmat(perVek(2), [len(xvek), 1]))

        # TODO: findの調査
        # report maximal (absolute) distance: 最大(絶対)距離を報告
        absProj = abs(projectOnPerpStraight)
        maxind = np.where(absProj == max(absProj))
        featMat[i, 21] = projectOnPerpStraight(maxind[0])

        # TODO: 動作確認未完了
        # stat of distances (bins are not the same for all strokes):距離の統計量 (ビンはすべてのストロークで同じではない)
        featMat[i, 22:25] = np.percentile(projectOnPerpStraight, indivPrctlVals, interpolation='midpoint')

        # TODO: 動作確認未完了
        # average direction of ensemble of pairs: ペアのアンサンブルの平均方向
        featMat[i, 25] = pg.circ_r(angl)

        # TODO: 動作確認未完了
        # direction of end-to-end line: 端から端までの直線の方向
        featMat[i, 12] = np.atan2((featMat[i, 8] - featMat[i, 6]), (featMat[i, 7] - featMat[i, 5]))

        # direction flag 1 up, 2 down, 3 left 4 right  (see doc atan2): in what direction is screen being moved to?
        # 方向フラグ 1 上向き，2 下向き，3 左向き，4 右向き:画面はどの方向に移動しているか
        # TODO: 動作確認未完了
        # convert to [0 2pi]
        tmpangle = featMat[i, 12] + math.pi
        if tmpangle <= (math.pi / 4):
            # right
            featMat[i, 11] = 4
        elif (tmpangle > math.pi/4) and (tmpangle <= 5*math.pi/4):
            # up or left
            if tmpangle < 3 * math.pi / 4:
                # up
                featMat[i, 11] = 1
            else:
                # left
                featMat[i, 11] = 2
        else:
            # down or right
            if tmpangle < 7*math.pi/4:
                # down
                featMat[i, 11] = 3
            else:
                # right
                featMat[i, 11] = 4

        # TODO: 動作確認未完了
        # length of trajectory : 軌跡の長さ
        featMat[i, 26] = sum(pairwDist)

        # TODO: 動作確認未完了
        # ratio between direct length and length of trajectory : 直接の長さと軌道の長さの比
        featMat[i, 27] = featMat[i, 9] / featMat[i, 26]

        # TODO: 動作確認未完了
        # average velocity : 平均速度
        featMat[i, 28] = featMat[i, 26] / featMat[i, 4]

        # TODO: 動作確認未完了
        # average acc over first 5 points : 最初の 5 ポイントの平均アクセント
        featMat[i, 29] = np.median(a[0:min(5, len(a))])

        # TODO: 動作確認未完了
        # pressure in the middle of the stroke: ストロークの途中の圧力
        featMat[i, 30] = np.median(x_stroke.loc[np.floor(npoints / 2):np.ceil(npoints / 2), 'eventPressure'])

    print(df.head())
    print(downInd[:10])
    print(pd.DataFrame(featMat).head())

    # delete NaNs
    # featMat(np.isnan(featMat(:, 1)),:) = []


preprocess(df)
