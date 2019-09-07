import os
import time

import cv2
import numpy as np
import win32api

from multiprocessing import Process, Manager
from threading import Thread

from PIL import ImageGrab



def video_synthesis(img_stream_list, length, width, name):
    list_size = len(img_stream_list)
    # print(list_size)
    pic_list = []
    for i in range(0, list_size):
        pic_list.append(img_stream_list[i])
    fps = 0
    if list_size > 60:
        fps = 30
        sub_num = list_size - 60
        base_num = sub_num // 5
        space_len_list = [base_num] * 5
        base_num *= 5
        for i in range(0, sub_num - base_num):
            space_len_list[i] = space_len_list[i] + 1
        # print(space_len_list)
        last_end = 10
        new_pic_list = pic_list[0: last_end]
        for space_len in space_len_list:
            last_end += space_len
            new_pic_list.extend(pic_list[last_end: last_end + 10])
        pic_list = new_pic_list
    else:
        fps = list_size // 2
    # print(len(pic_list))
    video_decode_style = cv2.VideoWriter_fourcc(*'XVID')  # 编码格式
    video = cv2.VideoWriter('video/{}.avi'.format(name), video_decode_style, fps, (length, width))  # 输出文件命名为a.avi,帧率为30，可以调节
    for pic in pic_list:
        imm = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
        video.write(imm)
    video.release()

def save_file(img_stream_list):
    print(type(img_stream_list[0]))
    print(img_stream_list[0])

# 图片流队列
def pic_queue(img_stream_list):
    while True:
        im = ImageGrab.grab()
        img_stream_list.append(im)

def listen_key(king_key_stat):
    while True:
        f12_key = win32api.GetKeyState(0x7B)  # 开始或终止录屏按键检测
        if f12_key < 0:
            king_key_stat['stat'] = False if king_key_stat['stat'] else True
        

if __name__ == '__main__':
    screen = ImageGrab.grab()  # 获得当前屏幕
    length, width = screen.size  # 获得当前屏幕的大小
    # video_process_list = []
    # 检测录制按键命令
    print('按f12进行屏幕录制\n')
    king_key_stat = {'stat': True}
    t = Thread(target=listen_key, args=(king_key_stat,))
    t.start()
    # 开始录制
    i = 0
    while True:
        if king_key_stat['stat']:
            continue
        process_list = []  # 存储处理截屏的进程列表
        img_stream_list = Manager().list()  # 多线程共享变量的写法
        start = time.time()
        for _ in range(0, 4):
            p = Process(target=pic_queue, args=(img_stream_list,))
            p.start()
            process_list.append(p)
        # 等待两秒
        while time.time() - start < 2:
            pass
        for p in process_list:
            p.terminate()
        # print(len(img_stream_list))
        # 启动线程进行合成
        p = Thread(target=video_synthesis, args=(img_stream_list, length, width, i))
        p.start()
        # video_process_list.append(p)
        i += 1
        print(i * 2, '秒')
    # print('等待多线程结束')
    # for p in video_process_list:
    #     p.join()
    print('全部合成结束')
