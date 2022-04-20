import cv2 #open-cv
# import paho.mqtt.client as mClient
# import time
# import threading
# import random
import os # 현재사용os에서 가능 파일위치등
from enum import Enum

#from cv2 import imwrite
# from sys import exit
  
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
    cap.set(cv2.CAP_PROP_FOCUS, 10)
    #cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

    return cap


def goodFeature(src):
    gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 5, blockSize=3, useHarrisDetector=True, k=0.03)

    if corners is None:
        return src
    for i in corners:
        print(int(i[0][0]), int(i[0][1]))
        cv2.circle(src, (int(i[0][0]), int(i[0][1])), 3, (0, 0, 255), 2)
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
        frame = frame[:, 800:3000]  ## 정사각 aspect ratio 적용
        frame = cv2.resize(frame, dsize=(1080, 1080))
        
        frame = goodFeature(frame)
        
        cv2.imshow('carmer/img', frame)
        if isSave:
            filename = "carmer/img.jpg"  
            imwrite(filename, frame)
    #cv2.destroyAllWindows()

def syncContext():
    global cap
    cap = cv2.VideoCapture()    
    cap.open(cv2.CAP_DSHOW)

    #setCam(cap, 1280, 720)
    #setCam(cap, 3264, 2448)
    #setCam(cap, 3840, 2160)
    setCam(cap, 1920, 1080)
    cv2.namedWindow('carmer.img')
    while True:
        cam(isSave=False)
        key = cv2.waitKey(0)
        if key == KeyCode.Enter.value:
            break
    pass

syncContext()
      