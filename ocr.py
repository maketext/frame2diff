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
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cv2.waitKey(33) < 0:
    ret, frame = capture.read()
    text = reader.readtext(image=frame, detail=0)
    if len(text) > 0:
        frame = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame)
        unicode_font = ImageFont.truetype("malgun.ttf", 20)
        draw.text((10,10), ",".join(str(x) for x in text), font=unicode_font, fill=Color.GREEN.value)
        frame = np.array(frame)
    cv2.imshow("VideoFrame", frame)