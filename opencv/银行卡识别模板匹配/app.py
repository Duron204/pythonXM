import cv2

digits={}

def cv_show(name,img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def sort_contours(cnts,method="left-to-right"):
    reverse = False
    i=0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse=True
    if method == "top-to-bottom"or method == "bottom-to-top":
        i=1
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b: b[1][i],
    reverse=reverse))
    return cnts,boundingBoxes

def process_template():
    img = cv2.imread("mb.png")
    ref = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ref = cv2.threshold(ref, 10, 255, cv2. THRESH_BINARY_INV)[1]
    cv_show("ref", ref)
    refCnts, hierarchy =cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, refCnts, -1, (0, 0, 255), 3)
    cv_show("img",img)
    refCnts = sorted(refCnts, key=cv2.contourArea, reverse=True)
    refCnts = sort_contours(refCnts, method="left-to-right")[0]
    for (i, c) in enumerate(refCnts):
        (x, y, w,h)= cv2.boundingRect(c)
        roi = ref[y:y + h,x:x +w]
        roi = cv2.resize(roi, (57, 58))
        cv_show("ror", roi)
        digits[i]= roi

if __name__ == '__main__':
    process_template()