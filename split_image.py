from PIL import Image
import numpy as np

def boxing(im, count):
    ims = []

    if isinstance(im, str):
        im = Image.open(im)
    im = im.resize((224, 224))
    size = im.size
    unitSize = size[0] // count
    dst = Image.new('RGB', tuple(np.add(size,(1, 1))))

    def v(val):
        return val * size[0] // count

    def forward(x1, y1, x2, y2):
        if x1 < 0 or x2 < 0 or y1 < 0 or y2 < 0:
            return
        while True:
            print(v(x1), v(y1), v(x2), v(y2))
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
    return ims


boxing('img/mold1.png', 8)  # Split image 8 by 8
