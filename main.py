

import cv2
import numpy as np
import mydef
import datetime


# 単位変換 1目盛りは10μm 
pxl = 115
# 1目盛りに対するピクセル数
scale_per_pxl = 10 / pxl

videoPath = "video/ptl.mp4"
savePath = "result"
windowName = "Tracker"
sum_dist = 0
x_list = []
y_list = []


print("アルゴリズムを選択してください")
print("1: MIL  2: DaSiamRPN  3: Nano")
selectedAlgorithm = int(input("> "))

# カメラ準備
cap = cv2.VideoCapture(videoPath)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)


# Tracker初期化
cv2.namedWindow(windowName)

isFrameLoaded, frame = cap.read()

if isFrameLoaded == False:
    print("[Error] 動画の読み込みに失敗しました")
    exit(0)

tracker = mydef.initTracker(windowName, frame, selectedAlgorithm)


# 稼働開始
while cap.isOpened():
    isFrameLoaded, frame = cap.read()

    if isFrameLoaded == False:
        print("追跡が終了しました")
        mydef.measure(x_list, y_list, sum_dist, scale_per_pxl) # 距離出力

        # 画像とグラフ保存処理
        answer = input("画像とグラフを保存しますか [y/n]: ")
        
        if answer == "y":
            cv2.imwrite(f"{savePath}/Ptl_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg", frame_prev) # 前フレームの画像保存

            x_after = []
            y_after = []

            # 最初の座標を原点にして、移動距離リスト生成
            for i in range(len(x_list)):
                x_after.append(x_list[i] - x_list[0])
                y_after.append(-(y_list[i] - y_list[0])) # x軸対称で反転

            mydef.draw(x_after, y_after, savePath)

            print("> 保存が完了しました")
            
        break

    frame_prev = frame.copy()

    # 追跡アップデート
    isOK, target = tracker.update(frame)
    
    if isOK == True:
        # 追跡後のボックス描画
        box = []
        box.append(int(target[0]))
        box.append(int(target[1]))
        box.append(int(target[2]))
        box.append(int(target[3]))
        cv2.rectangle(frame_prev, box, [0, 0, 255], thickness=1)

        track_x, track_y = mydef.calc_center(box)

        if len(x_list) < 1:
            x_list.append(track_x)
            y_list.append(track_y)
            
        # 移動距離をsum_distに加算
        sum_dist += np.round(np.linalg.norm(np.array([x_list[-1], y_list[-1]]) - np.array([track_x, track_y])), 2)
                
        # 粒子の現在地をリストに追加
        x_list.append(track_x)
        y_list.append(track_y)
        cv2.drawMarker(frame, (track_x, track_y), (255, 0, 255), markerSize=5)

        
        # 軌跡の点を直線で結ぶ
        for i in range(1, len(x_list)):
            cv2.line(frame_prev, (x_list[i-1], y_list[i-1]), (x_list[i], y_list[i]), (255, 0, 0))

    
        
    cv2.imshow(windowName, frame_prev)

    key = cv2.waitKey(1)
    if key == 32:  # SPACE
        # 追跡対象再指定
        tracker = mydef.initTracker(windowName, frame, selectedAlgorithm)
        
    #Escで終了
    if key == 27:
        mydef.measure(x_list, y_list, sum_dist, scale_per_pxl) # 移動距離計算
        break
    

cv2.destroyAllWindows()
print("追跡を終了しました。")

if len(x_list) > 1:
    # 画像とグラフ保存処理
    answer = input("画像とグラフを保存しますか [y/n]: ")
            
    if answer == "y":
        cv2.imwrite(f"{savePath}/Ptl_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg", frame_prev) # 前フレームの画像保存

        x_after = []
        y_after = []

        # 最初の座標を原点にして、移動距離リスト生成
        for i in range(len(x_list)):
            x_after.append(x_list[i] - x_list[0])
            y_after.append(-(y_list[i] - y_list[0])) # x軸対称で反転

        mydef.draw(x_after, y_after, savePath)

    print("保存が完了しました")
