import easyocr
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from enum import Enum

reader = easyocr.Reader(['ko', 'en'], gpu=False)
class Color(Enum):
    RED = (0, 0, 255)
    GREEN = (0, 0, 0)

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#capture.set(cv2.CAP_PROP_FOCUS, 21)
capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)

kernel = np.zeros((5, 5), np.uint8)

f = 0
while True:
    ret, frame = capture.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #ret, frame = cv2.threshold(frame, 150, 255, cv2.THRESH_BINARY)
    #frame = cv2.dilate(frame, kernel, iterations=10)

    #print(fr"포커스={capture.get(cv2.CAP_PROP_FOCUS)}")
    cv2.imshow("VideoFrame", frame)
    #cv2.imwrite("ddd.jpg", frame)

    key = cv2.waitKey(13)
    if key >= 0:
        text = reader.readtext(image=frame, detail=0)
        if len(text) > 0:
            frame = Image.fromarray(frame)
            draw = ImageDraw.Draw(frame)
            unicode_font = ImageFont.truetype("malgun.ttf", 10)
            #draw.text((10,10), ",".join(str(x) for x in text), font=unicode_font, fill=Color.GREEN.value)
            print(text)
            frame = np.array(frame)

