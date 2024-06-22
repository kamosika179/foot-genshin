import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# データが格納されているディレクトリパス
data_dir = 'data'

# 加速度データの読み込みと前処理
X = [] # 特徴量
y = [] # ラベル
window_size = 5  # 時間窓のサイズ

for filename in os.listdir(data_dir):
    if filename.startswith(('jump', 'run', 'stand', 'walk')) and filename.endswith('.txt'):
        with open(os.path.join(data_dir, filename), 'r') as file:
            lines = file.readlines()
            lines = lines[int(0.05 * len(lines)):-int(0.05 * len(lines))]  # 最初と最後の5%の行を除外
            datas = []
            for line in lines:
                try:
                    data = line.strip().split(',')
                    data = [float(x) for x in data]
                    if len(data) == 3:
                        datas.append(data)
                        # if filename.startswith('jump'):
                        #     y.append('jump')
                        # elif filename.startswith('run'):
                        #     y.append('run')
                        # elif filename.startswith('stand'):
                        #     y.append('stand')
                        # elif filename.startswith('walk'):
                        #     y.append('walk')
                except ValueError:
                    continue
            # 時系列を表すための次元を作る
            for i in range(len(datas) - window_size - 1):
                accs = datas[i:i + window_size] #複数の時間の加速度を取得する
                acc_data = []
                for acc in accs:
                    acc_data += acc
                X.append(acc_data)
                if filename.startswith('jump'):
                    y.append('jump')
                elif filename.startswith('run'):
                    y.append('run')
                elif filename.startswith('stand'):
                    y.append('stand')
                elif filename.startswith('walk'):
                    y.append('walk')

# データをNumPy配列に変換
X = np.array(X)
y = np.array(y)

# 訓練データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=42)

# 訓練データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=42)

# クラスラベルの辞書を作成
class_label_map = {'jump': 0.0, 'run': 1.0, 'stand': 2.0, 'walk': 3.0}

# ファイルに書き出す
with open('Xy_train.txt', 'w') as file:
    for i, row in enumerate(X_train):
        # 行の最初に「{」を追加
        file.write('{')

        # 各要素を書き出し
        for j, value in enumerate(row):
            file.write('%.2f' % value)
            # 要素の最後でなければ、","を追加
            if j < len(row) - 1:
                file.write(', ')

        # y_trainの値をクラスラベルに置き換えて書き出す
        class_label = y_train[i]
        if class_label in class_label_map:
            file.write(', %.1f' % class_label_map[class_label])
        else:
            # クラスラベルがマップに存在しない場合はエラーを出力して終了する
            print("Unknown class label:", class_label)
            exit(1)

        # 行の最後に「},」を追加
        file.write('},\n')

print("X_trainとy_trainの内容をファイルに書き出しましたにゃん♪")

# k近傍法（k-NN）モデルの定義と訓練
k = 3  # kの値（近傍点の数）
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X_train, y_train)

# テストデータで予測
y_pred = knn.predict(X_test)

# 混同行列を計算する
conf_matrix = confusion_matrix(y_test, y_pred)
print(conf_matrix)

# 分類レポートの表示
print(classification_report(y_test, y_pred))
