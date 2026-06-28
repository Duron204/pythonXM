import cv2
import numpy as np

def sobel_lena():
    img = cv2.imread('opencv/image/ren.png', cv2.IMREAD_GRAYSCALE)
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sobelx = cv2.convertScaleAbs(sobelx)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    sobely = cv2.convertScaleAbs(sobely)
    sobelxy = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)
    sobelall = cv2.Sobel(img, cv2.CV_64F, 1, 1, ksize=3)
    sobelall = cv2.convertScaleAbs(sobelall)
    res=np.hstack((sobelall,sobelxy))
    cv2.imshow('sobelxy',res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    sobel_lena()
