import os
import sys
import cnn_model
import keras
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

# 入力と出力を指定
im_rows = 32 # 画像の縦ピクセル数
im_cols = 32 # 画像の横ピクセル数
im_color = 3 # 画像の色空間
in_shape = (im_rows, im_cols, im_color)
nb_classes = 8

# 写真データを読み込み
npz_file_path = sys.argv[1]
photos = np.load(npz_file_path)
x = photos['x']
y = photos['y']

# 読み込んだデータを三次元配列に変換
x = x.reshape(-1, im_rows, im_cols, im_color)
x = x.astype('float32') / 255
# ラベルデータをone-hotベクトルに直す
y = keras.utils.to_categorical(y.astype('int32'), nb_classes)

# 学習用とテスト用に分ける
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8)

# CNNモデルを取得
model = cnn_model.get_model(in_shape, nb_classes)

# 学習を実行
hist = model.fit(x_train, y_train, 
    batch_size=32,
    epochs=20,
    verbose=1,
    validation_data=(x_test, y_test))
# モデルを評価
score = model.evaluate(x_test, y_test, verbose=1)
print('正解率=', score[1], 'loss=', score[0])

# 学習の様子をグラフへ描画
# 正解率の推移をプロット
plt.plot(hist.history['accuracy'])
plt.plot(hist.history['val_accuracy'])
plt.title('Accuracy')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# ロスの推移をプロット
plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('Loss')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# モデルの重みを保存
weights_filename = 'photos-model-weights.hdf5'
weights_directory = os.path.join('.', 'weight')  # ディレクトリパス
os.makedirs(weights_directory, exist_ok=True)  # ディレクトリが存在しない場合に作成
weights_path = os.path.join(weights_directory, weights_filename)
model.save_weights(weights_path)

print('The weight file has been saved to', weights_path)