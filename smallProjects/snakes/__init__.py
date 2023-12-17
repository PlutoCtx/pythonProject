# @Version: python3.10
# @Time: 2023/12/17 17:17
# @Author: PlutoCtx
# @Email: 15905898514@163.com
# @File: __init__.py.py
# @Software: PyCharm
# @User: chent

""""""
"""
贪吃蛇游戏是一款经典的益智游戏，既简单又耐玩。回味童年经典，今天我们来一同学习贪吃蛇游戏的制作。

课题：《使用 Python 制作贪吃蛇小游戏》
课程时间：20:00-22:00
讲师：正心老师

开发环境：
    1. 解释器： Python 3.6.5 | Anaconda, Inc.
    2. 编辑器： pycharm 社区版

课程收获：Python游戏开发的核心知识点，程序员需要掌握的核心技能
    1. Python开发游戏的流程
    2. 如何用编程思维设计游戏
    3. PyGame 游戏模块的使用

有不懂的随时在讨论区问出来

做一个项目流程是什么？
    + 需求文档
    + 开发文档
pip install pygame
"""
import pygame
import random
import copy

# 初始化蛇移动的位置
move_up = False
move_down = True
move_left = False
move_right = False

# 1.1 游戏初始化
pygame.init()
clock = pygame.time.Clock()  # 设置游戏时钟，帧率 fps
pygame.display.set_caption('贪吃蛇小游戏')
screen = pygame.display.set_mode((500, 500))  # 设置窗口大小
# 随机生成一个整数
x = random.randint(10, 490)
y = random.randint(10, 490)
food_point = [x, y]

# 蛇 有很多个点
snake_list = [
    [10, 10]
]

# 1.2 启动游戏
running = True  # 死循环的开关
while running:
    # 1.3 设置帧率
    clock.tick(20)  # 一秒钟刷新20次

    # 1.4 设置窗口的背景
    screen.fill([255, 255, 255])  # 三原色

    food_rect = pygame.draw.circle(screen, [255, 0, 0], food_point, 15, 0)

    snake_rect = []  # 蛇的身子在页面的图像
    for pos in snake_list:  # 遍历蛇的每一个点
        snake_rect.append(pygame.draw.circle(screen, [255, 0, 0], pos, 5, 0))

        # 只要蛇碰到了食物就吃掉食物，并且重新生成新的食物
        if food_rect.collidepoint(pos):
            snake_list.append(food_point)
            # 重新生成食物
            food_point = [random.randint(10, 490), random.randint(10, 490)]
            food_rect = pygame.draw.circle(screen, [255, 0, 0], food_point, 15, 0)
            break
    # 移动蛇的位置

    # 先把身子走一下
    pos = len(snake_list) - 1
    while pos > 0:
        snake_list[pos] = copy.deepcopy(snake_list[pos - 1])
        pos -= 1
    # pos = 0  # 获取蛇的头部位置

    if move_right:
        # x += 10 就可以不断往右走
        snake_list[pos][0] += 10
        if snake_list[pos][0] > 500:
            snake_list[pos][0] = 0

    if move_left:
        # x += 10 就可以不断往右走
        snake_list[pos][0] -= 10
        if snake_list[pos][0] < 0:
            snake_list[pos][0] = 500

    if move_up:
        snake_list[pos][1] -= 10
        if snake_list[pos][1] < 0:
            snake_list[pos][1] = 500

    if move_down:
        snake_list[pos][1] += 10
        if snake_list[pos][1] > 500:
            snake_list[pos][1] = 0

    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.KEYDOWN:
            # 判断上下左右的按键
            if event.key == pygame.K_UP:
                print('上')
                move_up = True
                move_down = False
                move_left = False
                move_right = False
            if event.key == pygame.K_DOWN:
                print('下')
                move_up = False
                move_down = True
                move_left = False
                move_right = False
            if event.key == pygame.K_LEFT:
                print('左')
                move_up = False
                move_down = False
                move_left = True
                move_right = False
            if event.key == pygame.K_RIGHT:
                print('右')
                move_up = False
                move_down = False
                move_left = False
                move_right = True

            # 你们平时敲的代码多吗

    # 蛇吃掉自己，结束游戏
    # 如果蛇吃掉了自己，就结束游戏
    head_rect = snake_rect[0]
    count = len(snake_rect)
    while count > 1:
        if head_rect.colliderect(snake_rect[count - 1]):
            running = False
        count -= 1

    # 将内容显示到界面
    pygame.display.update()


