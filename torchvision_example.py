import torch
import torchvision.transforms as T
import torchvision.transforms.functional as F
import PIL.Image as Image

t = torch.round(torch.rand(size=(5, 5, 3))) * 255
t = t.type(torch.uint8)
#t = torch.ByteTensor(100, 100, 3).random_(0, 255)

# torchvision example
tr = F.hflip(t)
tr = F.vflip(t)
tr = torch.rot90(t, 1, [0, 1])
tr = T.RandomPerspective(distortion_scale=0.6, p=1.0)(t)
# end

im = T.ToPILImage()(t.numpy())
imr = T.ToPILImage()(tr.numpy())
imr_w, imr_h = imr.size
bg = Image.new('RGB', (10, 5), (0, 0, 0))
bg_w, bg_h = bg.size

offset = (0, 0)
bg.paste(im, offset)
offset = (5, 0)
bg.paste(imr, offset)

bg.show()
