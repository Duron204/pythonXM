import cv2

# 1. 打开本地视频文件（请确保 test.mp4 存在）
cap = cv2.VideoCapture('../image/保护校花.mp4')
if not cap.isOpened():
    print("无法打开视频文件！")
else:
    # 2. 获取视频帧率，计算每帧等待时间
    fps = cap.get(cv2.CAP_PROP_FPS) or 30  # 防止获取失败，默认30fps
    delay = int(1000 / fps)

    paused = False  # 暂停状态标志
    while True:
        # 3. 非暂停状态时读取新帧
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break  # 视频播放完毕

        # 4. 显示帧（暂停时保持最后一帧）
        cv2.imshow('Video', frame)

        # 5. 检测按键：ESC退出，空格切换暂停
        key = cv2.waitKey(delay) & 0xFF
        if key == 27:
            break
        elif key == 32:
            paused = not paused
            print("暂停" if paused else "继续")

    cap.release()
    cv2.destroyAllWindows()