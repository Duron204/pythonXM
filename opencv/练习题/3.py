import cv2
import numpy as np

# 1. 创建 400×400 的黑色图像（3通道，uint8）
img = np.zeros((400, 400, 3), dtype=np.uint8)

# 2. 绘制红色直线（BGR颜色：(0,0,255)，线宽3）
cv2.line(img, (50, 50), (350, 350), (0, 0, 255), 3)

# 3. 绘制绿色矩形（BGR：(0,255,0)，线宽2）
cv2.rectangle(img, (100, 100), (200, 200), (0, 255, 0), 2)

# 4. 绘制蓝色填充圆（BGR：(255,0,0)，线宽-1表示填充）
cv2.circle(img, (300, 100), 40, (255, 0, 0), -1)

# 5. 绘制白色文本（字体：FONT_HERSHEY_SIMPLEX，大小1，线宽2）
cv2.putText(img, 'OpenCV', (150, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# 6. 保存并显示
cv2.imwrite('draw.jpg', img)
cv2.imshow('Drawing', img)
cv2.waitKey(0)
cv2.destroyAllWindows()