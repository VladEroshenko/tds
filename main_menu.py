import pygame as pg
from screen_init import screen
import settings as st
from button import Button


font = pg.font.SysFont(st.TEXT, 24)
clock = pg.time.Clock()
x, y = 0, 0
running = True
buttons = [Button(x=1140, y=700, size=(200, 100), color=st.ORANGE, text='абоба', text_size=24, text_color=st.BLACK),
           Button(x=1140, y=400, size=(200, 100), color=st.ORANGE, text='Start', text_size=24, text_color=st.BLACK)]

while running:
    screen.fill((0, 0, 0))
    for button in buttons:
        button.draw()
        if button.collide_with((x, y)):
            button.change_text_color(st.WHITE)
        else:
            button.change_text_color(st.BLACK)
    for event in pg.event.get():
        if event.type == pg.MOUSEMOTION:
            x, y = event.pos
        if event.type == pg.QUIT:
            running = False
    pg.display.flip()
    clock.tick(60)
pg.quit()