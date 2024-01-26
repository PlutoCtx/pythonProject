# @Version: python3.10
# @Time: 2024/1/14 1:04
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: list_tree_to_json.py
# @Software: PyCharm
# @User: chent

import os
import json


def get_directory_tree(path):
    tree = {"name": os.path.basename(path)}
    if os.path.isdir(path):
        tree["type"] = "directory"
        tree["content"] = []
        for filename in os.listdir(path):
            if os.path.isdir(path):
                child = os.path.join(path, filename)
                tree["content"].append(get_directory_tree(child))
    else:
        tree["type"] = "file"

    return tree


# if os.path.isdir(path):
#     print "it's a directory"
# elif os.path.isfile(path):
#     print "it's a normal file"
# else:
#     print "it's a special file(socket,FIFO,device file)"






def directory_tree_to_json(tree):
    return json.dumps(tree, indent=2)



if __name__ == '__main__':
    # 获取目录树信息
    tree = get_directory_tree("D:\Documents")

    # 将目录树转换为JSON
    json_data = directory_tree_to_json(tree)

    print(json_data)
    with open('list_tree.json', 'w') as f:
        json.dump(json_data, f)



