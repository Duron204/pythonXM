import cv2  # 导入OpenCV库，用于图像处理和计算机视觉
import numpy as np  # 导入NumPy库，用于数值计算和数组操作
import matplotlib.pyplot as plt  # 导入Matplotlib，用于显示图像和调试结果
import pytesseract  # 导入Tesseract OCR引擎，用于文字识别
from PIL import Image  # 导入PIL库，用于图像格式转换

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

debug = 1  # 调试模式开关：1=开启（保存中间图像并显示结果），0=关闭
# 配置Tesseract OCR引擎的可执行文件路径
pytesseract.pytesseract.tesseract_cmd=r'D:\TesseractOCR\tesseract.exe'


def preprocess(gray):
    """
    图像预处理函数：对灰度图进行二值化和膨胀操作，
    目的是突出文本区域，使其在图像中形成明显的连通块。

    参数：
        gray: 输入灰度图像（单通道）
    返回：
        dilation: 膨胀后的二值图像
    """
    # 二值化：将灰度图转为黑白图，大于180的像素置0（黑），小于180的置255（白）
    # 使用THRESH_BINARY_INV反转，使文字区域变为白色（前景），背景为黑色
    ret, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    # 创建膨胀核：15x10的矩形结构元素，水平方向更长，用于连接水平方向上的文字字符
    ele = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 10))

    # 膨胀操作：将白色区域向外扩张，使相邻的文字字符连成一片，形成完整文本块
    dilation = cv2.dilate(binary, ele, iterations=1)

    # 保存中间结果到文件，供调试查看
    cv2.imwrite("binary.jpg", binary)      # 二值化结果
    cv2.imwrite("dilation.jpg", dilation)  # 膨胀后结果

    return dilation


def findTextRegion(img):
    """
    在膨胀后的二值图像中查找文本区域（身份证号码所在位置）。
    通过轮廓检测和几何特征筛选，定位符合身份证号码特征的区域。

    参数：
        img: 膨胀后的二值图像
    返回：
        region: 符合条件的文本区域边界框列表（每个框为4个顶点坐标）
    """
    region = []  # 保存所有符合条件的文本区域边界框

    # 查找轮廓：使用RETR_TREE（树形层级）和CHAIN_APPROX_SIMPLE（压缩水平/垂直段）
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历每个找到的轮廓
    for i in range(len(contours)):
        cnt = contours[i]  # 当前轮廓

        # 计算轮廓面积，过滤掉太小的噪点（面积小于300像素的轮廓直接跳过）
        area = cv2.contourArea(cnt)
        if area < 300:
            continue

        # 轮廓近似：用更少的顶点逼近轮廓形状，epsilon为最大逼近精度
        epsilon = 0.001 * cv2.arcLength(cnt, True)  # 基于轮廓周长的1‰
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # 获取轮廓的最小外接矩形（带旋转角度）
        rect = cv2.minAreaRect(cnt)
        # 将矩形转为4个顶点坐标
        box = cv2.boxPoints(rect)
        # 坐标转换为整型
        box = box.astype(np.int32)

        # 计算边界框的高度和宽度（取顶点0和顶点2的差值）
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])

        # 筛选条件1：排除竖立的长条（高度 > 宽度×1.2 的认为是竖排文字或噪声）
        if (height > width * 1.2):
            continue
        # 筛选条件2：排除过长的条形（宽度 > 高度×18，太扁的轮廓不可能是号码区域）
        if (height * 18 < width):
            continue

        # 筛选条件3：宽度超过图像宽度的一半，且高度超过图像高度的1/20
        # 身份证号码通常是图像中较宽的水平区域
        if(width > img.shape[1] / 2 and height > img.shape[0] / 20):
            region.append(box)  # 将符合条件的区域加入列表

    return region


def grayImg(img):
    """
    将彩色图像区域放大并转为灰度图，然后使用Otsu自适应阈值二值化。
    目的是提高OCR识别精度。

    参数：
        img: 输入的彩色图像区域
    返回：
        gray: 处理后的灰度/二值图像
    """
    # 将图像放大3倍，提高小文字的分辨率，使OCR识别更准确
    gray = cv2.resize(img, (img.shape[1] * 3, img.shape[0] * 3), interpolation=cv2.INTER_CUBIC)

    # 将彩色图像转换为灰度图（单通道）
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

    # 使用Otsu自适应阈值二值化：自动计算最优阈值，将灰度图转为黑白图
    retval, gray = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return gray


def detect(img):
    """
    检测身份证图像中的号码区域，并提取该区域进行预处理。
    这是核心函数，整合了去噪、灰度转换、膨胀、轮廓检测和区域提取。

    参数：
        img: 输入的身份证彩色图像（已缩放到标准尺寸）
    返回：
        idImg: 提取并预处理后的身份证号码区域图像
    """
    # 使用快速非局部均值去噪算法去除彩色图像噪声
    # 参数：图像, 无, 滤波强度h=10, hForColor=3, templateWindowSize=3, searchWindowSize=3
    gray = cv2.fastNlMeansDenoisingColored(img, None, 10, 3, 3, 3)

    # 自定义灰度转换系数：提取RGB通道中的G和B通道分量（系数[0,1,1]）
    # 即：gray = 0*R + 1*G + 1*B（忽略红色通道，仅使用绿蓝通道的和）
    coefficients = [0, 1, 1]
    m = np.array(coefficients).reshape((1, 3))  # 转为1×3的变换矩阵
    gray = cv2.transform(gray, m)  # 执行颜色通道线性变换

    if debug:
        cv2.imwrite("gray.jpg", gray)  # 保存灰度图用于调试

    # 预处理：二值化 + 膨胀，使文字区域连成块
    dilation = preprocess(gray)

    # 在膨胀图上检测文本区域轮廓
    region = findTextRegion(dilation)

    # 遍历找到的所有候选区域
    li = 0  # 计数器，用于命名保存的图片文件
    for box in region:
        # 计算该区域的高度和宽度
        h = abs(box[0][1] - box[2][1])
        w = abs(box[0][0] - box[2][0])

        # 提取所有顶点的X坐标和Y坐标
        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]

        # 计算区域的左上角坐标
        x1 = min(Xs)
        y1 = min(Ys)

        # 在原图上绘制绿色边框，标记检测到的候选区域（调试用）
        cv2.drawContours(img, [box], 0, (0, 255, 0), 2)

        # 最终筛选：宽高都大于0，且区域在图像左半部分
        # (身份证号码通常在身份证图像的左半侧)
        if w > 0 and h > 0 and x1 < gray.shape[1] / 2:
            # 从原图中裁剪出号码区域，然后放大并二值化处理
            idImg = grayImg(img[y1:y1 + h, x1:x1 + w])
            cv2.imwrite(str(li) + ".jpg", idImg)  # 保存号码区域图片
            break  # 只取第一个符合条件的区域（即最可能的号码区）
        li += 1

    if debug:
        cv2.imwrite("contours.jpg", img)  # 保存标有轮廓的调试图

    return idImg


def ocrIdCard(imgPath, realId=""):
    """
    身份证OCR识别主函数：读取身份证图片，定位号码区域，执行文字识别。

    参数：
        imgPath: 身份证图片的文件路径
        realId: 真实的身份证号码（用于对比识别结果，评估准确率，可选）

    工作流程：
        1. 读取图像并缩放到标准尺寸
        2. 检测号码区域
        3. 使用Tesseract OCR引擎进行中文识别
        4. 输出真实号码和识别结果
        5. 调试模式下显示所有中间处理步骤的图像
    """
    # 以彩色模式读取身份证图像
    img = cv2.imread(imgPath, cv2.IMREAD_COLOR)

    # 将图像缩放到统一尺寸 428×270 像素（身份证标准宽高比）
    # INTER_CUBIC 是三次插值法，缩放质量较高
    img = cv2.resize(img, (428, 270), interpolation=cv2.INTER_CUBIC)

    # 调用detect函数检测并提取身份证号码区域
    idImg = detect(img)

    # 将OpenCV图像（NumPy数组）转换为PIL Image对象，供pytesseract使用
    image = Image.fromarray(idImg)

    # 指定Tesseract语言数据目录（存放chi_sim中文简体语言包）
    tessdata_dir_config = '--tessdata-dir D:\\TesseractOCR\\tessdata'

    # 使用Tesseract进行OCR文字识别
    # lang='chi_sim'：使用简体中文语言包
    # config=tessdata_dir_config：指定语言数据目录
    result = pytesseract.image_to_string(image, lang='chi_sim', config=tessdata_dir_config)

    # 打印真实号码（用于对照）和OCR识别的号码
    print("真实号码：", realId)
    print("识别号码：", result)

    # 调试模式：使用Matplotlib显示各处理步骤的图像
    if debug:
        f, axarr = plt.subplots(2, 3)  # 创建2行3列的子图布局

        # 第1行：原始图像、灰度图、二值图
        axarr[0][0].imshow(cv2.imread(imgPath))       # 原图
        axarr[0][1].imshow(cv2.imread("gray.jpg"))    # 灰度图
        axarr[0][2].imshow(cv2.imread("binary.jpg"))  # 二值图
        # 第2行：膨胀图、轮廓标记图、号码区域图
        axarr[1][0].imshow(cv2.imread("dilation.jpg"))    # 膨胀图
        axarr[1][1].imshow(cv2.imread("contours.jpg"))    # 标有轮廓的图

        # 在最后一个子图上显示真实号码和识别号码作为标题
        axarr[1, 2].set_title("真实号码:" + realId + "\n识别号码:" + result)
        axarr[1, 2].imshow(cv2.imread("0.jpg"))  # 最终提取的号码区域

        plt.show()  # 显示所有图像


# 程序入口：执行身份证号码识别
# 测试图片：image/sfz1.png，真实号码：430523197603204314
ocrIdCard("image/sfz1.png", "430523197603204314")