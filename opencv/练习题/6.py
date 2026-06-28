import cv2
from datetime import datetime

# 1. 打开摄像头
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("无法打开摄像头！")
else:
    # 2. 获取摄像头参数，配置视频写入器
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 20.0
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 编码器
    out = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))

    name = "heshunqiang"  # 请替换为你的姓名

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 3. 获取当前时间，格式：YYYY-MM-DD HH:MM:SS
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 4. 计算文字位置（右下角）
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        (time_w, time_h), _ = cv2.getTextSize(time_str, font, font_scale, thickness)
        (name_w, name_h), _ = cv2.getTextSize(name, font, font_scale, thickness)

        text_x = width - max(time_w, name_w) - 10
        time_y = height - 10 - name_h - 5
        name_y = height - 10

        # 5. 绘制时间和姓名（白色）
        cv2.putText(frame, time_str, (text_x, time_y), font, font_scale, (255, 255, 255), thickness)
        cv2.putText(frame, name, (text_x, name_y), font, font_scale, (255, 255, 255), thickness)

        # 6. 写入视频并显示
        out.write(frame)
        cv2.imshow('Recording', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()