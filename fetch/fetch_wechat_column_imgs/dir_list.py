# @Version: python3.10
# @Time: 2024/1/6 23:02
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: dir_list.py
# @Software: PyCharm
# @User: chent

import os
import cv2 as cv


def get_file_list(dir, FileList):
    if os.path.isfile(dir):
        FileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            get_file_list(newDir, FileList)
    return FileList



def face_detection(image):
    # 转成灰度图像
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # 创建一个级联分类器 加载一个.xml分类器文件 它既可以是Haar特征也可以是LBP特征的分类器
    face_detecter = cv.CascadeClassifier(
        r'D:\Program Files\OpenCV\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
    # 多个尺度空间进行人脸检测   返回检测到的人脸区域坐标信息
    faces = face_detecter.detectMultiScale(image=gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        print('There is a face in the picture')
        return True
    else:
        print('There is no face in the picture')
        return False

def exist_face(img_url):
    src = cv.imread(img_url)
    flag = face_detection(src)
    print(flag)
    try:
        if not flag:
            os.system(r"start " + img_url)
    except:
        print('error!!!')

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    file_folder_path = '/fetch/fetch_wechat_column_imgs/Test'
    img_list = get_file_list(file_folder_path, [])


    for i in range(len(img_list)):
        print(img_list[i])
        exist_face(img_list[i])
    # print(img_list[4])
    # D:\ProgramingCodes\PycharmProjects\pythonProject\\fetch_wechat_column_imgs\\test\【00000】\\10.png

    # exist_face('D:\ProgramingCodes\PycharmProjects\pythonProject\\face_recognition\\28.png')












