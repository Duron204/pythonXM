import cv2

# 1. 打开默认摄像头（0表示第一个摄像头）
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("无法打开摄像头！")
else:
    while True:
        # 2. 循环读取摄像头帧
        ret, frame = cap.read()
        if not ret:
            print("无法获取帧！")
            break

        # 3. 显示实时画面
        cv2.imshow('Camera', frame)

        # 4. 检测按键：ESC(27)退出，空格(32)保存
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == 32:
            cv2.imwrite('snapshot.jpg', frame)
            print("快照已保存为 snapshot.jpg")

    # 5. 释放资源
    cap.release()
    cv2.destroyAllWindows()