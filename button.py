import pygame as pg
from screen_init import screen
import settings as st
from typing import Tuple


class Button:
    def __init__(self, x, y, size, color, text, text_size, text_color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        # self.rect = pg.draw.rect(screen, self.color, (self.x, self.y, self.size[0], self.size[1]), 0)
        self.font = pg.font.SysFont(st.TEXT, 24)

    def draw(self):
        text = self.font.render(self.text, True, self.text_color)
        self.rect = pg.draw.rect(screen, self.color, (self.x, self.y, self.size[0], self.size[1]), 0)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def collide_with(self, mouse_coords):
        return self.rect.collidepoint(mouse_coords[0], mouse_coords[1])

    def change_text_color(self, new_color: Tuple[int, int, int]):
        self.text_color = new_color