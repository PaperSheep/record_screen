import socket
import time
import os, sys

# from multiprocessing import Process, Manager
from threading import Thread

import numpy as np
import pygame
from pygame.locals import *


def recv_into(arr, source):
    view = memoryview(arr).cast('B')
    while len(view):
        nrecv = source.recv_into(view)
        view = view[nrecv:]


def link_client(sock):
    # 这个位置可以添加阻拦特定客户端
    connect_msg = '200|success'
    sock.send(connect_msg.encode('utf-8'))
    data = sock.recv(1024)
    screen_size = str(data, 'utf-8').split('x')
    print(screen_size)
    length = int(screen_size[0])
    width = int(screen_size[1])
    screen_size = length * width
    # 初始化终端
    pygame.init()
    screen = pygame.display.set_mode((length, width))
    pygame.display.set_caption(str(sock))
    # 显示帧数据
    while True:
        is_start = sock.recv(1024)
        is_start = str(is_start, 'utf-8')
        if is_start == 'frame_start':
            sock.send(b'start')
            # has_recv = 0
            data = b''
            while b'|frame_end' not in data:
                data += sock.recv(10240)
                # has_recv = len(data)
                # print(data)
                # break
            # data = np.array(data[:-10], dtype = np.int16)
            data = data[:-10]
            # data = np.zeros(shape=(width, length, 3))
            # recv_into(data, sock)
            print(len(data))
            # data = np.array(data)
            # print(data[0])
            # break
            # camshot = pygame.image.frombuffer(data, (width, length), "RGB")
            camshot = pygame.image.frombuffer(data, (length, width), "RGB")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            screen.blit(camshot, (0,0))
            pygame.display.update()
            end_tag = 'frame_end'
            sock.send(end_tag.encode('utf-8'))

if __name__ == '__main__':
    # 第一个参数是ipv4，第二个参数是tcp
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 1234))
    server.listen()  # 开始监听
    # 客户端连接成功则进行下去，否则阻塞在这
    sock, addr = server.accept()
    print('连接成功{}'.format(sock))
    # 启动线程
    # p = Process(target=link_client, args=(sock,))
    # p.start()
    t = Thread(target=link_client, args=(sock,))
    t.start()
