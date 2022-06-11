import cv2

im = cv2.imread('img/bolt1.jpg', cv2.IMREAD_GRAYSCALE)
bg = cv2.imread('img/bolts.jpg', cv2.IMREAD_GRAYSCALE)
w, h = im.shape[:2]

res = cv2.matchTemplate(bg, im, cv2.TM_CCOEFF_NORMED)

for y in range(0, res.shape[0]):
    for x in range(0, res.shape[1]):
        if res[y,x] > 0.7:
            cv2.rectangle(bg, (x, y), (x + w, y + h), (0, 0, 255), 1)

#res = res * 255

cv2.imshow('bolt1', im)
cv2.imshow('match', res)
cv2.imshow('result', bg)
cv2.waitKey(0)
