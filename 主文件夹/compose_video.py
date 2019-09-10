import os

from moviepy.editor import VideoFileClip, concatenate_videoclips


if __name__ == '__main__':
    path_item_list = os.listdir('video/')
    vfc_list = []
    # for i in range(0, len(path_item_list)):
    for i in range(0, 90):
        vfc_list.append(VideoFileClip('video/{}.avi'.format(i)))
        if i % 30 == 0:
            finalclip = concatenate_videoclips(vfc_list, method='compose')  # vfc_list为VideoFileClip的对象组成的list
            finalclip.write_videofile('temp_c.mp4')
            if(os.path.exists('temp.mp4')):
                os.remove('temp.mp4')
            os.rename('temp_c.mp4', 'temp.mp4')
            vfc_list = []
            vfc_list.append(VideoFileClip('temp.mp4'))
    finalclip = concatenate_videoclips(vfc_list, method='compose')  # vfc_list为VideoFileClip的对象组成的list
    finalclip.write_videofile('my_concatenate.mp4')
    os.remove('temp.mp4')  # 删除临时合成的视频
    print('全部完成')
    # clip.write_videofile(path, codec='mpeg4', verbose=False, audio=False)
