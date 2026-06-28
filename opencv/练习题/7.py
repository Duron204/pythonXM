import cv2
import numpy as np

# 1. 读取两张图片（请确保 image1.jpg、image2.jpg 存在）
img1 = cv2.imread('../image/cat.jpg')
img2 = cv2.imread('../image/dog.png')
if img1 is None or img2 is None:
    print("无法读取图片！")
else:
    # 2. 统一调整为 500×400 尺寸（注意：cv2.resize 参数是 (宽度, 高度)）
    size = (500, 400)
    img1_resized = cv2.resize(img1, size)
    img2_resized = cv2.resize(img2, size)

    # 3. cv2.add() 直接相加（饱和运算：超过255截断为255）
    add_result = cv2.add(img1_resized, img2_resized)

    # 4. cv2.addWeighted() 加权混合（比例 0.6:0.4）
    blend_result = cv2.addWeighted(img1_resized, 0.6, img2_resized, 0.4, 0)

    # 5. 显示结果
    cv2.imshow('cv2.add Result', add_result)
    cv2.imshow('cv2.addWeighted Result', blend_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 6. 原因说明
    print("💡 cv2.add() 结果偏亮的原因：")
    print("cv2.add() 是**饱和运算**，两像素值之和超过255时会被截断为255（白色）；")
    print("而 cv2.addWeighted() 是按比例加权求和，结果更柔和，因此直接相加整体更亮。")