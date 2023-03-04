"""Python Common Utils for Computer Vision"""

from PIL import Image
import numpy as np
import random
import math
import torch
import msvcrt
from os import listdir, remove
from os.path import isfile, join
from torchvision import transforms
import pygal
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def between(a, b, c):
    """a <= b < c 를 만족하는지 여부를 반환
    Args:
        a - 최소 값
        b - 비교할 값
        c - 최대 값

    Returns: b가 a와 c 사이에 있는 값인지 여부를 True, False로 반환
    """
    if a <= b and b < c:
        return True
    return False

def no(n, digit=3, initValue=0):
    """세 자리수 포멧인 000 부터 999까지의 숫자형 문자열 제너레이터
    Args:
        n - 자연수
        digit - 기본값 3. 이 값을 변경하면 N 자리수 포멧 제너레이터가 됨.
        initValue - 최초 카운팅 시작 값

    Returns: 포멧화된 문자열
    """
    n = n + initValue
    nArr = []
    length = len(str(n))
    if length < digit:
        for _ in range(digit - length):
            nArr.append('0')
    nArr.append(str(n))
    return ''.join(nArr)

def ceil(n):
    """소수 부분 올림 래퍼
    Args:
        n - 실수형

    Returns: 소숫점 올림한 실수
    """
    return math.ceil(n)

def trunc(n):
    """소수 부분 버림 래퍼
    Args:
        n - 실수형

    Returns: 소숫점 버림한 실수
    """
    return math.trunc(n)


def enter():
    """한 문자를 키보드 입력으로 받음

    - 숫자 1을 입력하면 True, 그렇지 않으면 False를 반환함.

    Args:
        없음.

    Returns: True, False 중 하나
    """
    ch = msvcrt.getch()
    print(ch)
    if ch == b'1':
        return True
    return False

def crop(im, a):
    """PIL crop 래퍼

    Args:
        테스트 하지 않음.

    Returns: 테스트 하지 않음.
    """
    return im.crop(a)

def getCenterPoint(x1, y1, x2, y2):
    """주어진 (x1, y1) 부터 (x2, y2) 영역의 중앙점을 반환

    Args:
        x1 - 좌표 값
        y1 - 좌표 값
        x2 - 좌표 값
        y2 - 좌표 값

    Returns: (x, y) 중앙 점 좌표
    """
    return ((x1 + x2) // 2, (y1 + y2) // 2)

def isEqualLabel(tensor, i):
    """딥러닝 모델 추론 결과 텐서 타입의 라벨에 스레시홀드를 적용하여 정상 여부를 True, False로 판정

    - i 파라미터 값이 1 이면 비품, 10이면 양품을 의미하는데 딥러닝 모델의 데이터셋과 맞아야 함.

    Args:
        tensor - 라벨링 부분을 의미마는 (,1) 1차원 텐서
        i - 판단할 라벨 값

    Returns: 없음
    """
    if isinstance(i, bool):
        if -30 <= tensor.float() <= 5 and i == True:
            return True
        if 5 < tensor.float() <= 20 and i == False:
            return True
    elif isinstance(i, (float, int)):
        if -30 <= tensor.float() <= 5 and i == 1:
            return True
        if 5 < tensor.float() <= 20 and i == 10:
            return True
    return False

def removeFolder(path):
    """주어진 폴더 경로 상의 모든 파일들을 삭제함.

    - 폴더 안의 폴더를 삭제하는지는 테스트 하지 않음

    Args:
        path - 폴더 경로

    Returns: 없음
    """

    files = [f for f in listdir(path) if isfile(join(path, f))]
    for i, file in enumerate(files):
        try:
            remove(f'{path}{file}')
        except FileNotFoundError as e:
            pass

def getRedChannnel():
    """이미지의 빨강 성분을 0-255 사이 값으로 추출함

    - 세그먼테이션용 딥러닝 모델의 추론 결과 관심 영역이 빨강색 계열로 색칠되어 있으며 이 부분만을 오려냄.

    Args:
        없음. 이미지 파일을 입력으로 받음
    Returns: 3차원 텐서
    """
    dst = Image.new('RGB', (225, 225), color=(255, 255, 255))
    #red = Image.new('RGB', (225, 225), color=(255, 31, 10))
    im = Image.open('../res/res63-0.jpg')
    w, h = im.size

    dst.paste(im=im, box=(0, 0, w, h), mask=im.getchannel('R'))

def transform(self, x):
    """파이토치 텐서 타입을 입력으로 받아 전통적 컴퓨터비전의 원근 변환 기법으로 변환하여 텐서 타입을 출력함.

    - 원근 변환의 결과는 주로 재생성 딥러닝 모델의 입력에 주입되며 모델의 결과 매번 조금씩 형상이 틀어진 이미지를 출력함.
    - 산업용 비품 데이터셋 생성에 활용

    Args:
        x - (batch, x, y) 3차원 텐서

    Returns: 3차원 텐서
    """

    def pxToNdarray(arr):
        arr = np.array(arr)
        return arr / 255
    def find_coeffs(pa, pb):
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

        A = np.matrix(matrix, dtype=np.float)
        B = np.array(pb).reshape(8)

        res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
        return np.array(res).reshape(8)
    r = random.randint(150, 224)
    r2 = random.randint(150, 224)
    coeffs = find_coeffs(
        [(0, 0), (r, 0), (r2, r), (0, r2)],
        [(0, 0), (r2, 0), (r, r2), (10, r)])
    x = transforms.ToPILImage()(x.squeeze())
    x = x.transform((224, 224), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    #x.show()
    return torch.tensor(pxToNdarray(x), dtype=torch.float32).permute(2, 0, 1).contiguous().unsqueeze(dim=0)

def torchVersion(eq):
    """파이토치 버전 확인용

    Args:
        eq - Version String e.g., 1.9.0+cu102
    Returns: True, False
    """
    if isinstance(eq, str):
        if eq == torch.__version__:
            print(fr"torch.__version__={torch.__version__} 이 일치합니다.")
            return True
        return False
    print(torch.__version__)
    return torch.__version__

def chart(cmd):
    """초안: 텍스트 파일을 열어 차트를 그려줌

    - matplotlib와 pygal 추가 라이브러리를 사용
    - pygal을 통해 svg 파일 익스포트시 이미지 에디터 프로그램으로 열리지 않고 브라우저를 통해 열어야 함.

    Args:
        cmd - '로스', '로스파이갈' 중 하나

    Returns: None
    """

    # 디렉토리 및 파일 이름에 맞추어 변경
    Roboto = fm.FontProperties(fname='./font/Roboto-Medium.ttf')

    if cmd == '로스':
        f = open("dat/loss.txt", 'r')
        '''
            파일의 형태
            ep=1 loss=46.19415283203125
            ...
        '''
        arr = []
        index = []
        cnt = 0
        while True:
            cnt = cnt + 1
            line = f.readline()
            if not line: break
            fl = float(line.split(' ')[1].split('=')[1])
            arr.append(np.trunc(fl * 10) / 10)
            index.append(cnt)

        plt.xlabel('Epoch',fontproperties = Roboto, fontsize=13)
        plt.ylabel('Loss rate',fontproperties = Roboto, fontsize=13)

        plt.ylim(0, 10)
        plt.plot(index, arr)
        #plt.yticks(np.arange(0, 100, 10))

        plt.axhline(y=0.3, color='r', linewidth=1, linestyle='--')
    elif cmd == '로스파이갈':
        line_chart = pygal.Line()
        line_chart.title = 'Browser usage evolution (in %)'
        line_chart.x_labels = map(str, range(2002, 2013))
        line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
        line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
        line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
        line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
        line_chart.render_to_file('dat/chart.svg')

    plt.show()


"""
초안
def equal(source, matchList):
    for i, dst in enumerate(matchList):
        if source == dst:
            return True
    return False

def arraySplit(arr, div=1):
    return np.array_split(arr, div)
def arrayFlat(arr):
    arr.shape = (1, arr.size)
"""
