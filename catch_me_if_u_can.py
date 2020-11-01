import pygame
import math
from pygame.draw import *
from random import randint, choice, random

pygame.init()

FPS = 30
# время игры
time = 15
# параметры экрана
height = 900
width = 1200
screen = pygame.display.set_mode((width, height))

# цвета фигур
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Ball:
    def __init__(self):
        self.x = randint(150, 1050)
        self.y = randint(150, 750)
        self.r = randint(20, 100)
        self.color = choice(COLORS)
        self.velocity = randint(90, 150)
        self.angle = 2 * math.pi * random()
        self.velocity_x = self.velocity * math.cos(self.angle)
        self.velocity_y = self.velocity * math.sin(self.angle)

    def draw(self):
        '''
        рисует цель
        '''
        circle(screen, self.color, (int(self.x), int(self.y)), self.r)

    def ball_distruct(self):
        '''
        закрашивает цель
        '''
        circle(screen, BLACK, (int(self.x), int(self.y)), self.r)

    def move(self):
        '''
        двигает цель
        '''
        if self.x - self.r <= 0:
            self.velocity_x = -self.velocity_x
        elif self.x + self.r >= width:
            self.velocity_x = -self.velocity_x
        if self.y - self.r <= 0:
            self.velocity_y = -self.velocity_y
        elif self.y + self.r >= height:
            self.velocity_y = -self.velocity_y
        self.x += self.velocity_x / FPS
        self.y += self.velocity_y / FPS


class Square:
    def __init__(self):
        self.x = randint(201, 999)
        self.y = randint(201, 699)
        self.width = randint(75, 200)
        self.height = randint(75, 200)
        self.color = choice(COLORS)
        self.velocity = randint(90, 150)
        self.angle = 2 * math.pi * random()
        self.velocity_x = self.velocity * math.cos(self.angle)
        self.velocity_y = self.velocity * math.sin(self.angle)

    def draw(self):
        '''
        рисует цель
        '''
        rect(screen, self.color, (int(self.x), int(self.y), self.width, self.height))

    def square_distruct(self):
        '''
        закрашивает цель
        '''
        rect(screen, BLACK, (int(self.x), int(self.y), self.width, self.height))

    def move(self):
        '''
        двигает цель
        '''
        if self.x <= 0:
            self.velocity_x = -self.velocity_x
        elif self.x + self.width >= width:
            self.velocity_x = -self.velocity_x
        if self.y <= 0:
            self.velocity_y = -self.velocity_y
        elif self.y + self.height >= height:
            self.velocity_y = -self.velocity_y
        self.x += self.velocity_x / FPS
        self.y += self.velocity_y / FPS


def is_click_square(x, y, square_width, square_height):
    '''
    проверка попали ли мы в квадрат
    :param x: расстояние от левого верхнего угла до точки нажатия по х
    :param y: расстояние от левого верхнего угла до точки нажатия по у
    :param square_width: ширина квадрата
    :param square_height: высота квадрата
    :return: True - если попал, иначе - False
    '''
    if (x <= square_width) and (y <= square_height) and (x >= 0) and (y >= 0):
        return True
    else:
        return False


def is_click_ball(x, y, r):
    '''
    проверка попали ли мы в квадрат
    :param x: расстояние от центра круга до точки нажатия по х
    :param y: расстояние от центра круга до точки нажатия по у
    :param r: радиус круга
    :return: True - если попал, иначе - False
    '''
    if x ** 2 + y ** 2 <= r ** 2:
        return True
    else:
        return False


# имя игрока
name = input()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

pygame.font.init()
score = 0  # point counter
balls = []  # array of balls
squares = []  # array of squares
for i in range(5):
    if random() <= 0.5:
        ball = Ball()
        ball.draw()
        balls.append(ball)
    else:
        square = Square()
        square.draw()
        squares.append(square)
# время от начала игры
seconds = 0

while not finished:
    clock.tick(FPS)
    seconds += 1
    rect(screen, BLACK, (1100, 0, 100, 100))
    labelFont = pygame.font.SysFont('Monaco', 100)
    surface_counter = labelFont.render(str(score), False, RED)
    screen.blit(surface_counter, (1100, 0))
    if seconds == time * FPS:
        finished = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i in range(len(balls)):
                if is_click_ball(x-balls[i].x, y-balls[i].y, balls[i].r):
                    score += 1
                    balls[i].ball_distruct()
                    balls.pop(i)
                    ball = Ball()
                    ball.draw()
                    balls.append(ball)
            for i in range(len(squares)):
                if is_click_square(x - squares[i].x, y - squares[i].y, squares[i].width, squares[i].height):
                    score += 3
                    squares[i].square_distruct()
                    squares.pop(i)
                    square = Square()
                    square.draw()
                    squares.append(square)
    for ball in balls:
        ball.ball_distruct()
        ball.move()
        ball.draw()
    for square in squares:
        square.square_distruct()
        square.move()
        square.draw()
    pygame.display.update()

# считываем данные таблицы из рейтинга и сортируем вместе с данными игрока
f = open('bools.txt', 'r')
rating = []
for line in f:
    name_old, score_old = line.split(' ')
    score_old = int(score_old)
    rating.append((name_old, score_old))
rating.append((name, score))
f.close()

rating.sort(key=lambda x: x[1], reverse=True)

# выводим отсортированную таблицу в файл
f = open('bools.txt', 'w')
for name, score in rating:
    f.write(str(name) + ' ' + str(score) + '\n')
f.close()

pygame.quit()
