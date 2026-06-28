"""
身份证号码识别 - Web 应用
基于 识别身份证上的号码.py 的 OCR 逻辑，提供 Web 前端界面
"""
import os
import uuid
import cv2
import numpy as np
import pytesseract
from PIL import Image
from flask import Flask, request, jsonify, render_template, url_for

# ========== Flask App 配置 ==========
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ========== Tesseract 配置 ==========
pytesseract.pytesseract.tesseract_cmd = r'D:\TesseractOCR\tesseract.exe'
TESSDATA_DIR = 'D:\\TesseractOCR\\tessdata'

debug = 1  # 调试模式开关：1=保存中间图像，0=关闭


# ========== 以下 OCR 函数来自 识别身份证上的号码.py ==========

def preprocess(gray, save_prefix=""):
    """
    图像预处理函数：对灰度图进行二值化和膨胀操作，
    目的是突出文本区域，使其在图像中形成明显的连通块。

    参数：
        gray: 输入灰度图像（单通道）
        save_prefix: 保存文件的前缀（用于区分不同上传）
    返回：
        dilation: 膨胀后的二值图像
    """
    # 二值化：将灰度图转为黑白图，大于180的像素置0（黑），小于180的置255（白）
    ret, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    # 创建膨胀核：15x10的矩形结构元素，水平方向更长，用于连接水平方向上的文字字符
    ele = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 10))

    # 膨胀操作：将白色区域向外扩张，使相邻的文字字符连成一片，形成完整文本块
    dilation = cv2.dilate(binary, ele, iterations=1)

    # 保存中间结果到文件，供调试查看
    cv2.imwrite(f"{save_prefix}_binary.jpg", binary)
    cv2.imwrite(f"{save_prefix}_dilation.jpg", dilation)

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
    region = []

    # 查找轮廓：使用RETR_TREE（树形层级）和CHAIN_APPROX_SIMPLE
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        cnt = contours[i]

        # 计算轮廓面积，过滤掉太小的噪点
        area = cv2.contourArea(cnt)
        if area < 300:
            continue

        # 轮廓近似
        epsilon = 0.001 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # 获取轮廓的最小外接矩形（带旋转角度）
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = box.astype(np.int32)

        # 计算边界框的高度和宽度
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])

        # 筛选条件1：排除竖立的长条
        if (height > width * 1.2):
            continue
        # 筛选条件2：排除过长的条形
        if (height * 18 < width):
            continue

        # 筛选条件3：宽度超过图像宽度的一半，且高度超过图像高度的1/20
        if (width > img.shape[1] / 2 and height > img.shape[0] / 20):
            region.append(box)

    return region


def grayImg(img):
    """
    将彩色图像区域放大并转为灰度图，然后使用Otsu自适应阈值二值化。

    参数：
        img: 输入的彩色图像区域
    返回：
        gray: 处理后的灰度/二值图像
    """
    gray = cv2.resize(img, (img.shape[1] * 3, img.shape[0] * 3), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    retval, gray = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return gray


def detect(img, save_prefix=""):
    """
    检测身份证图像中的号码区域，并提取该区域进行预处理。

    参数：
        img: 输入的身份证彩色图像（已缩放到标准尺寸）
        save_prefix: 保存文件前缀
    返回：
        idImg: 提取并预处理后的身份证号码区域图像
    """
    # 快速非局部均值去噪
    gray = cv2.fastNlMeansDenoisingColored(img, None, 10, 3, 3, 3)

    # 自定义灰度转换系数
    coefficients = [0, 1, 1]
    m = np.array(coefficients).reshape((1, 3))
    gray = cv2.transform(gray, m)

    if debug:
        cv2.imwrite(f"{save_prefix}_gray.jpg", gray)

    # 预处理：二值化 + 膨胀
    dilation = preprocess(gray, save_prefix)

    # 在膨胀图上检测文本区域轮廓
    region = findTextRegion(dilation)

    # 遍历所有候选区域
    li = 0
    idImg = None
    for box in region:
        h = abs(box[0][1] - box[2][1])
        w = abs(box[0][0] - box[2][0])

        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]

        x1 = min(Xs)
        y1 = min(Ys)

        cv2.drawContours(img, [box], 0, (0, 255, 0), 2)

        if w > 0 and h > 0 and x1 < gray.shape[1] / 2:
            idImg = grayImg(img[y1:y1 + h, x1:x1 + w])
            cv2.imwrite(f"{save_prefix}_number.jpg", idImg)
            break
        li += 1

    if debug:
        cv2.imwrite(f"{save_prefix}_contours.jpg", img)

    return idImg


# ========== Web 路由 ==========

@app.route('/')
def index():
    """首页：上传界面"""
    return render_template('index.html')


@app.route('/recognize', methods=['POST'])
def recognize():
    """处理上传的身份证图片并识别号码"""
    if 'image' not in request.files:
        return jsonify({'error': '请上传图片'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '请选择图片'}), 400

    # 生成唯一前缀，防止并发覆盖
    uid = uuid.uuid4().hex[:8]
    save_prefix = os.path.join(app.config['UPLOAD_FOLDER'], uid)

    # 保存上传的原图
    ext = os.path.splitext(file.filename)[1] or '.png'
    orig_path = f"{save_prefix}_original{ext}"
    file.save(orig_path)

    # 读取图片
    img = cv2.imread(orig_path, cv2.IMREAD_COLOR)
    if img is None:
        return jsonify({'error': '无法读取图片，请上传有效的图片文件'}), 400

    # 缩放到统一尺寸
    img = cv2.resize(img, (428, 270), interpolation=cv2.INTER_CUBIC)
    # 覆盖保存缩放后的原图
    cv2.imwrite(orig_path, img)

    # 获取真实号码（可选，用于对比）
    real_id = request.form.get('real_id', '')

    # 执行 OCR 识别
    try:
        idImg = detect(img, save_prefix)

        if idImg is None:
            return jsonify({
                'error': '未能检测到身份证号码区域，请确认图片清晰且包含身份证正面',
                'images': _get_image_urls(save_prefix)
            }), 400

        image = Image.fromarray(idImg)
        tessdata_dir_config = f'--tessdata-dir {TESSDATA_DIR}'
        result = pytesseract.image_to_string(image, lang='chi_sim', config=tessdata_dir_config)
        result = result.strip()

        return jsonify({
            'success': True,
            'real_id': real_id,
            'recognized': result,
            'images': _get_image_urls(save_prefix)
        })

    except Exception as e:
        return jsonify({'error': f'识别过程出错：{str(e)}'}), 500


@app.route('/test')
def test():
    """返回测试图片的信息"""
    test_path = 'image/sfz1.png'
    if os.path.exists(test_path):
        return jsonify({
            'success': True,
            'test_file': test_path,
            'test_url': url_for('static', filename='../' + test_path.replace('\\', '/')),
            'test_real_id': '430523197603204314'
        })
    return jsonify({'success': False, 'error': '测试图片不存在'}), 404


def _get_image_urls(save_prefix):
    """获取所有中间处理图片的 URL 列表"""
    names = ['original', 'gray', 'binary', 'dilation', 'contours', 'number']
    urls = {}
    for name in names:
        # 尝试常见扩展名
        for ext in ['.jpg', '.png']:
            path = f"{save_prefix}_{name}{ext}"
            if os.path.exists(path):
                # 转为相对 URL 路径
                rel_path = os.path.relpath(path, 'static').replace('\\', '/')
                urls[name] = url_for('static', filename=rel_path)
                break
    return urls


# ========== 入口 ==========

if __name__ == '__main__':
    print("=" * 50)
    print("身份证号码识别 Web 应用")
    print(f"打开浏览器访问: http://127.0.0.1:5001")
    print("=" * 50)
    app.run(debug=True, host='127.0.0.1', port=5001)
