import cv2
import numpy as np


# ============================================================
# 一、膨胀与腐蚀的对比实验
# ============================================================

def part1():
    """膨胀与腐蚀对比实验"""
    img1 = cv2.imread('opencv/image/dg.jpg')
    img2 = cv2.imread('opencv/image/by.jpg')

    if img1 is None or img2 is None:
        print("无法读取图片！")
        return

    # 缩小图片以便显示
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    img1 = cv2.resize(img1, (300, int(300 * h1 / w1)))
    img2 = cv2.resize(img2, (300, int(300 * h2 / w2)))

    # 转灰度 + 二值化
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    _, binary1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)
    _, binary2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)

    # 两种结构元素
    kernel_rect = np.ones((3, 3), np.uint8)
    kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    results = []

    for binary in [binary1, binary2]:
        row_imgs = [binary]

        # 膨胀 1、3、5 次（矩形核）
        for n in [1, 3, 5]:
            row_imgs.append(cv2.dilate(binary, kernel_rect, iterations=n))
        # 腐蚀 1、3、5 次（矩形核）
        for n in [1, 3, 5]:
            row_imgs.append(cv2.erode(binary, kernel_rect, iterations=n))
        # 膨胀 1、3、5 次（十字形核）
        for n in [1, 3, 5]:
            row_imgs.append(cv2.dilate(binary, kernel_cross, iterations=n))
        # 腐蚀 1、3、5 次（十字形核）
        for n in [1, 3, 5]:
            row_imgs.append(cv2.erode(binary, kernel_cross, iterations=n))

        labels = ['Original',
                  'Dilate1(rect)', 'Dilate3(rect)', 'Dilate5(rect)',
                  'Erode1(rect)', 'Erode3(rect)', 'Erode5(rect)',
                  'Dilate1(cross)', 'Dilate3(cross)', 'Dilate5(cross)',
                  'Erode1(cross)', 'Erode3(cross)', 'Erode5(cross)']

        # 统一小图尺寸
        target_h = binary.shape[0]
        target_w = binary.shape[1]

        titled_imgs = []
        for img, label in zip(row_imgs, labels):
            canvas = img.copy()
            if len(canvas.shape) == 2:
                canvas = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
            canvas = cv2.resize(canvas, (target_w, target_h))
            cv2.putText(canvas, label, (5, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 1)
            titled_imgs.append(canvas)

        # 拼成两行
        row1 = np.hstack(titled_imgs[0:7])
        row2 = np.hstack(titled_imgs[7:13])
        max_w = max(row1.shape[1], row2.shape[1])
        if row1.shape[1] < max_w:
            row1 = np.hstack([row1, np.zeros((row1.shape[0], max_w - row1.shape[1], 3), dtype=np.uint8)])
        if row2.shape[1] < max_w:
            row2 = np.hstack([row2, np.zeros((row2.shape[0], max_w - row2.shape[1], 3), dtype=np.uint8)])
        results.append(np.vstack([row1, row2]))

    max_w = max(r.shape[1] for r in results)
    padded = []
    for r in results:
        if r.shape[1] < max_w:
            r = np.hstack([r, np.zeros((r.shape[0], max_w - r.shape[1], 3), dtype=np.uint8)])
        padded.append(r)
    final = np.vstack(padded)
    cv2.imshow('Dilation & Erosion Comparison', final)
    cv2.imwrite('part1_result.jpg', final)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("""
=== 问题解答 ===

1. 随着迭代次数增加：
   - 膨胀：白色区域逐渐扩大，物体越来越"胖"，细节消失，
     5次时相邻物体可能粘连在一起（过度膨胀）。
   - 腐蚀：白色区域逐渐缩小，物体越来越"瘦"，
     细小部分断裂消失，5次时物体可能完全消失（过度腐蚀）。

2. 对于dg.jpg中的毛刺（细小凸起）：
   - 腐蚀更容易消除毛刺，因为腐蚀从边界向内收缩，
     毛刺像素少，1-2次腐蚀就会消失。
   - 但腐蚀也会让主体变小，所以通常先腐蚀去毛刺再膨胀恢复主体（即开运算）。

3. 十字形 vs 矩形结构元素：
   - 矩形核各方向均匀作用，对角线也有影响，效果更"圆润"。
   - 十字形核只在上下左右4个方向作用，对角线不受影响，
     物体的角保持更好，效果更"棱角分明"。
""")


# ============================================================
# 二、开运算与闭运算模拟图像中的去噪与修补
# ============================================================

def add_salt_pepper_noise(img, ratio=0.02):
    """添加椒盐噪声"""
    noisy = img.copy()
    h, w = noisy.shape[:2]
    num = int(h * w * ratio)
    coords = [np.random.randint(0, i, num) for i in [h, w]]
    noisy[coords[0], coords[1]] = 255
    coords = [np.random.randint(0, i, num) for i in [h, w]]
    noisy[coords[0], coords[1]] = 0
    return noisy


def part2_noise_removal():
    """2.1 噪声去除：开运算、闭运算、中值滤波对比"""
    img = cv2.imread('opencv/image/ren.png')
    if img is None:
        print("无法读取 ren.png！")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    noisy = add_salt_pepper_noise(gray, ratio=0.03)

    kernel = np.ones((5, 5), np.uint8)
    opened = cv2.morphologyEx(noisy, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(noisy, cv2.MORPH_CLOSE, kernel)
    median = cv2.medianBlur(noisy, 5)

    def add_label(image, text):
        canvas = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.putText(canvas, text, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        return canvas

    row1 = np.hstack([add_label(gray, 'Original'), add_label(noisy, 'Noisy')])
    row2 = np.hstack([add_label(opened, 'Opening'), add_label(closed, 'Closing')])
    row3 = add_label(median, 'Median Filter')

    max_w = max(row1.shape[1], row2.shape[1], row3.shape[1])
    rows = []
    for r in [row1, row2, row3]:
        if r.shape[1] < max_w:
            r = np.hstack([r, np.zeros((r.shape[0], max_w - r.shape[1], 3), dtype=np.uint8)])
        rows.append(r)
    grid = np.vstack(rows)

    cv2.imshow('Noise Removal Comparison', grid)
    cv2.imwrite('part2_noise.jpg', grid)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("""
=== 去噪对比结论 ===
中值滤波最适合去除椒盐噪声，原因：
- 椒盐噪声是孤立的极值点（纯黑或纯白），中值滤波取邻域中值，能直接排除极值。
- 开运算只能去除白色亮噪声，对黑色暗噪声无效。
- 闭运算只能去除黑色暗噪声，对白色亮噪声无效。
- 中值滤波对椒盐噪声效果最好，且边缘保持也优于开/闭运算。
""")


def part2_hole_filling():
    """2.2 孔洞填补：闭运算不同核大小"""
    img = cv2.imread('opencv/image/dy.jpg', cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("无法读取 dy.jpg！")
        return
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    results = [cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)]
    cv2.putText(results[0], 'Original', (5, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    for ksize in [5, 11, 17]:
        kernel = np.ones((ksize, ksize), np.uint8)
        closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        canvas = cv2.cvtColor(closed, cv2.COLOR_GRAY2BGR)
        cv2.putText(canvas, f'Close ({ksize}x{ksize})', (5, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        results.append(canvas)

    grid = np.hstack(results)
    cv2.imshow('Hole Filling with Closing', grid)
    cv2.imwrite('part2_hole.jpg', grid)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("""
=== 孔洞填补结论 ===
- (5,5)核：只能填满尺寸小于5x5的小孔洞，较大的孔洞保留不变。
- (11,11)核：能填满中等大小的孔洞，更大的孔洞仍然保留。
- (17,17)核：能填满更大的孔洞，但仍无法填满超过17x17的孔。
原因：闭运算的膨胀阶段，核越大膨胀能力越强，能填满的孔越大。
      结构元素只能填充尺寸小于自身的孔洞。
""")


def part3_answer_sheet():
    """2.3 答题卡处理：开运算+闭运算组合流程"""
    img = cv2.imread('opencv/image/zz.png', cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("无法读取 zz.png！")
        return
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # 开运算：去除外部小噪点和轻微粘连
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    step1 = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel_open)

    # 闭运算：填补内部小空洞
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    step2 = cv2.morphologyEx(step1, cv2.MORPH_CLOSE, kernel_close)

    def add_label(image, text):
        canvas = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.putText(canvas, text, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        return canvas

    results = np.hstack([
        add_label(img, 'Original'),
        add_label(step1, 'After Opening'),
        add_label(step2, 'After Opening+Closing')
    ])

    cv2.imshow('Answer Sheet Processing', results)
    cv2.imwrite('part3_answer_sheet.jpg', results)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("""
=== 答题卡处理流程 ===
1. 开运算（7x7椭圆核）：先腐蚀去除小噪点和轻微粘连，再膨胀恢复圆点形状。
   - 小于核的噪点被消除
   - 粘连处被断开
   - 大圆点基本保持形状

2. 闭运算（7x7椭圆核）：先膨胀填补内部小空洞，再腐蚀恢复边界。
   - 小于核的空洞被填满
   - 圆点整体形状恢复

关键：选择合适大小的核，使核尺寸 > 噪点/空洞 但 < 正常圆点。
""")


if __name__ == '__main__':
    print("=" * 50)
    print("一、膨胀与腐蚀的对比实验")
    print("=" * 50)
    part1()

    print("=" * 50)
    print("二、2.1 噪声去除对比")
    print("=" * 50)
    part2_noise_removal()

    print("=" * 50)
    print("二、2.2 孔洞填补")
    print("=" * 50)
    part2_hole_filling()

    print("=" * 50)
    print("二、2.3 答题卡处理")
    print("=" * 50)
    part3_answer_sheet()
