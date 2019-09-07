import socket
import os, sys, pygame
from pygame.locals import *
 
pygame.init()
screen = pygame.display.set_mode((1368, 912))
pygame.display.set_caption("web cam")
 
pygame.display.flip()
svrsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
svrsocket.bind(('0.0.0.0', 1234))
clock = pygame.time.Clock()  # 计算帧速
while 1:
    data, address = svrsocket.recvfrom(80000)
    print(type(data))
    print(len(data))
    # data = list(data)
    for i in range(1, 304): 
        data += svrsocket.recvfrom(80000)[0]
    print(len(data))
    camshot = pygame.image.frombuffer(data, (1368, 912), "RGB")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.blit(camshot, (0,0))
    pygame.display.update() 
    print(clock.get_fps())  # 在终端打印帧速

