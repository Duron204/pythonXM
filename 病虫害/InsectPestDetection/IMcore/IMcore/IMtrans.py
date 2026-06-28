import cv2
import numpy as np
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

def ToQtPixmap(cv_image):
    if cv_image is None:
        return QPixmap()
    if len(cv_image.shape) == 2:
        h, w = cv_image.shape
        q_image = QImage(cv_image.data, w, h, w, QImage.Format_Grayscale8)
    else:
        h, w, ch = cv_image.shape
        bytes_per_line = ch * w
        q_image = QImage(cv_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(q_image)

def scalePixmap(pixmap, size, keepAspect=False):
    if pixmap.isNull():
        return pixmap
    if keepAspect:
        return pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    else:
        return pixmap.scaled(size, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

def setPixmap(label, pixmap):
    if label is not None:
        label.setPixmap(pixmap)
