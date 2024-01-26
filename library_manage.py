# @Version: python3.10
# @Time: 2024/1/14 18:06
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: library_manage.py
# @Software: PyCharm
# @User: chent


import os

book_info = {}
book_stock = {}


def init():
    book_info[123] = {
        'name': 'Java',
        'num': 11
    }
    book_stock[123] = 12


def print_menu():
    print("=======主菜单========")
    print("     1-显示书目信息")
    print("     2-显示库存信息")
    print("     3-添加书籍信息")
    print("     4-增加图书库存量")
    print("     5-图书查找")
    print("     6-图书借阅/归还")
    print("     0-结束")
    opt = "#"
    while opt not in "0123456" and opt != '':
        opt = input("请输入操作数: ")
    return int(opt)


# 显示书目信息
def print_book_info():
    # 打印基本信息
    print('书号\t\t书名\t\t价格')
    # 计算信息长度 格式化
    # 遍历书目并打印
    for key in book_info:
        book = book_info[key]
        print('%d\t\t%s\t%d' % (key, book['name'], book['num']))



# 显示库存信息
# 显示书名 库存量
def print_book_stock():
    print('书名\t\t库存')
    # 遍历库存字典
    for key in book_stock:
        print('%s\t%d' % (book_info[key]['name'], book_stock[key]))


# 添加书目信息
def add_book_info():
    book_no = int(input("输入书号: "))
    # 书号存在
    if book_info.get(book_no) is not None:
        print(f'已存在书号{book_no},书名为{book_info[book_no]["name"]}')
        while True:
            opt = input('是否覆盖已存在书籍信息,输入Y/N: ')
            if opt.lower() in 'yn':
                if opt.lower() == 'n':
                    return
                break
    book_info[book_no] = {
        'name': input('输入书名: '),
        'num': int(input('输入价格: '))
    }
    book_stock[book_no] = int(input("输入该书籍的库存: "))


# 修改库存信息
def modify_book_stock():
    book_no = int(input('输入书号: '))
    if book_stock.get(book_no) is not None:
        book_stock[book_no] = int(input("输入修改后的库存: "))
    else:
        print("书号不存在")
# 修改书目信息
def modify_book_info(book_no=None):
    if book_no is None:
        book_no = int(input("输入书号: "))
    book_info[book_no] = {
        'name': input('输入书名: '),
        'num': int(input('输入数量: '))
    }
def search_book_info():
    # book_name = input('请输入书名：')
    book_no = int(input('输入待查询书号: '))
    if book_stock.get(book_no) is not None:
        print('书号\t\t书名\t\t价格\t\t库存数')
        print(book_no, '   ' + book_info[book_no]['name'], '    ' + str(book_info[book_no]['num']), '    ' + str(book_stock[book_no]))
    else:
        print("书号不存在")

def borrow_or_lend_book():
    book_no = int(input('输入待借阅/归还书号: '))
    if book_stock.get(book_no) is not None:
        print('书号\t\t书名\t\t价格\t\t库存数')
        print(book_no, '   ' + book_info[book_no]['name'], '    ' + str(book_info[book_no]['num']),
              '    ' + str(book_stock[book_no]))

        act = int(input('如选择借阅，请按 1；如选择归还，请按 0：'))
        if act == 0:
            book_stock[book_no] += 1
            print('书号\t\t书名\t\t价格\t\t库存数')
            print(book_no, '   ' + book_info[book_no]['name'], '    ' + str(book_info[book_no]['num']),
                  '    ' + str(book_stock[book_no]))
        elif act == 1:
            if book_stock[book_no] < 1:
                print('无法借阅')
            else:
                print('借阅成功')
                book_stock[book_no] -= 1
                print('书号\t\t书名\t\t价格\t\t库存数')
                print(book_no, '   ' + book_info[book_no]['name'], '    ' + str(book_info[book_no]['num']),
                      '    ' + str(book_stock[book_no]))

    else:
        print("书号不存在")

def handling(opt):
    if opt == 1:
        print_book_info()
    elif opt == 2:
        print_book_stock()
    elif opt == 3:
        add_book_info()
    elif opt == 4:
        modify_book_stock()
    elif opt == 5:
        search_book_info()
    elif opt == 6:
        borrow_or_lend_book()
    else:
        exit(0)
    clear()


def clear(info=''):
    # 打印完阻塞控制台 按任意键继续
    input(f"${info} 按任意键继续.......")
    os.system("cls")
    # cmd可以实现清屏


if __name__ == '__main__':
    init()
    while True:
        try:
            handling(print_menu())
        except:
            clear('程序错误')