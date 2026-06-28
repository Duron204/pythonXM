import cv2
import numpy as np

def canny_edge_detection():
    img=cv2.imread("opencv/image/ren.png")
    dst=cv2.Canny(img,10,150,3,L2gradient=False)
    cv2.imshow("dst",dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    canny_edge_detection()