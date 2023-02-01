import cv2

bg = cv2.imread('img/mold.png', cv2.IMREAD_GRAYSCALE) # 원본 이미지
bg = cv2.resize(bg, (100, 100))
im = bg[0:33, 33:66] # 탬플릿 이미지
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
for i, part in enumerate(parts):
    print(part.shape)
    res = cv2.matchTemplate(part, im, cv2.TM_CCOEFF_NORMED) # 원본, 탬플릿 이미지, 옵션 순

    for y in range(0, res.shape[0]):
        for x in range(0, res.shape[1]):
            if res[y,x] > 0.5:
                y1, y2, x1, x2 = crop[i]
                checked = cv2.cvtColor(bg, cv2.COLOR_GRAY2RGB)
                checked = cv2.rectangle(checked, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.imshow("ddd", checked)
                cv2.imwrite("ddd.jpg", checked)

#res = res * 255

cv2.waitKey(0)
