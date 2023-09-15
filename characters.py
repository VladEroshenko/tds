import settings as st
from screen_init import screen
from math import sqrt
import pygame as pg


class Character:
    def __init__(self, x, y, hp, speed, size, color):
        self.x = x
        self.y = y
        self.hp = hp
        self.speed = speed
        self.size = size
        self.color = color

    def draw(self):
        pass


class Hero(Character):
    def __init__(self, x, y, hp=10, speed=1, size=10, color=st.WHITE, cooldown=100, max_cooldown=100, hit_pause=100, max_hit_pause=100, current_weapon=1):
        super().__init__(x, y, hp, speed, size, color)
        self.cooldown = cooldown
        self.max_cooldown = max_cooldown
        self.hit_pause = hit_pause
        self.max_hit_pause = max_hit_pause
        self.current_weapon = current_weapon


    def draw(self):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def tp(self, x, y):
        self.x = x
        self.y = y

    def is_ready_to_tp(self):
        return self.cooldown >= self.max_cooldown

    def reset_cooldown(self):
        self.cooldown = 0

    def warm_up(self):
        self.cooldown += 1

    def health_check(self):
        return self.hp > 0

    def make_hit_pause(self):
        if self.hit_pause > self.max_hit_pause:
            self.hit_pause = self.max_hit_pause
        self.hit_pause += 1


class Enemy(Character):
    def __init__(self, x, y, hp, speed, size, color, view_range):
        super().__init__(x, y, hp, speed, size, color)
        self.view_range = view_range

    def draw(self):
        pg.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def get_distance(self, another_obj: Hero):
        return sqrt((self.x + self.size / 2 - another_obj.x + another_obj.size / 2) ** 2 + (self.y + self.size / 2 - another_obj.y + another_obj.size / 2) ** 2)

    def move_to(self, another_obj: Hero):
        a = another_obj.x - self.x
        b = another_obj.y - self.y
        c = self.get_distance(another_obj)
        diff_x = a / c
        diff_y = b / c
        if c <= self.view_range:
            self.x += diff_x * self.speed
            self.y += diff_y * self.speed

    def check_collision_with_hero(self, another_obj: Hero):
        return self.get_distance(another_obj) < (self.size + another_obj.size) * sqrt(2) / 2

    def check_collision_with_bullet(self, another_obj):
        return self.get_distance(another_obj) < (self.size + another_obj.size) * sqrt(2) / 2