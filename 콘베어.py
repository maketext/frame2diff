import cv2 as cv
from cv2 import cvtColor
cap=cv.VideoCapture(0)
fb=cv.createBackgroundSubtractorMOG2(history=10, varThreshold=250, detectShadows=False)

while(1):
    isSuccess, img_frame =cap.read()
    if isSuccess ==False:
        break
    blur=cv.GaussianBlur(img_frame,(5,5),0)
    img_mask=fb.apply(blur,learningRate=0)

    img_frame = cvtColor(img_frame, cv.COLOR_BGR2GRAY)
    img_mask = ~img_mask
    img_res = cv.subtract(img_frame, img_mask)
    isSuccess, img_res = cv.threshold(img_res, 70, 255, cv.THRESH_BINARY) 
    #img_res = cv.subtract(img_frame, img_res)
    cv.imshow('res', img_res)
    if cv.waitKey(13) > 0:
        break
cap.release()


