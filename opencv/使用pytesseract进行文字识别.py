from PIL import Image
import pytesseract
# 指定Tesseract的路径（如果你没有将其添加到系统的PATH中）
# pytesseract.pytesseract.tesseract_cmd = r'C:\TesseractOCR\tesseract.exe'
# 打开图像文件
image_path = 'image/test1.png'
try:
    image = Image.open(image_path)
except FileNotFoundError:
    print(f"Error: The file {image_path} does not exist.")
    exit()
# 使用pytesseract进行文字识别
text = pytesseract.image_to_string(image, lang='chi_sim')
# 输出识别结果
print(text)