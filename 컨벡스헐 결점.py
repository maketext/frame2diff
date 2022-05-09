import cv2
img_color = cv2.imread("a1.png", cv2.IMREAD_COLOR)
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
isSuccess, img_binaray = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY_INV)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
img_binaray = cv2.morphologyEx(img_binaray, cv2.MORPH_CLOSE, kernel)

contours, hierarchy = cv2.findContours(img_binaray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

for c in contours: # [1,2,3] for element in [1,2,3]: element = 1, 2, 3.. 포문 종료.
    hull = cv2.convexHull(c, returnPoints=False)
    #cv2.drawContours(img_color,[hull],0,(255,0,255),2)

    try:
        defects = cv2.convexityDefects(c, hull)
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(c[s][0])
            end = tuple(c[e][0])
            far = tuple(c[f][0])

            if d > 10000:
                cv2.line(img_color, start, end, (0, 255, 0), 3)
                cv2.circle(img_color, far, 5, (0, 0, 255), -1)
    except:
        pass

cv2.imshow('res', img_color)
cv2.waitKey(0)