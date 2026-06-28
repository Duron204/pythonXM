import cv2
import numpy as np

def sharr_lena():
    img = cv2.imread('opencv/image/ren.png', cv2.IMREAD_GRAYSCALE)
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sobelx = cv2.convertScaleAbs(sobelx)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    sobely = cv2.convertScaleAbs(sobely)
    sobelxy = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)
    sobelxr = cv2.Scharr(img, cv2.CV_64F, 1, 0)
    sobelxr = cv2.convertScaleAbs(sobelxr)
    sobelyr = cv2.Scharr(img, cv2.CV_64F, 0, 1)
    sobelyr = cv2.convertScaleAbs(sobelyr)
    sobelxyr = cv2.addWeighted(sobelxr, 0.5, sobelyr, 0.5, 0)
    res=np.hstack((sobelxy,sobelxyr))
    cv2.imshow('sobelxy',res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    sharr_lena()
