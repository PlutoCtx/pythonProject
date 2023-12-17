# @Version: python3.10
# @Time: 2023/11/27 20:32
# @Author: PlutoCtx
# @Email: 15905898514@163.com
# @File: ts_to_mp4.py
# @Software: PyCharm
# @User: chent

import requests
import os

# 整合文件夹下所有ts文件，保存为mp4格式
def tsToMp4():
    print("开始合并...")
    root = "D:\桌面\公考\励行公考\【8】省考冲刺轮23.11.27-23.12.9"
    outdir = "output"
    os.chdir(root)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    os.system("copy /b *.ts merged_video.mp4")
    os.system("move merged_video.mp4 {}".format(outdir))
    print("结束合并...")


if __name__ == '__main__':
    tsToMp4()



