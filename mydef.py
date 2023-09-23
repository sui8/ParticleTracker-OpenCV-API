import cv2
from matplotlib import pyplot as plt
import numpy as np
import datetime

# Tracker初期化
def initTracker(windowName, frame, selectedAlgorithm):

    # Tracker生成
    if selectedAlgorithm == 1:
        # MIL
        tracker = cv2.TrackerMIL_create()
        print("使用するアルゴリズム: MIL")

    elif selectedAlgorithm == 2:
        # DaSiamRPN
        params = cv2.TrackerDaSiamRPN_Params()
        params.model = "model/DaSiamRPN/dasiamrpn_model.onnx"
        params.kernel_r1 = "model/DaSiamRPN/dasiamrpn_kernel_r1.onnx"
        params.kernel_cls1 = "model/DaSiamRPN/dasiamrpn_kernel_cls1.onnx"
        tracker = cv2.TrackerDaSiamRPN_create(params)
        print("使用するアルゴリズム: DaSiamRPN")

    elif selectedAlgorithm == 3:
        # Nano
        params = cv2.TrackerNano_Params()
        params.backbone = "model/nanotrackv2/nanotrack_backbone_sim.onnx"
        params.neckhead = "model/nanotrackv2/nanotrack_head_sim.onnx"
        #params.backbone = "model/nanotrackv3/nanotrack_backbone_sim.onnx"
        #params.neckhead = "model/nanotrackv3/nanotrack_head_sim.onnx"
        tracker = cv2.TrackerNano_create(params)
        print("使用するアルゴリズム: Nano")

    else:
        # DaSiamRPN
        params = cv2.TrackerDaSiamRPN_Params()
        params.model = "model/DaSiamRPN/dasiamrpn_model.onnx"
        params.kernel_r1 = "model/DaSiamRPN/dasiamrpn_kernel_r1.onnx"
        params.kernel_cls1 = "model/DaSiamRPN/dasiamrpn_kernel_cls1.onnx"
        tracker = cv2.TrackerDaSiamRPN_create(params)
        print("使用するアルゴリズム: DaSiamRPN")
            

    # 関心領域指定
    while True:
        print("追跡範囲を指定してください")
        print("EnterまたはSpaceキーを押下して追跡を開始します")
        print("Escキーで終了します")
        target = cv2.selectROI(windowName, frame, showCrosshair=False)

        try:
            tracker.init(frame, target)

        except Exception as e:
            print(e)
            continue

        return tracker
    

# 粒子の中心(x, y)を求める
def calc_center(coodinates): # x左端(0), y上端(1), width(2), height(3) #cv2の仕様で座標が+1されているのでその分引いている
    x_center = round(coodinates[0] + (coodinates[2] - 1) / 2)
    y_center = round(coodinates[1] + (coodinates[3] - 1) / 2)
    return x_center, y_center


# グラフ描画
# 引数: list, list, str
def draw(x, y, path):
    
    fig, ax = plt.subplots()

    ax.plot(x, y) # グラフ描画
    xy_range = max(abs(min(x)), abs(max(x)), abs(min(y)), abs(max(y))) + 5 # グラフの範囲を決定
    ax.set_xlim(-xy_range, xy_range)                                       # x軸の数値(min,max)
    ax.set_ylim(-xy_range, xy_range)                                       # y軸の数値(min,max)
    ax.set_aspect("equal")                                                 # アスペクト比を1:1にする
    ax.grid(color = "gray", linestyle = "--")                              # 目盛り線を描画

    plt.savefig(f"{path}/Figure_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
    

# 距離の測定
def measure(x_list, y_list, particleMileageSum, scale_per_pxl): 
    width_x = (max(x_list) - min(x_list)) * scale_per_pxl
    width_y = (max(y_list) - min(y_list)) * scale_per_pxl
    particleMileageSum = particleMileageSum * scale_per_pxl

    print(f"移動距離: {particleMileageSum}")
    print(f"横幅: {width_x}")
    print(f"縦幅: {width_y}")
    

