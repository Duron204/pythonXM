import cv2
import numpy as np
# 分别使用soble、scharr、laplacian算子对图像进行边缘检测
def laplacian_base():
    img=cv2.imread('opencv/image/ren.png',cv2.IMREAD_GRAYSCALE)

    sobelx=cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3)
    sobely=cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3)
    sobelx=cv2.convertScaleAbs(sobelx)
    sobely=cv2.convertScaleAbs(sobely)
    sobelxy=cv2.addWeighted(sobelx,0.5,sobely,0.5,0)

    scharrx=cv2.Scharr(img,cv2.CV_64F,1,0)
    scharry=cv2.Scharr(img,cv2.CV_64F,0,1)
    scharrx=cv2.convertScaleAbs(scharrx)
    scharry=cv2.convertScaleAbs(scharry)
    scharrxy=cv2.addWeighted(scharrx,0.5,scharry,0.5,0)

    laplacian=cv2.Laplacian(img,cv2.CV_64F,ksize=3)
    laplacian=cv2.convertScaleAbs(laplacian)
    res=np.hstack((sobelxy,scharrxy,laplacian))

    cv2.imshow("res",res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    laplacian_base()