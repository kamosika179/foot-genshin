import socket
from datetime import datetime

# サーバのIPアドレスとポート番号
server_ip = '192.168.0.13'  # すべてのネットワークインターフェースにバインドする場合
server_port = 17900  # 任意のポート番号にゃ

# ソケットを作成する
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# サーバのIPアドレスとポート番号にバインドする
s.bind((server_ip, server_port))

# 接続待機する
s.listen(1)
print("クライアントの接続を待機中...")

# クライアントからの接続を受け入れる
client_socket, client_address = s.accept()
print("クライアントが接続されました。")

# データを保存するファイルを開く
filename = 'stand' #walk,jump,run,standのどれかにしてほしいかな
now = datetime.now()
with open(f'./data/{filename}{str(now)[-4:-1]}.txt', 'a') as file:
    while True:
        # クライアントからデータを受信する
        data = client_socket.recv(1024).decode('utf-8')

        # 受信したデータをファイルに書き込む
        # file.write(data + '\n')
        # file.flush()  # バッファをフラッシュしてデータを即座にファイルに書き込む
        # 受信したデータを表示する
        class_label_map = {'jump': "0", 'run': "1", 'stand': "2", 'walk': "3"}
        # class_label_mapから対応する文字列を取得して表示
        number = data
        #print(number)
        if number in class_label_map.values():
            label = list(class_label_map.keys())[list(class_label_map.values()).index(number)]
            print(label)
        else:
            print("Number not found in class_label_map")

# クライアントとの接続を閉じる
client_socket.close()

# サーバのソケットを閉じる
s.close()
