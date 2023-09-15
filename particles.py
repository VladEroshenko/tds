import pygame as pg
import random
import settings as st
from screen_init import screen


class Particle:
    def __init__(self, x, y, size=5, color=st.WHITE):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def draw(self):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.size)


class Field:
    def __init__(self, min_size, max_size, quantity):
        self.field = [
            Particle(
                random.randint(0, st.MAP_WIDTH),
                random.randint(0, st.MAP_HEIGHT),
                random.randint(min_size, max_size),
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            ) for i in range(quantity)
        ]

    def draw(self):
        for particle in self.field:
            particle.draw()