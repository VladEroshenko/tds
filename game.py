import pygame as pg
import random
import settings as st
from screen_init import screen
from particles import Particle, Field
from characters import Hero, Enemy
from item import Bullet
from weapon import Pistol, Shotgun
import time


hero = Hero(100, 100)
field = Field(1, 10, 1000)
enemies = [
    Enemy(x=random.randint(10, st.MAP_WIDTH-10), y=random.randint(10, st.MAP_HEIGHT-10), hp=10, speed=0.5, size=10, color=st.RED, view_range=150),
    Enemy(x=random.randint(10, st.MAP_WIDTH-10), y=random.randint(10, st.MAP_HEIGHT-10), hp=10, speed=0.5, size=10, color=st.RED, view_range=150),
    Enemy(x=random.randint(10, st.MAP_WIDTH-10), y=random.randint(10, st.MAP_HEIGHT-10), hp=10, speed=0.5, size=10, color=st.RED, view_range=150)
]
bullets = []
weapons = [
    Pistol(x=200, y=200, color=(0, 0, 0), name='pistol', image_name='images/pistol1.png'),
    Shotgun(x=200, y=200, color=(0, 0, 0), name='shotgun', image_name='images/shotgun.png')]


running = True
clock = pg.time.Clock()
print(enemies[0].x, enemies[0].y, enemies[1].x, enemies[1].y, enemies[2].x, enemies[2].y)
font = pg.font.SysFont(None, 24)
while running:
    screen.fill(st.BLACK)
    field.draw()
    hero.make_hit_pause()
    keys = pg.key.get_pressed()
    if hero.health_check():
        hero.draw()
    if keys[pg.K_1]:
        hero.current_weapon = 1
    if keys[pg.K_2]:
        hero.current_weapon = 2
    weapons[hero.current_weapon-1].draw()
    img = font.render(f'Weapon: {weapons[hero.current_weapon-1].name}', True, (255, 0, 0))
    screen.blit(img, (10, 10))
    img = font.render(f'HP: {hero.hp}', True, (255, 0, 0))
    screen.blit(img, (10, 50))
    for enemy in enemies:
        enemy.draw()
        enemy.move_to(hero)
        if enemy.check_collision_with_hero(hero) and hero.hit_pause >= 100:
            hero.hp -= 1
            hero.hit_pause = 0
            #баг когда чел заходит в героя не отнимается хп
    if pg.mouse.get_pressed()[0]:
        mouse_pos = pg.mouse.get_pos()
        if hero.current_weapon == 1 and weapons[0].check_cooldown(time.time()):
            bullets.extend(weapons[0].shoot(mouse_pos))
        if hero.current_weapon == 2:
            bullets.append(Bullet(x=hero.x, y=hero.y, size=(10, 10), color=(0, 255, 0), image_name='images/bullet.png',
                    speed=weapons[1].bullet_speed, damage=weapons[1].damage, x_click=mouse_pos[0], y_click=mouse_pos[1]))
    for bullet in bullets:
        bullet.draw()
        bullet.move()
    if keys[pg.K_e] and hero.is_ready_to_tp():
        window_width, window_height = screen.get_size()
        hero.tp(random.randint(0, window_width), random.randint(0, window_height))
        hero.reset_cooldown()
    if keys[pg.K_a]:
        hero.x -= hero.speed
    if keys[pg.K_d]:
        hero.x += hero.speed
    if keys[pg.K_w]:
        hero.y -= hero.speed
    if keys[pg.K_s]:
        hero.y += hero.speed
    for event in pg.event.get():
        # if event.type == pg.KEYDOWN:
        #     print(f'Клавиша {event.key}, {pg.key.name(event.key)} нажата')
        #     if event.key == pg.K_q:
        #         print('Клавиша q нажата')
        if event.type == pg.QUIT:
            running = False
    hero.warm_up()
    pg.display.flip()
    clock.tick(st.FPS)
pg.quit()