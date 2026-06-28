import random
import string
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont

def imRandCode(width=120, height=40, length=4, characters=None):
    if characters is None:
        characters = string.ascii_uppercase + string.digits
    random_str = ''.join(random.choices(characters, k=length))
    pixmap = QPixmap(width, height)
    pixmap.fill(QColor(255, 255, 255))
    painter = QPainter(pixmap)
    font = QFont("Arial", 20)
    painter.setFont(font)
    for i, char in enumerate(random_str):
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        painter.setPen(color)
        painter.drawText(10 + i * 25, 30, char)
    painter.end()
    return pixmap, random_str
