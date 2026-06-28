import cv2
import numpy as np

img = cv2.imread('../image/cat.jpg')
if img is None:
    print("无法读取图片！")
else:
    h, w = img.shape[:2]

    # 1. 创建掩模：全黑，中央 200×200 设为白色（255）
    mask = np.zeros((h, w), dtype=np.uint8)
    start_x, start_y = (w - 200) // 2, (h - 200) // 2
    mask[start_y:start_y+200, start_x:start_x+200] = 255

    # 2. 按位运算
    and_result = cv2.bitwise_and(img, img, mask=mask)  # 与运算
    or_result = cv2.bitwise_or(img, img, mask=mask)    # 或运算
    xor_result = cv2.bitwise_xor(img, img, mask=mask)  # 异或运算

    # 3. 显示结果
    cv2.imshow('Original', img)
    cv2.imshow('Mask', mask)
    cv2.imshow('bitwise_and', and_result)
    cv2.imshow('bitwise_or', or_result)
    cv2.imshow('bitwise_xor', xor_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 4. 差异解释
    print("💡 按位运算结果差异：")
    print("• bitwise_and：仅掩模白色区域保留原图，其余变黑（提取中央区域）；")
    print("• bitwise_or：掩模白色区域变白，其余保留原图；")
    print("• bitwise_xor：掩模白色区域原图反色，其余保留原图。")