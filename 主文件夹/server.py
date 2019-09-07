import socket

import numpy as np

from PIL import ImageGrab


clisocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while 1:
    im = ImageGrab.grab()
    # im = im.resize((384, 162))
    da = np.array(im)
    for i in range(0, len(da)):
        clisocket.sendto(da[i], ('192.168.0.2', 1234))
    # clisocket.sendto(da, ("127.0.0.1", 1234))
clisocket.close()
