import cv2
import numpy as np
from sympy import Point, Polygon

import paho.mqtt.client as mClient
import os
from enum import Enum
from pathlib import Path

baseVSCodePath = "웹서버"

class KeyCode(Enum):
    Enter = 13
class Color(Enum):
    BLACK = (0, 0, 0)
    RED = (0, 0, 255)
    WHITE = (255, 255, 255)
cap = None
count = 0


def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)
        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
                return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

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

cap = None
count = 0

def setCam(cap, w, h):
    #cap = cv2.VideoCapture(cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    cap.set(cv2.CAP_PROP_FPS, 1)
    cap.set(cv2.CAP_PROP_FOCUS, 10)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

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

        p1, p2, p3, p4 = map(Point, box)
        poly = Polygon(p1, p2, p3, p4)
        print(fr'면적={poly.area}')
        if 190000 < poly.area < 300000:
            cv2.circle(src, (int(x), int(y)), 15, (0, 0, 255), -1)
            cv2.polylines(src, [box], True, (255, 0, 0), 2)
            cv2.putText(src, "W {} mm".format(round(w * 0.315, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, Color.RED.value, 2)
            cv2.putText(src, "H {} mm".format(round(h * 0.315, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, Color.RED.value, 2)
            cv2.putText(src, "D {} deg".format(round(angle, 0)), (int(x - 100), int(y + 15 + 35)), cv2.FONT_HERSHEY_PLAIN, 2, Color.RED.value, 2)
            cv2.putText(src, "({},{})".format(int(x), int(y)), (int(x - 100), int(y + 15 + 35 + 35)), cv2.FONT_HERSHEY_PLAIN, 2, Color.RED.value, 2)
            cv2.putText(src, "area={}".format(poly.area), (int(x - 100), int(y + 15 + 35 + 35 + 35)), cv2.FONT_HERSHEY_PLAIN, 2, Color.RED.value, 2)
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


brokerAddr = "127.0.0.1"
brokerPort = 1883

def conn() -> mClient:
    def on_connect(client, userData, flags, rc):
        if rc == 0:
            print("연결됨")
            pass
    def on_disconnect(client, userData, flags, rc=0):
        pass
    clientId = f'cli-python-cam'
    client = mClient.Client(clientId)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect(host=brokerAddr, port=brokerPort)
    return client

def setCam(cap, w, h):
    #cap = cv2.VideoCapture(cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    cap.set(cv2.CAP_PROP_FPS, 1)
    cap.set(cv2.CAP_PROP_FOCUS, 8)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    return cap

def setThresHold(im):
    def compare(a, gt=(255, 255, 255)):
        if a[0] + a[2] < a[1]:
            return (255, 255, 255)
        return (0, 0, 0)

    im.putdata(list(map(lambda x: compare(x), im.getdata())))


filename1 = fr'{Path.home()}/Pictures/cam.jpg'
filename2 = fr'{baseVSCodePath}\res\img\웹캠.jpg'
def cam(isSave = True):
    global cap
    if cap is None:
        print("캡쳐 객체가 없습니다.")
        return
    if not cap.isOpened():
        print("카메라가 종료되었습니다.")
        return
    print(f'width :{cap.get(3)}, height : {cap.get(4)} focus : {cap.get(cv2.CAP_PROP_FOCUS)} ({count})')

    ret, frame = cap.read()    # Read 결과와 frame

    if ret:
        h, w , _ = frame.shape
        frame = measureSize(frame)
        imwrite(filename2, frame)
        pub('/img-save-ready')

def pub(topic):
    res = client.publish(topic=topic, qos=0)
    stat = res[0]
    if stat == 0:
        pass
        print(f"PUB topic={topic} 퍼블리시됨.")

def on_message(_, userData, msg):
    global cap, count
    if msg.topic == '/img-start':
        print("카메라 시작")
        if cap is None:
            cap = cv2.VideoCapture()
            cap.open(cv2.CAP_DSHOW)
            setCam(cap, 3264, 2448) ## QSENN QC4K 웹캠 의 에스펙트 레이시오입니다.
            # setCam(cap, 1280, 720)
            # setCam(cap, 3840, 2160) ## 로지텍 BRIO 4K 웹캠의 에스펙트 레이시오입니다.
            # setCam(cap, 1920, 1080)
            # setCam(cap, 1280, 720)

        pub('/img-start-ready')
    elif msg.topic == '/img-recv':
        cam()
    elif msg.topic == '/img-stop':
        count = count + 1
        print("카메라 종료")
        if cap is not None:
            cap.set(cv2.CAP_PROP_FPS, 0)
            if count % 100 == 0:
                print(f"카메라 객체 반환됨. 100주기 반환 카운트({count})")
                cap.release() # 카메라 객체 릴리즈 시 QSENN QC4K 웹캠에서 딸깍 거리는 기계식 스위치 소리가 납니다. 스위치는 내구도가 약하므로 최대한 릴리즈를 덜 하는 방향으로 소스코드를 수정하였습니다.
                cap = None

    elif msg.topic == '/cam-release':
        if cap is not None:
            cap.release()
        cap = None
        print("카메라 객체 반환됨.")
    else:
        pass

def sub(topic):
    print(f'sub: MQ {topic}')
    client.subscribe(topic, qos=0)


def run(client, flag):
    sub('/img-recv')
    sub('/img-start')
    sub('/img-stop')
    sub('/cam-release')
    print("무한루프 시작")

    if flag == 'loop_forever':
        client.loop_forever()
    elif flag == 'loop_start':
        client.loop_start()

client = conn()
client.on_message = on_message
run(client, 'loop_forever')
