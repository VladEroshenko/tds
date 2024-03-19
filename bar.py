import pygame as pg
from screen_init import screen
import settings as st


class Bar:
    def __init__(self, x, y, size, color, percent):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.percent = percent

    def draw(self):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.size[0], self.size[1]), 2)
        pg.draw.rect(screen, self.color, (self.x, self.y, self.size[0] * (self.percent / 100), self.size[1]))

    def add(self, value):
        self.percent = min(self.percent + value, 100)