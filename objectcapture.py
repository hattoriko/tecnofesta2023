import cv2
import numpy as np

# カメラのキャプチャを開始
cap = cv2.VideoCapture(0)

# 1つ前のフレームの座標を初期化
prev_x, prev_y = 0, 0

# ループを開始
while True:
    # 新しいフレームを取得
    ret, frame = cap.read()

    # BGR形式からHSV形式に変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 赤い色の範囲を定義（OpenCVではHSV形式を使用）
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # 赤い色の領域を抽出
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # マスクを使用して元の画像から赤い色の部分だけを抽出
    red_object = cv2.bitwise_and(frame, frame, mask=mask)

    # 輪郭を検出
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 最大面積の輪郭を見つける
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(max_contour)

        # 輪郭の中心座標を計算
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # 速度の計算（前フレームとの差分）
        velocity_x = cx - prev_x
        velocity_y = cy - prev_y

        # 方向の計算（atan2を使用）
        angle_rad = np.arctan2(velocity_y, velocity_x)
        angle_deg = np.degrees(angle_rad)

        # 結果を表示
        print(f"速度: ({velocity_x}, {velocity_y}), 方向: {angle_deg}")

        # 1つ前の座標を更新
        prev_x, prev_y = cx, cy

    # 結果を表示
    cv2.imshow("Original", frame)
    cv2.imshow("Red Object", red_object)

    # 'q'キーが押されたら終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# キャプチャを解放
cap.release()
cv2.destroyAllWindows()
