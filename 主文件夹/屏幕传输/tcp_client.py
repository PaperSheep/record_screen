import socket
import time

import numpy as np

from PIL import ImageGrab


def send_from(arr, dest):
    view = memoryview(arr).cast('B')
    while len(view):
        nsent = dest.send(view)
        view = view[nsent:]

if __name__ == '__main__':
    client = None
    # 初连接
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 1234))  # 与服务器的地址连接
        # 第一次接收服务端的数据，若收到连接成功的状态则开始传输数据
        data = client.recv(1024)
        data_tup = str(data, 'utf-8').split('|')  # (状态码, 状态信息)
        if len(data_tup) != 2 or data_tup[0] != '200':
            print('连接失败，正在等待重新连接')
            client.close()
            time.sleep(2)
        else:
            print('连接成功，正在往服务器发送屏幕数据')
            break
    # 循环发送屏幕数据
    screen = ImageGrab.grab()  # 当前帧截图
    length, width = screen.size  # 获得当前屏幕的大小
    screen_size = '{}x{}'.format(length, width)
    client.send(screen_size.encode('utf-8'))  # 发送屏幕分辨率
    while True:
        screen = ImageGrab.grab()  # 当前帧截图
        start_tag = 'frame_start'
        client.send(start_tag.encode('utf-8'))  # 发送开始标签
        start_msg = client.recv(1024)
        start_msg = str(start_msg, 'utf-8')
        print(start_msg)
        # start_msg.encode('utf-8')
        if start_msg != 'start':
            print('没收到发送数据指令')
        data = np.array(screen)
        # send_from(data, client)
        client.sendall(data)
        # client.sendall(screen)
        client.sendall(b'|frame_end')
        # for i in range(0, len(data)):
            # print(data[i])
            # print(len(data[i]))
            # client.sendall(data[i])
            # break
        print('等待服务端的结束指令')
        is_end = client.recv(1024)
        is_end.decode('utf-8')
        if is_end == 'frame_end':
            continue
        # end_tag = 'frame_end'
        # client.send(end_tag.encode('utf-8'))  # 发送结束标签
    client.close()
