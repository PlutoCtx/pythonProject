# @Version: python3.10
# @Time: 2024/1/23 14:27
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: rename_files_and_folders.py
# @Software: PyCharm
# @User: chent

import os
import shutil


def rename_folders_and_files(directory):
    # 遍历指定目录下的所有文件和文件夹
    for root, dirs, files in os.walk(directory):
        # 对每一个文件夹进行重命名
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            # 获取新的文件夹名称
            print(dir_name)
            new_dir_name = input("请输入新的文件夹名称: ")
            new_dir_path = os.path.join(root, new_dir_name)
            # 重命名文件夹
            os.rename(dir_path, new_dir_path)
            print(f"已将文件夹 {dir_name} 重命名为 {new_dir_name}")

            # 对文件夹内的所有文件进行重命名
            for file in files:
                file_path = os.path.join(root, file)
                # 获取新的文件名
                print(file_path)
                new_file_name = input(f"请输入新的文件名 (文件名前加上文件夹名): {new_dir_name} ")
                new_file_path = os.path.join(new_dir_path, new_file_name)
                # 重命名文件
                shutil.move(file_path, new_file_path)
                print(f"已将文件 {file} 重命名为 {new_file_name}")

            # 清空当前文件夹，因为已经将所有文件移动到了新的文件夹中
            shutil.rmtree(dir_path)
            print(f"已删除空文件夹 {dir_name}")
        # 使用示例


def rename_files_in_directory(directory, prefix):
    # 遍历指定目录下的所有文件和文件夹
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # 获取文件的相对路径（相对于指定目录）
            relative_path = os.path.relpath(file_path, directory)
            # 构建新的文件名
            new_name = prefix + relative_path
            new_path = os.path.join(directory, new_name)
            # 检查新文件名是否已存在
            if not os.path.exists(new_path):
                # 重命名文件
                shutil.move(file_path, new_path)
                print(f"已将文件 {file} 重命名为 {new_name}")
            else:
                print(f"新文件名 {new_name} 已存在，跳过重命名操作")


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

def get_file_name(directory):
    file_name_list = []
    for file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file_name)):
            file_name_list.append(directory + '\\\\' + file_name)
    return file_name_list


def change_files_name(directory, prefix):
    for file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file_name)):
            print(directory + '\\\\' + file_name)

            new_name = prefix + file_name
            rename_file(directory + '\\\\', file_name, new_name)

def rename_file(directory, old_name, new_name):
    try:
        os.rename(directory + old_name.replace('picpicpic', ''), directory + new_name.replace('picpicpic', ''))
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

if __name__ == '__main__':
    directory = 'D:\Documents\Test'  # 替换为你的文件夹路径
    rename_folders(directory)

    dir_list = get_folders_name(directory)
    prefix = 'pic'  # 替换为你想要的前缀

    for dir in dir_list:
        change_files_name(dir, prefix)

    all_file_paths = get_all_file_paths(directory)
    save_to_txt(all_file_paths, 'all_file_paths.txt')
