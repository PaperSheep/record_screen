import numpy as np

from PIL import ImageGrab


if __name__ == '__main__':
    # im = ImageGrab.grab()
    # # im = im.resize((2048, 864))
    # im.save('2.png')
    im = ImageGrab.grab()
    # im = im.resize((384, 162))
    da = np.array(im)
    print(da.shape)
    print(im.size)
    # print(len(da[0]))
    # print('123|frame_end'[:-10])
