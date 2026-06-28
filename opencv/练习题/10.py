import cv2
import numpy as np

# 1. 读取两张图片（确保高度相同，否则先统一高度）
img1 = cv2.imread('../image/cat.jpg')
img2 = cv2.imread('../image/dog.png')
if img1 is None or img2 is None:
    print("无法读取图片！")
else:
    # 2. 统一高度（将 img2 高度调整为与 img1 一致）
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    if h1 != h2:
        img2 = cv2.resize(img2, (w2, h1))

    overlap = 100  # 重叠区域宽度（可调整）
    output_w = w1 + w2 - overlap
    output = np.zeros((h1, output_w, 3), dtype=np.uint8)

    # 3. 左边部分：img1 的前 w1-overlap 列
    output[:, :w1 - overlap] = img1[:, :w1 - overlap]

    # 4. 重叠区域：线性加权混合（img1 权重从1→0，img2 从0→1）
    for i in range(overlap):
        alpha = 1 - (i / overlap)
        beta = i / overlap
        output[:, w1 - overlap + i] = cv2.addWeighted(
            img1[:, w1 - overlap + i], alpha,
            img2[:, i], beta, 0
        )

    # 5. 右边部分：img2 的 overlap 之后的列
    output[:, w1:] = img2[:, overlap:]

    # 6. 显示并保存结果
    cv2.imshow('Stitched Image', output)
    cv2.imwrite('stitched.jpg', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()