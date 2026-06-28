import cv2
import numpy as np

# 1. 读取包含蓝色物体的图片（如 opencv_logo.jpg）
img = cv2.imread('../image/cat.jpg')
if img is None:
    print("无法读取图片！")
else:
    # 2. 转换到 HSV 颜色空间（更易提取颜色）
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 3. 定义蓝色的 HSV 范围（H:100-124, S:43-255, V:46-255）
    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])

    # 4. 生成蓝色掩模（蓝色区域为白，其余为黑）
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # 5. 将蓝色区域替换为红色（BGR: (0,0,255)）
    result = img.copy()
    result[mask == 255] = (0, 0, 255)  # 掩模白色区域赋值红色

    # 6. 显示结果
    cv2.imshow('Original', img)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()