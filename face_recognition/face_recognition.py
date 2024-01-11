# @Version: python3.10
# @Time: 2024/1/5 23:53
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: face_recognition.py
# @Software: PyCharm
# @User: chent

import cv2 as cv
import os

def face_detection(image):
    # 转成灰度图像
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # 创建一个级联分类器 加载一个.xml分类器文件 它既可以是Haar特征也可以是LBP特征的分类器
    face_detecter = cv.CascadeClassifier(
        r'D:\Program Files\OpenCV\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
    # 多个尺度空间进行人脸检测   返回检测到的人脸区域坐标信息
    faces = face_detecter.detectMultiScale(image=gray, scaleFactor=1.1, minNeighbors=5)


    # print('检测人脸信息如下：\n', faces)
    # for x, y, w, h in faces:
    #     # 在原图像上绘制矩形标识
    #     cv.rectangle(img=image, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2)
    # cv.imshow('result', image)

    if len(faces) > 0:
        print('There is a face in the picture')
        return True
    else:
        print('There is no face in the picture')
        return False

if __name__ == '__main__':

    path = 'D:\ProgramingCodes\PycharmProjects\pythonProject\\face_recognition\\28.png'
    src = cv.imread(path)
    cv.imshow('input image', src)
    flag = face_detection(src)
    if flag:
        os.system(r"start D:\ProgramingCodes\PycharmProjects\pythonProject\\face_recognition")
    cv.waitKey(0)
    cv.destroyAllWindows()
