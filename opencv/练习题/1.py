import cv2
# 题1：图像读取与信息打印
# 编写程序读取一张彩色图片（image.jpg），完成以下操作：
# 打印图片的 shape、size、dtype
# 打印图片左上角第一个像素的 BGR 值
# 显示图片，按任意键关闭窗口
# 提醒
# 使用 cv2.imread()、cv2.imshow()、cv2.waitKey()

# 读取图片（请确保 image.jpg 在当前目录，或修改为绝对路径）
img = cv2.imread('../image/cat.jpg')
if img is None:
    print("无法读取图片，请检查路径！")
else:
    # 1. 打印图像基本信息
    print(f"图像形状 (shape): {img.shape}")    # (高度, 宽度, 通道数)
    print(f"像素总数 (size): {img.size}")       # 高度×宽度×通道数
    print(f"数据类型 (dtype): {img.dtype}")     # uint8（0-255）

    # 2. 打印左上角第一个像素的 BGR 值
    b, g, r = img[0, 0]
    print(f"左上角像素 BGR: B={b}, G={g}, R={r}")

    # 3. 显示图片（按任意键关闭窗口）
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()