# @Version: python3.10
# @Time: 2023/11/28 16:05
# @Author: PlutoCtx
# @Email: 15905898514@163.com
# @File: merge_srt_and_videos.py
# @Software: PyCharm
# @User: chent

from os.path import splitext, isfile

from moviepy.editor import (VideoFileClip,
                            TextClip,
                            CompositeVideoClip)


# 读取字幕文件
def read_srt(path):
    with open(path, 'r', encoding='UTF-8') as f:
        srt_content = f.read()
        return srt_content


# 字幕拆分
def get_sequences(srt_content):
    srt_sequences = srt_content.split('\n\n')
    srt_sequences = [sequence.split('\n') for sequence in srt_sequences]
    # 去除每一句空值
    srt_sequences = [list(filter(None, sequence)) for sequence in srt_sequences]
    # 去除整体空值
    return list(filter(None, srt_sequences))


def strFloatTime(tempStr):
    xx = tempStr.split(':')
    hour = int(xx[0])
    minute = int(xx[1])
    second = int(xx[2].split(',')[0])
    minSecond = int(xx[2].split(',')[1])
    allTime = hour * 60 * 60 + minute * 60 + second + minSecond / 1000
    return allTime


class RealizeAddSubtitles():
    """
    合成字幕与视频
    """

    def __init__(self, videoFile, txtFile):
        self.src_video = videoFile
        self.sentences = txtFile
        if not (isfile(self.src_video)
                and self.src_video.endswith(('.avi', '.mp4'))
                and isfile(self.sentences)
                and self.sentences.endswith('.srt')):
            print('视频仅支持avi以及mp4，字幕仅支持srt格式')
        else:
            video = VideoFileClip(self.src_video)
            # 获取视频的宽度和高度
            w, h = video.w, video.h
            # 所有字幕剪辑
            txts = []
            content = read_srt(self.sentences)
            sequences = get_sequences(content)

            for line in sequences:
                if len(line) < 3:
                    continue
                sentences = line[2]
                start = line[1].split(' --> ')[0]
                end = line[1].split(' --> ')[1]

                start = strFloatTime(start)
                end = strFloatTime(end)

                start, end = map(float, (start, end))
                span = end - start
                txt = (TextClip(sentences, fontsize=40,
                                font='SimHei', size=(w - 20, 40),
                                align='center', color='red')
                       .set_position((10, h - 150))
                       .set_duration(span)
                       .set_start(start))

                txts.append(txt)
            # 合成视频，写入文件
            video = CompositeVideoClip([video, *txts])
            fn, ext = splitext(self.src_video)
            video.write_videofile(f'{fn}_2带字幕{ext}')


if __name__ == '__main__':
    '''调用方法示例'''

    srt_path = 'D:\桌面\百度\convex optimizations\Lecture+1-Introduction.srt'
    # content = read_srt(srt_path)
    # sequences = get_sequences(content)
    # print(sequences)
    # strTime = '00:55:03,000'

    addSubtitles = RealizeAddSubtitles("D:\桌面\百度\convex optimizations\Lecture+1-Introduction.mp4", srt_path)
