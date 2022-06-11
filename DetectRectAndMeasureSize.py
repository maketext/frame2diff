import imp
import cv2 #open-cv
# import paho.mqtt.client as mClient
# import time
# import threading
# import random
import os # 현재사용os에서 가능 파일위치등
from enum import Enum
import numpy as np

#from cv2 import imwrite
# from sys import exit
  

class HomogeneousBgDetector():
    def __init__(self):
        pass

    def detect_objects(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        objects_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 2000:
                objects_contours.append(cnt)

        return objects_contours


class Color(Enum):
    BLACK = (0,0,0)
    RED = (0,0,255)

class KeyCode(Enum):
    Enter = 13

# def imwrite(filename, img, params=None):
   # try: 
     #   ext = os.path.splitext(filename)[1]
      #  result, n = cv2.imencode(ext, img, params)
       # if result:  
         #   with open(filename, mode='w+b') as f:
          #       n.tofile(f)
           #      return True
         #else:
          #   return False
     #except Exception as e:
      #   print(e)
       #  return False




cap = None
count = 0

def setCam(cap, w, h):
    #cap = cv2.VideoCapture(cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    cap.set(cv2.CAP_PROP_FPS, 1)
    cap.set(cv2.CAP_PROP_FOCUS, 8)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    return cap

def measureSize(src):

    detector = HomogeneousBgDetector()
    contours = detector.detect_objects(src)
    objects_contours = []

    for cnt in contours:
      area = cv2.contourArea(cnt)
      if area > 500:
          objects_contours.append(cnt)
    for cnt in objects_contours:
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect

        box = cv2.boxPoints(rect)
        box = np.int0(box)

        if w < h:
            angle += 90
        else:
            angle += 0

        if angle - 180 > 0:
            angle -= 180

        cv2.circle(src, (int(x), int(y)), 15, (0, 0, 255), -1)
        cv2.polylines(src, [box], True, (255, 0, 0), 2)
        cv2.putText(src, "W {} mm".format(round(w * 0.315, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, Color.RED.value, 2)
        cv2.putText(src, "H {} mm".format(round(h * 0.315, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, Color.RED.value, 2)
        cv2.putText(src, "D {} deg".format(round(angle, 0)), (int(x - 100), int(y + 15 + 35)), cv2.FONT_HERSHEY_PLAIN, 2, Color.RED.value, 2)
        cv2.putText(src, "({},{})".format(int(x), int(y)), (int(x - 100), int(y + 15 + 35 + 35)), cv2.FONT_HERSHEY_PLAIN, 2, Color.RED.value, 2)
    return src

def goodFeature(src):
    gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    ret, gray = cv2.threshold(gray ,100, 255, cv2.THRESH_BINARY)
    #gray = cv2.adaptiveThreshold(gray ,128, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #return gray
    corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 5, blockSize=3, useHarrisDetector=True, k=0.03)

    pointListX = []
    pointListY = []

    src = cv2.rectangle(src, (100, 100), (800, 800), (255,255,255), 10)

    if corners is None:
        return src
    print(corners)
    for i in corners: #i[[100.,200.]]
        x = int(i[0][0])
        y = int(i[0][1])

        if 100 < x < 800:
            if 100 < y < 800:
                pointListX.append(x)
                pointListY.append(y)
                cv2.circle(src, (x, y), 3, (0, 255, 0), 2)
                cv2.circle(src, (pointListX[0], pointListY[0]), 3, (255, 0, 0), 2)

    pointListX.sort(reverse=True)
    pointListY.sort(reverse=True)

    if len(pointListX) == 0:
        return src
    if len(pointListY) == 0:
        return src
    cv2.circle(src, (pointListX[0], pointListY[0]), 3, (0, 0, 255), 2)
    cv2.circle(src, (pointListY[0], pointListX[0]), 3, (0, 0, 255), 2)
    pointListX.sort()
    pointListY.sort()
    cv2.circle(src, (pointListX[0], pointListY[0]), 3, (0, 0, 255), 2)
    cv2.circle(src, (pointListY[0], pointListX[0]), 3, (0, 0, 255), 2)
    return src

def cam(isSave = True):
    global cap, count
    if cap is None:
        print("캡쳐 객체가 없습니다.")
        return
    if not cap.isOpened():
        print("카메라가 종료되었습니다.")
        return
    count = count + 1
    print(f'width :{cap.get(3)}, height : {cap.get(4)} focus : {cap.get(cv2.CAP_PROP_FOCUS)} ({count})')

    ret, frame = cap.read()    # Read 결과와 frame

    if ret:
        #gray = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY)    # 입력 받은 화면 Gray로 변환
        #frame = cv2.resize(frame, dsize=(3264, 2448), interpolation=cv2.INTER_LINEAR)
        #frame = frame[:, 280:1080]  ## 정사각 aspect ratio 적용
        #frame = frame[:, 800:3000]  ## 정사각 aspect ratio 적용
        #frame = frame[:, (1280-720) // 2:720 + (1280-720) // 2]  ## 정사각 aspect ratio 적용
        #frame = cv2.resize(frame, dsize=(1080, 1080))
        frame = measureSize(frame)
        #frame = goodFeature(frame)
        
        cv2.imshow('로지텍', frame)
        if isSave:
            filename = "pic/사진.jpg"  
            imwrite(filename, frame)
    #cv2.destroyAllWindows()

def syncContext():
    global cap
    cap = cv2.VideoCapture()    
    cap.open(cv2.CAP_DSHOW)

    setCam(cap, 1280, 720)
    #setCam(cap, 3264, 2448)
    #setCam(cap, 3840, 2160)
    #setCam(cap, 1920, 1080)
    cv2.namedWindow('로지텍')
    while True:
        cam(isSave=False)
        key = cv2.waitKey(0)
        if key == KeyCode.Enter.value:
            break
    pass

syncContext()
      
