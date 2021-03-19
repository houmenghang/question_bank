"""贪吃蛇"""
"""贪吃蛇"""

import random
import sys
import time
import pygame

from pygame.locals import *
from collections import deque

SCREEN_WIDTH = 600      # 屏幕宽度
SCREEN_HEIGHT = 480     # 屏幕高度
SIZE = 20               # 小方格大小
LINE_WIDTH = 1          # 网格线宽度

# 游戏区域的坐标范围
SCOPE_X = (0, SCREEN_WIDTH // SIZE - 1)
SCOPE_Y = (2, SCREEN_HEIGHT // SIZE - 1)

# 食物的分值及颜色
FOOD_STYLE_LIST = [(10, (255, 100, 100)), (20, (100, 255, 100)), (30, (100, 100, 255))]

LIGHT = (100, 100, 100)
SNAKE_COLOR = (100, 200, 100)      # 蛇的颜色
WALL_COLOR = (150,150,150)
BLACK = (0, 0, 0)           # 网格线颜色
RED = (200, 30, 30)         # 红色，GAME OVER 的字体颜色
BGCOLOR = (40, 40, 60)      # 背景色

def init_wall(wall_num):
    wall = deque()
    for j in range(10, 20):
        wall.append((j,5))
    for j in range(10, 20):
        wall.append((j,15))
    for j in range(5, 15):
        wall.append((10,j))
    for j in range(5, 9):
        wall.append((20,j))
    for j in range(13, 16):
        wall.append((20,j))
    return wall
def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    """
    :param screen:
    :param font:
    :param x:
    :param y:
    :param text:
    :param fcolor:
    :return: None
    """
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


def init_snake():
    snake = deque()
    snake.append((2, SCOPE_Y[0]))
    snake.append((1, SCOPE_Y[0]))
    snake.append((0, SCOPE_Y[0]))
    return snake


def create_food(snake,wall):

    """
    this function have judged that the food is not in snake
    :param snake
    :return: food_list
    """
    food_list=[]
    for i in range(3):
        food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
        food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
        while ((food_x, food_y) in snake)or((food_x, food_y) in wall):
            food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
            food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
        food_list.append((food_x, food_y))
    return food_list


def get_food_style():
    food_style_list = []
    for i in range(3):
        food_style_list.append(FOOD_STYLE_LIST[random.randint(0, 2)])
    return food_style_list


def draw_line(screen):
    """
    need : BGCOLOR, SIZE, SCREEN_WIDTH,SCREEN_HEIGHT
    :param screen:
    :return:
    """
    # 填充背景色
    screen.fill(BGCOLOR)
    # 画网格线 竖线
    for x in range(SIZE, SCREEN_WIDTH, SIZE):
        pygame.draw.line(screen, BLACK, (x, SCOPE_Y[0] * SIZE), (x, SCREEN_HEIGHT), LINE_WIDTH)
    # 画网格线 横线
    for y in range(SCOPE_Y[0] * SIZE, SCREEN_HEIGHT, SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y), LINE_WIDTH)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 设置屏幕初始化
    pygame.display.set_caption('贪吃蛇 2.0')

    font1 = pygame.font.SysFont('SimHei', 24)  # 得分的字体
    font2 = pygame.font.Font(None, 72)         # GAME OVER 的字体
    fwidth, fheight = font2.size('GAME OVER')  # 得到game over时的字体大小，用于屏幕输出

    error_flag = True                          # 用于判断是否连续两次按键导致死亡

    # 蛇
    snake = init_snake()
    # 墙
    wall = init_wall(5)
    # 食物 food_list
    food = create_food(snake,wall)
    food_style = get_food_style()
    # 方向 第一个坐标表示x+1
    pos = (1, 0)

    game_over = True
    start = False       # 是否开始，当start = True，game_over = True 时，才显示 GAME OVER
    score = 0           # 得分
    ori_speed = 0.25   # 原始速度
    speed = ori_speed
    last_move_time = None
    pause = False       # 暂停


    while True:
        for event in pygame.event.get():
            # 按照while循环的时间频率进行读取的event操作，目的是只想有一个操作
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        start = True
                        game_over = False
                        error_flag = True
                        snake = init_snake()
                        food = create_food(snake,wall)
                        food_style = get_food_style()
                        pos = (1, 0)
                        # 得分
                        score = 0
                        last_move_time = time.time()
                elif event.key == K_SPACE:
                    if not game_over:
                        pause = not pause
                elif event.key in (K_w, K_UP):
                    # 这个判断是为了防止蛇向下移时按了向上键，导致直接 GAME OVER
                    if error_flag and not pos[1]:
                        pos = (0, -1)
                        error_flag = False
                elif event.key in (K_s, K_DOWN):
                    if error_flag and not pos[1]:
                        pos = (0, 1)
                        error_flag = False
                elif event.key in (K_a, K_LEFT):
                    if error_flag and not pos[0]:
                        pos = (-1, 0)
                        error_flag = False
                elif event.key in (K_d, K_RIGHT):
                    if error_flag and not pos[0]:
                        pos = (1, 0)
                        error_flag = False

        draw_line(screen)
        # 判断运动
        if not game_over:
            curTime = time.time()
            if curTime - last_move_time > speed:
                if not pause:
                    error_flag = True
                    last_move_time = curTime
                    next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])
                    # 吃到了食物
                    if next_s in food:
                        snake.appendleft(next_s)
                        index = food.index(next_s)
                        score += food_style[index][0]
                        speed = ori_speed - 0.03 * (score // 100)
                        food.pop(index)
                        food_style.pop(index)
                        if not food:
                            food = create_food(snake,wall)
                            food_style = get_food_style()
                    else:
                        if SCOPE_X[0] <= next_s[0] <= SCOPE_X[1] and SCOPE_Y[0] <= next_s[1] <= SCOPE_Y[1] \
                                and next_s not in snake and next_s not in wall:
                            snake.appendleft(next_s)
                            snake.pop()
                        else:
                            game_over = True

        # 画食物（更新）
        if not game_over:
            # 避免 GAME OVER 的时候把 GAME OVER 的字给遮住了
            for f,fs in zip(food,food_style):
                pygame.draw.rect(screen, fs[1], (f[0] * SIZE, f[1] * SIZE, SIZE, SIZE), 0)

        # 画蛇（更新蛇位置）
        for s in snake:
            # snake就是一个保存了地址的双向栈
            pygame.draw.rect(screen, SNAKE_COLOR, (s[0] * SIZE + LINE_WIDTH, s[1] * SIZE + LINE_WIDTH,
                                                   SIZE - LINE_WIDTH * 2, SIZE - LINE_WIDTH * 2), 0)
        for w in wall:
            # snake就是一个保存了地址的双向栈
            pygame.draw.rect(screen, WALL_COLOR, (w[0] * SIZE + LINE_WIDTH, w[1] * SIZE + LINE_WIDTH,
                                                  SIZE - LINE_WIDTH * 2, SIZE - LINE_WIDTH * 2), 0)

        print_text(screen, font1, 30, 7, f'速度: {score//100}')
        # 用分数确定速度
        print_text(screen, font1, 450, 7, f'得分: {score}')

        if game_over:
            if start:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2, 'GAME OVER', RED)
                # 正中间
        # 只要没有重新开始，就一直刷新game over
        pygame.display.update()


if __name__ == '__main__':
     main()


