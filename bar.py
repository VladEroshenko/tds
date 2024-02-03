import pygame as pg
from screen_init import screen


class Bar:
    def __init__(self, x, y, size, color, percent):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.percent = percent

    def draw(self):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.size[0], self.size[1]), )

    def filling(self):
        pass