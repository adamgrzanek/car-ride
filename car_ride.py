#-*- coding: utf-8 -*-

import pygame
import random
import tkinter as tk
from tkinter import messagebox

window_wide = 300
square = window_wide/10  # 30


pygame.init()
window = pygame.display.set_mode((window_wide, window_wide * 2))



class Car:


    def __init__(self, color=(24, 164, 240)):
        self.color = color
        self.center = window_wide/2                       # 150
        self.position_y = window_wide * 2 - 90            # 510
        self.c_row = int(self.position_y // square)            # 510 / 30 = 17
        #self.c_column = int(self.center // square - 1)         # 150 / 30 = 4 (currently middle column; 4 of 8 (0-8))
        #self.rectangle = (self.center - square / 2, self.position_y, square, square * 2)  # **


    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # zamknij gre po naciśnięciu X
                pygame.quit()

            keys = pygame.key.get_pressed()  # zbiór ze wszystkimi naciśniętymi klawiszami w grze

            if keys[pygame.K_LEFT]:
                if self.center == square:
                    self.center = square
                else:
                    self.center -= square

            elif keys[pygame.K_RIGHT]:
                if self.center == window_wide - square:
                    self.center = window_wide - square
                else:
                    self.center += square

    def draw_car(self):
        window.fill((20, 0, 200))
        #pygame.draw.rect(window, self.color, self.rectangle)  # **
        #pygame.draw.rect(window, self.color, (self.center - square / 2, self.position_y, square, square * 2))
        pygame.draw.rect(window, self.color, (self.center - square / 4, self.position_y, square/2, square * 2))

        # prow of the vehicle (triangle)
        pygame.draw.polygon(window, self.color, points=[(self.center-7.5, self.position_y),
                                                         (self.center, self.position_y-6),
                                                         (self.center+7.5, self.position_y)])
        # wheel
        wheel_color = (100, 10, 50)
        pygame.draw.rect(window, wheel_color, (self.center - 15, self.position_y+3, 6, 15))    # front left
        pygame.draw.rect(window, wheel_color, (self.center + 9, self.position_y+3, 6, 15))     # front right
        pygame.draw.rect(window, wheel_color, (self.center - 15, self.position_y + 37, 6, 15)) # back left
        pygame.draw.rect(window, wheel_color, (self.center + 9, self.position_y + 37, 6, 15))  # back right
        # spoiler
        pygame.draw.rect(window, (255, 255, 0), (self.center - square/2, self.position_y + 57, square, 3))

    def check_collision(self):
        global collision
        collision = False
        for i in obstacles_cubes:
            #if i.column == self.c_column and i.o_row == self.c_row:
            if i.column == int(self.center // square - 1) and i.o_row == self.c_row:
                collision = True
        return collision



    def reset(self):
        message_box('GAME OVER', f'Your result: {result}\nPlay again')
        self.center = window_wide / 2
        self.position_y = window_wide * 2 - 90
        self.c_row = int(self.position_y // square)
        obstacles_square = []
        obstacles_cubes = []


car = Car()


class Track:

    @staticmethod
    def draw_side_limiters(color=(100, 0, 0)):
        pygame.draw.rect(window, color, (0, 0, square/2, window_wide * 2))                       # left
        pygame.draw.rect(window, color, (window_wide-square/2, 0, square/2, window_wide * 2))    # right


    @staticmethod
    def obstacles():  # impediments - przeszkody

        global obstacles_cubes

        column_quantity = window_wide // square - 1  # -1 side delimiters  =9
        obstacles_square = []
        # 9 column -> [True, True, True, True, True, True, False, True, True]   min 1 False

        if obstacle_row == 0:
            while False not in obstacles_square:
                for i in range(int(column_quantity)):
                    obstacles_square.append(random.choice([True, False]))

            obstacles_cubes = []  # **** aftre if statement [Cube(0), Cube(1), .....]
            for number, i in enumerate(obstacles_square):
                # [True, True, True, True, True, True, False, True, True]
                #    0     1     2     3     4     5     6      7     8     i - column number
                if i == True:
                    o_c = ObstacleCube(number)
                    obstacles_cubes.append(o_c)  # ****

        for o in obstacles_cubes:
            o.o_row = obstacle_row
            o.draw_cube(obstacle_row)


class ObstacleCube:

    side_space = square/2

    def __init__(self, column, o_row=0):
        self.column = column
        self.o_row = o_row

    def draw_cube(self, row):
        pygame.draw.rect(window, (0, 0, 0), (self.side_space + self.column * square, row * square, square, square))



def message_box(subject, content):
    root = tk.Tk()
    # root.attributes("-topmost", 1)
    root.withdraw()
    messagebox.showinfo(subject, content)

    try:
        root.destroy()
    except:
        pass



track = Track()
clock = pygame.time.Clock()
t = 10
obstacle_row = 0
result = 0
run = True


while run:

    car.move()
    car.draw_car()
    track.draw_side_limiters()

    track.obstacles()
    if car.check_collision():
        car.reset()
        result = -1
        t = 10

    clock.tick(t)

    pygame.display.update()
    obstacle_row += 1
    if obstacle_row > 20:
        obstacle_row = 0
        result += 1
        if result >= 5 and result % 5 == 0:
            t += 2



