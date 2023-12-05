from screen_init import screen
from math import sqrt
import pygame as pg
from typing import Tuple, List
from characters import Character, Hero


class Item:
    def __init__(self, x: float, y: float, size: Tuple[int, int], color: Tuple[int, int, int], image_name: str):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.image = pg.image.load(image_name)
        self.image = pg.transform.scale(self.image, self.size)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_distance(self, another_obj: Hero) -> float:
        return sqrt((self.x + self.size[0] / 2 - another_obj.x + another_obj.size[0] / 2) ** 2 + (
                    self.y + self.size[1] / 2 - another_obj.y + another_obj.size[1] / 2) ** 2)


class Bullet(Item):
    def __init__(self, x: float, y: float, size: Tuple[int, int], color: Tuple[int, int, int], image_name: str, speed: int, damage: int, x_click: float, y_click: float, angle: float):
        super().__init__(x, y, size, color, image_name)
        self.speed = speed
        self.damage = damage
        self.angle = angle
        diff_x = x_click - x
        diff_y = y_click - y
        hypot = sqrt(diff_x**2 + diff_y**2)
        diff_x /= hypot
        diff_y /= hypot
        self.x_speed = diff_x * speed
        self.y_speed = diff_y * speed
        self.image = pg.transform.rotate(self.image, self.angle)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed


class AmmoBox(Item):
    def __init__(self, x: float, y: float, size: Tuple[int, int], color: Tuple[int, int, int], image_name: str, ammo_type: str, volume: int):
        super().__init__(x, y, size, color, image_name)
        self.ammo_type = ammo_type
        self.volume = volume

    def get_distance(self, another_obj):
        return sqrt((self.x + self.size[0] / 2 - another_obj.x + another_obj.size[0] / 2) ** 2 + (self.y + self.size[1] / 2 - another_obj.y + another_obj.size[1] / 2) ** 2)

    def check_collision_with_hero(self, another_obj: Hero):
        hypot1 = sqrt(self.size[0] ** 2 + self.size[1] ** 2)
        hypot2 = sqrt(another_obj.size[0] ** 2 + another_obj.size[1] ** 2)
        return self.get_distance(another_obj) < (hypot1 + hypot2) / 2