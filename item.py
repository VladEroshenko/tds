from screen_init import screen
from math import sqrt
import pygame as pg


class Item:
    def __init__(self, x, y, size, color, image_name):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.image = pg.image.load(image_name)
        self.image = pg.transform.scale(self.image, self.size)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Bullet(Item):
    def __init__(self, x, y, size, color, image_name, speed, damage, x_click, y_click):
        super().__init__(x, y, size, color, image_name)
        self.speed = speed
        self.damage = damage
        diff_x = x_click - x
        diff_y = y_click - y
        hypot = sqrt(diff_x**2 + diff_y**2)
        diff_x /= hypot
        diff_y /= hypot
        self.x_speed = diff_x * speed
        self.y_speed = diff_y * speed

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed