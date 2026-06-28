import cv2

img = cv2.imread('../image/cat.jpg')
if img is None:
    print("无法读取图片！")
else:
    # 1. 裁剪左上角 200×200 区域（数组切片：[y范围, x范围]）
    crop_img = img[0:200, 0:200]

    # 2. 保存裁剪后的图片
    cv2.imwrite('crop.jpg', crop_img)
    print("裁剪图已保存为 crop.jpg")

    # 3. 显示原图和裁剪图
    cv2.imshow('Original', img)
    cv2.imshow('Cropped', crop_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()