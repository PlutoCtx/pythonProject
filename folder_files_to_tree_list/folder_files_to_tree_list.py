# @Version: python3.10
# @Time: 2024/1/14 0:51
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: folder_files_to_tree_list.py
# @Software: PyCharm
# @User: chent

from pathlib import Path

tree_str = ''


def generate_tree(pathname, n=0):
    global tree_str
    # tree_str = ''
    # if pathname.is_file():
    #     tree_str += '    |' * n + '-' * 4 + pathname.name + '\n'
    # elif pathname.is_dir():
    if pathname.is_dir():
        tree_str += '    |' * n + '-' * 4 + \
                    str(pathname.relative_to(pathname.parent)) + '\\' + '\n'
        for cp in pathname.iterdir():
            generate_tree(cp, n + 1)



if __name__ == '__main__':
    folders = [
        # '个人项目实训',
        # '书籍资料',
        # '教学视频',
        # '教学01',
        # '旧电脑教学视频',
        # '项目教学',
        '【02】开发相关',
        # '视频',
        # '资料',
        # '阿里',
        # '下载完成',
        # '教学',
        # '教学02',
    ]
    for i in folders:
        path = 'F:\\' + i
        # tree_ = ''
        generate_tree(Path(path), 0)
        # print(tree_str)
        print(i)
        f = open(i + '.txt', 'wb')
        f.write(tree_str.encode('utf-8'))
        f.close()
