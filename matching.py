import cv2

bg = cv2.imread('img/mold1.png', cv2.IMREAD_GRAYSCALE)
bg = cv2.resize(bg, (100, 100))
im = bg[0:33, 33:66]
#cv2.imshow('dds', im);
w, h = im.shape[:2]

print(w, h)
parts = [bg[0:33, 0:33], bg[0:33, 33:66], bg[0:33, 66:99],

        bg[33:66, 0:33], bg[33:66, 66:99],

        bg[66:99, 0:33], bg[66:99, 33:66], bg[66:99, 66:99]
]
crop = [[0,33,0,33], [0,33,33,66], [0,33,66,99],
        [33,66,0,33], [33,66,33,66],
        [66,99,0,33], [66,99,33,66],[66,99,66,99]
        ]
max = 0
y1, y2, x1, x2 = [None, None, None, None]

for i, part in enumerate(parts):
    res = cv2.matchTemplate(part, im, cv2.TM_CCORR) # Option "TM_CCORR" works well for detecting whole white background rather then TM_CCOEFF_NORMED or TM_SQDIFF_NORMED.
    for y in range(0, res.shape[0]):
        for x in range(0, res.shape[1]):
            if res[y,x] > max:
                max = res[y,x]
                y1, y2, x1, x2 = crop[i]
print(y1, y2, x1, x2)

checked = cv2.cvtColor(bg, cv2.COLOR_GRAY2RGB)
checked = cv2.rectangle(checked, (x1, y1), (x2, y2), (0, 0, 255), 2)
cv2.imshow("Matching result", checked)
cv2.imwrite("res.png", checked)

#res = res * 255

cv2.waitKey(0)
