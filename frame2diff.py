import cv2
import numpy as np

col_images=[]

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cv2.waitKey(33) < 0:
    ret, frame = capture.read()
    col_images.append(frame)

    if len(col_images) > 2:
        i = len(col_images) - 1
        grayA = cv2.cvtColor(col_images[i - 1], cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(col_images[i], cv2.COLOR_BGR2GRAY)

        diff_image = cv2.absdiff(grayB, grayA)
        ret, thresh = cv2.threshold(diff_image, 30, 255, cv2.THRESH_BINARY)

        kernel = np.ones((10, 10), np.uint8)
        dilated = cv2.dilate(thresh, kernel, 10)
        cv2.imshow("VideoFrame", dilated)

capture.release()
cv2.destroyAllWindows()
