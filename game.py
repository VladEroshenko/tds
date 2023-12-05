import pygame as pg
import random
import settings as st
from screen_init import screen
from particles import Field
from characters import Hero, Enemy
from item import AmmoBox
from weapon import Pistol, Shotgun
import time


hero = Hero(100, 100)
field = Field(1, 10, 1000)
enemies = [
    Enemy(x=random.randint(10, st.MAP_WIDTH-10), y=random.randint(10, st.MAP_HEIGHT-10), hp=25, speed=0.5, size=(10, 10), color=st.RED, view_range=2000),
    Enemy(x=random.randint(10, st.MAP_WIDTH-10), y=random.randint(10, st.MAP_HEIGHT-10), hp=25, speed=0.5, size=(10, 10), color=st.RED, view_range=2000),
    Enemy(x=random.randint(10, st.MAP_WIDTH-10), y=random.randint(10, st.MAP_HEIGHT-10), hp=25, speed=0.5, size=(10, 10), color=st.RED, view_range=2000)
]
bullets = []
weapons = [
    Pistol(x=hero.x, y=hero.y, color=(0, 0, 0), name='pistol', image_name='images/pistol1.png'),
    Shotgun(x=200, y=200, color=(0, 0, 0), name='shotgun', image_name='images/shotgun1.png')]
ammoboxes = [AmmoBox(x=random.randint(10, st.MAP_WIDTH-10), y=random.randint(10, st.MAP_HEIGHT-10), size=(15, 15), color=(0, 0, 0), image_name='images/ammobox_pistol.png', ammo_type='pistol', volume=weapons[0].magazine_volume * st.AMMO_BOX_SIZE),
             AmmoBox(x=random.randint(10, st.MAP_WIDTH-10), y=random.randint(10, st.MAP_HEIGHT-10), size=(15, 15), color=(0, 0, 0), image_name='images/ammobox_shotgun.png', ammo_type='shotgun', volume=weapons[1].magazine_volume * st.AMMO_BOX_SIZE)]


running = True
clock = pg.time.Clock()
font = pg.font.SysFont('impact', 24)
available_fonts = pg.font.get_fonts()
while running:
    screen.fill(st.BLACK)
    field.draw()
    hero.make_hit_pause()
    keys = pg.key.get_pressed()
    if hero.health_check():
        hero.draw()
    if keys[pg.K_1]:
        hero.current_weapon = 0
    if keys[pg.K_2]:
        hero.current_weapon = 1
    weapons[hero.current_weapon].draw()
    weapons[hero.current_weapon].move_to(hero)
    img = font.render(f'HP: {hero.hp}', True, (255, 0, 0))
    screen.blit(img, (10, 50))
    img = font.render(f'Weapon: {weapons[hero.current_weapon].name}', True, (255, 0, 0))
    screen.blit(img, (10, 10))
    img = font.render(f'Cartridges: {weapons[hero.current_weapon].current_cartridges_in_magazine}/{weapons[hero.current_weapon].cartridges:<1}', True, (255, 0, 0))
    screen.blit(img, (10, 30))
    for enemy in enemies:
        enemy.draw()
        enemy.move_to(hero)
        if enemy.check_collision_with_hero(hero) and hero.hit_pause >= 100:
            hero.hp -= 1
            hero.hit_pause = 0
            #баг когда чел заходит в героя не отнимается хп.
        for bullet in bullets:
            if enemy.check_collision_with_bullet(bullet):
                enemy.hp = max(enemy.hp - bullet.damage, 0)
                enemy.color = (enemy.color[0] - 10, enemy.color[1] + 10, 0)
    for i in range(len(enemies)-1, -1, -1):
        if enemies[i].hp <= 0:
            enemies.pop(i)
    for i in range(len(ammoboxes)-1, -1, -1):
        ammoboxes[i].draw()
        if ammoboxes[i].check_collision_with_hero(hero):
            weapons[i].cartridges += ammoboxes[i].volume
            ammoboxes.pop(i)
    if pg.mouse.get_pressed()[0]:
        mouse_pos = pg.mouse.get_pos()
        if hero.current_weapon == 0 and weapons[0].check_cooldown(time.time()) and weapons[0].current_cartridges_in_magazine > 0 and weapons[0].check_reload():
            bullets.extend(weapons[0].shoot(mouse_pos))
            weapons[0].last_shot_time = time.time()
            weapons[0].current_cartridges_in_magazine -= 1
        if hero.current_weapon == 1 and weapons[1].check_cooldown(time.time()) and weapons[1].current_cartridges_in_magazine > 0 and weapons[1].check_reload():
            bullets.extend(weapons[1].shoot(mouse_pos))
            weapons[1].last_shot_time = time.time()
            weapons[1].current_cartridges_in_magazine -= 1
    if weapons[0].cartridges > 0:
        if keys[pg.K_r]:
            weapons[0].reload()
            weapons[0].start_reload_time = time.time()
        if weapons[0].current_cartridges_in_magazine == 0:
            weapons[0].reload()
            weapons[0].start_reload_time = time.time()
    if weapons[1].cartridges > 0:
        if keys[pg.K_r]:
            weapons[1].reload()
            weapons[1].start_reload_time = time.time()
        if weapons[1].current_cartridges_in_magazine == 0:
            weapons[1].reload()
            weapons[1].start_reload_time = time.time()
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
        if event.type == pg.MOUSEWHEEL:
            hero.current_weapon -= event.y
        if event.type == pg.QUIT:
            running = False
    hero.warm_up()
    pg.display.flip()
    clock.tick(st.FPS)
pg.quit()