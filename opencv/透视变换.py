import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils

# ================== 工具函数 ==================

def order_points(pts):
    """
    对4个角点按照 左上→右上→右下→左下 的顺序排列
    pts: 4个原始角点坐标, shape=(4,2)
    返回: 排序后的4个角点
    原理: 左上角坐标和最小(x+y), 右下角坐标和最大(x+y);
          右上角diff最小(x-y), 左下角diff最大(x-y)
    """
    rect = np.zeros((4, 2), dtype="float32")
    # 按坐标和(x+y)排序: 和最小=左上, 和最大=右下
    s = np.sum(pts, axis=1)
    rect[0] = pts[np.argmin(s)]  # 左上
    rect[2] = pts[np.argmax(s)]  # 右下
    # 按坐标差(x-y)排序: 差最小=右上, 差最大=左下
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # 右上
    rect[3] = pts[np.argmax(diff)]  # 左下
    return rect

def four_point_transform(image, pts):
    """
    对图像进行透视变换(矫正), 将4个点围成的区域拉伸为矩形
    image: 原始图像
    pts:   4个角点坐标 (已排序: 左上->右上->右下->左下)
    返回:  矫正后的矩形图像
    """
    # 1. 对4个角点排序
    rect = order_points(pts)
    (tl, tr, br, bl) = rect  # 解包: 左上, 右上, 右下, 左下

    # 2. 计算目标矩形的宽度: 取上边和下边的较大者
    withB = np.sqrt((tr[0] - tl[0])**2 + (tr[1] - tl[1])**2)  # 上边长度
    withA = np.sqrt((br[0] - bl[0])**2 + (br[1] - bl[1])**2)  # 下边长度
    maxw = max(int(withB), int(withA))

    # 3. 计算目标矩形的高度: 取左边和右边的较大者
    heightA = np.sqrt((bl[0] - tl[0])**2 + (bl[1] - tl[1])**2)  # 左边高度
    heightB = np.sqrt((br[0] - tr[0])**2 + (br[1] - tr[1])**2)  # 右边高度
    maxh = max(int(heightA), int(heightB))

    # 4. 构建目标矩形的4个角点 (按同样顺序: 左上→右上→右下→左下)
    dst = np.array([
        [0, 0],                       # 左上
        [maxw - 1, 0],                # 右上
        [maxw - 1, maxh - 1],         # 右下
        [0, maxh - 1]                 # 左下
    ], dtype="float32")

    # 5. 计算透视变换矩阵 M (3×3), 将原图中的四边形映射到目标矩形
    M = cv2.getPerspectiveTransform(rect, dst)
    # 6. 应用透视变换
    warped = cv2.warpPerspective(image, M, (maxw, maxh))
    return warped


# ================== 主程序 ==================

# 1. 读取图像
img = cv2.imread('image/ts.jpg')

# 2. 图像缩放: 保持宽高比, 将高度缩放到500像素
#    原图可能太大, 缩放后能提高边缘检测和轮廓查找的速度
ratio = img.shape[0] / 500  # 计算缩放比例, 后续用于还原坐标
orig = img.copy()           # 保留原图用于最终绘制和矫正
img = imutils.resize(img, height=500)  # 缩放后的图用于处理

# 3. 预处理: 灰度化 + 高斯模糊(去噪)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# 4. Canny边缘检测: 提取图像中的边缘信息
edges = cv2.Canny(gray, 40, 50)

# 5. 查找轮廓: RETR_LIST=检测所有轮廓, CHAIN_APPROX_SIMPLE=压缩水平/垂直段
cnts, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# 6. 按面积从大到小排序轮廓 (面积最大的通常是文档/纸张的外轮廓)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

# 7. 遍历轮廓, 找到近似为四边形(4个顶点)的轮廓
#    approxPolyDP: 道格拉斯-普克算法, 0.02*周长 是近似精度
screenCnt = None
for c in cnts:
    perimeter = cv2.arcLength(c, True)          # 计算轮廓周长
    approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)  # 多边形近似
    if len(approx) == 4:   # 找到4边形的轮廓(文档/纸张的外边框)
        screenCnt = approx
        break

# 8. 在原图上绘制轮廓和顶点
#    注意: screenCnt坐标来自缩放后的图, 需要乘ratio还原到原图尺寸
screenCnt_scaled = np.intp(screenCnt.reshape(4, 1, 2) * ratio)
cv2.drawContours(orig, [screenCnt_scaled], -1, (0, 255, 0), 2)  # 绿色轮廓线

# 9. 透视变换: 将四边形区域矫正为正面矩形视图
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

# 10. 在原图上绘制4个角点(绿色圆点)
for point in screenCnt_scaled.reshape(4, 2):
    cv2.circle(orig, (int(point[0]), int(point[1])), 5, (0, 255, 0), 4)

# 11. 显示结果对比
plt.subplot(121)
plt.imshow(cv2.cvtColor(orig, cv2.COLOR_BGR2RGB))   # BGR→RGB
plt.title("Original Image")
plt.axis('off')

plt.subplot(122)
plt.imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
plt.title("Corrected Image")
plt.axis('off')

plt.show()