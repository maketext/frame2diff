from PIL import Image
import numpy as np

def boxing(im, initSize, count):
    """(initSize x initSize) 차원의 2D 이미지를 (count, count) 개의 서브 이미지로 분할
    Split the 2D image of (initSize x initSize) dimension into (count, count) sub-images

    :param im: 원본 이미지 Source Image
    :param initSize: 원본 이미지의 너비 또는 높이 크기 Size of the width or height of the source image
    :param count: 분할 옵션; (count, count) 개로 분할됨. Split option; split into (count, count).
    :return: 분할된 이미지 객체 배열, 분할된 각 이미지의 좌표 x1, y1, x2, y2를 담은 배열 Array of split image objects, Array containing coordinates x1, y1, x2, y2 of each split image
    """
    ims = []
    subset = []
    print(im)
    if isinstance(im, str):
        im = Image.open(im)
    im = im.resize(initSize)
    size = im.size
    unitSize = size[0] // count
    dst = Image.new('RGB', tuple(np.add(size,(1, 1))))

    def v(val):
        return val * size[0] // count

    def forward(x1, y1, x2, y2):
        if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0:
            return
        while True:
            subset.append((v(x1), v(y1), v(x2), v(y2)))
            sub = im.crop((v(x1), v(y1), v(x2), v(y2)))
            ims.append(sub)
            dst.paste(sub, (v(x1), v(y1), v(x2), v(y2)))

            x1 = x2
            y1 = y2
            x2 = x1 + 1
            y2 = y1 + 1
            if x1 > count or x2 > count or y1 > count or y2 > count:
                break

    forward(0, 0, 1, 1)
    for i in range(0, count - 1):
        x1, y1, x2, y2 = size[0] // unitSize - i - 1, 0, size[0] // unitSize - i, 1
        forward(x1, y1, x2, y2)
    for i in range(0, count - 1):
        x1, y1, x2, y2 = 0, size[1] // unitSize - i - 1, 1, size[1] // unitSize - i
        forward(x1, y1, x2, y2)
    #dst.show() # For validation by human eyes. Can be removed.
    return ims, subset
