# @Version: python3.10
# @Time: 2024/1/5 23:53
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: face_recognition.py
# @Software: PyCharm
# @User: chent

import cv2 as cv
import os


def get_folders_name(directory):
    dir_list = []
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            dir_list.append(os.path.join(root, dir))
    return dir_list


def rename_folders(directory):
    # 遍历指定目录下的所有文件和文件夹
    for root, dirs, files in os.walk(directory):
        # 对每一个文件夹进行重命名
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            # 获取新的文件夹名称
            # print(dir_name)
            # new_dir_name = input("请输入新的文件夹名称: ")
            new_dir_name = dir_name.replace('【', '[').replace('】', ']')
            new_dir_path = os.path.join(root, new_dir_name)
            # 重命名文件夹
            os.rename(dir_path, new_dir_path)
            # print(f"已将文件夹 {dir_name} 重命名为 {new_dir_name}")


def change_files_name(directory, prefix):
    for file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file_name)):
            print(directory + '\\\\' + file_name)

            new_name = prefix + file_name
            rename_file(directory + '\\\\', file_name, new_name)

def rename_file(directory, old_name, new_name):
    new_name = 'pic' + new_name.replace('pic', '')
    try:
        os.rename(directory + old_name, directory + new_name)
        print(f'{old_name} -> {new_name}')
    except OSError as e:
        print(f'{e}')


def get_all_file_paths(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files

def save_to_txt(file_paths, filename):
    with open(filename, 'w') as f:
        for file_path in file_paths:
            f.write(file_path + '\n')
            print(file_path)



def remove_qr_code_images(pic_path):
    # 加载图片并检测二维码
    img = cv.imread(pic_path)
    qr_detector = cv.QRCodeDetector()
    data, bbox, _ = qr_detector.detectAndDecode(img)

    # 如果检测到二维码，则删除该图片
    if data:
        print(f"Deleting image with QR Code: {pic_path}")
        os.remove(pic_path)  # 或者使用 shutil.rmtree() 来删除整个文件夹中的图片，如果它们都包含二维码的话
    return data

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

    directory = 'D:\Documents\公众号爬取'  # 替换为你的文件夹路径
    rename_folders(directory)

    dir_list = get_folders_name(directory)
    prefix = 'pic'  # 替换为你想要的前缀

    for dir in dir_list:
        change_files_name(dir, prefix)

    all_file_paths = get_all_file_paths(directory)



    for path in all_file_paths:
        if remove_qr_code_images(path):
            continue
        # src = cv.imread(path)
        # cv.imshow('input image', src)
        # flag = face_detection(src)
        # if not flag:
        #     os.system(r"start " + path)
        # cv.waitKey(0)
        # cv.destroyAllWindows()







    # path = 'D:\ProgramingCodes\PycharmProjects\pythonProject\\face_recognition\\28.png'
    # src = cv.imread(path)
    # cv.imshow('input image', src)
    # flag = face_detection(src)
    # if flag:
    #     os.system(r"start D:\ProgramingCodes\PycharmProjects\pythonProject\\face_recognition")
    # cv.waitKey(0)
    # cv.destroyAllWindows()
