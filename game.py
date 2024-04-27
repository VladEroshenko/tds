import pygame as pg
import random
import settings as st
from screen_init import screen
from particles import Field
from characters import Hero, Enemy
from item import AmmoBox
from weapon import Pistol, Shotgun, Ulta, Mine
import time
from spawner import Spawner
from threading import Timer
from bar import Bar


hero = Hero(100, 100)
field = Field(1, 10, 1000)
enemies = [
    Enemy(x=random.randint(10, st.MAP_WIDTH - 10), y=random.randint(10, st.MAP_HEIGHT - 10),
          hp=25, speed=0.6, size=(10, 10), color=st.RED, view_range=2000),
    Enemy(x=random.randint(10, st.MAP_WIDTH - 10), y=random.randint(10, st.MAP_HEIGHT - 10),
          hp=25, speed=0.6, size=(10, 10), color=st.RED, view_range=2000),
    Enemy(x=random.randint(10, st.MAP_WIDTH - 10), y=random.randint(10, st.MAP_HEIGHT - 10),
          hp=25, speed=0.6, size=(10, 10), color=st.RED, view_range=2000)
]
bullets = []
weapons = [
    Pistol(x=hero.x, y=hero.y, color=(0, 0, 0), name='pistol', image_name='images/pistol1.png'),
    Shotgun(x=200, y=200, color=(0, 0, 0), name='shotgun', image_name='images/shotgun1.png')]
ammoboxes = []
available_ammo_boxes = ['pistol', 'shotgun']
spawner = Spawner()
bar = Bar(x=60, y=80, size=(150, 15), color=st.RED, percent=0)
ulta = Ulta(damage=25, distance=100, color=[0, 0, 255])
mines = []


running = True
clock = pg.time.Clock()
font = pg.font.SysFont('impact', 24)
available_fonts = pg.font.get_fonts()
flag = True


while running:
    screen.fill(st.BLACK)
    field.draw()
    hero.make_hit_pause()
    keys = pg.key.get_pressed()
    if hero.health_check():
        hero.draw()
        if keys[pg.K_a]:
            hero.move('left')
        if keys[pg.K_d]:
            hero.move('right')
        if keys[pg.K_w]:
            hero.move('up')
        if keys[pg.K_s]:
            hero.move('down')
    else:
        img = font.render('You lose!', True, (255, 0, 0))
        screen.blit(img, (1140, 600))
        hero.hp = 0
    if keys[pg.K_1]:
        hero.current_weapon = 0
    if keys[pg.K_2]:
        hero.current_weapon = 1
    bar.draw()
    weapons[hero.current_weapon].draw()
    weapons[hero.current_weapon].move_to(hero)
    img = font.render(f'HP: {hero.hp}', True, (255, 0, 0))
    screen.blit(img, (10, 50))
    img = font.render(f'Weapon: {weapons[hero.current_weapon].name}', True, (255, 0, 0))
    screen.blit(img, (10, 10))
    img = font.render('Ulta:', True, bar.color)
    screen.blit(img, (10, 70))
    img = font.render(
        f'Cartridges: {weapons[hero.current_weapon].current_cartridges_in_magazine}/{weapons[hero.current_weapon].cartridges:<1}',
        True,
        (255,
         0,
         0))
    screen.blit(img, (10, 30))
    if len(enemies) == 0 and flag:
        flag = False
        t = Timer(10.0, spawner.start_wave, [enemies])
        t.start()
        # t.join()
        # enemies = spawner.start_wave()
    elif len(enemies) > 0:
        flag = True
    if keys[pg.K_e] and bar.percent == 100:
        indexes = ulta(hero, enemies)
        for i in indexes[::-1]:
            enemies.pop(i)
        bar.percent = 0
        pg.draw.circle(screen, (0, 0, 255), (hero.x, hero.y), 100, 5)
    for enemy in enemies:
        enemy.draw()
        enemy.move_to(hero)
        if enemy.check_collision_with_hero(hero) and hero.hit_pause >= 100:
            hero.hp -= 1
            hero.hit_pause = 0
        for bullet in bullets:
            if enemy.check_collision_with_bullet(bullet):
                enemy.hp = max(enemy.hp - bullet.damage, 0)
                enemy.color = (max(enemy.color[0] - 10, 0), min(enemy.color[1] + 10, 250), 0)
                bar.add(1)
    for i in range(len(enemies) - 1, -1, -1):
        if enemies[i].hp <= 0:
            if random.randrange(0, 100) < st.AMMO_BOX_DROP_PROB:
                box_type = random.choices(available_ammo_boxes, weights=(1, 1), k=1)[0]
                ammoboxes.append(AmmoBox(
                        x=enemies[i].x,
                        y=enemies[i].y,
                        size=(15, 15),
                        color=(0, 0, 0),
                        image_name=f'images/ammobox_{box_type}.png',
                        ammo_type=box_type,
                        volume=weapons[available_ammo_boxes.index(box_type)].magazine_volume * st.AMMO_BOX_SIZE))
            enemies.pop(i)
    for i in range(len(ammoboxes) - 1, -1, -1):
        ammoboxes[i].draw()
        if ammoboxes[i].check_collision_with_hero(hero):
            weapons[available_ammo_boxes.index(ammoboxes[i].ammo_type)].cartridges += ammoboxes[i].volume
            ammoboxes.pop(i)
    if pg.mouse.get_pressed()[0] and hero.health_check():
        mouse_pos = pg.mouse.get_pos()
        for ind, weapon in enumerate(weapons):
            if hero.current_weapon == ind and weapon.check_cooldown(
                    time.time()) and weapon.current_cartridges_in_magazine > 0 and weapon.check_reload():
                bullets.extend(weapon.shoot(mouse_pos))
                weapon.last_shot_time = time.time()
                weapon.current_cartridges_in_magazine -= 1
    for weapon in weapons:
        if weapon.cartridges > 0:
            if (keys[pg.K_r] and weapon.check_reload() and weapon.current_cartridges_in_magazine < weapon.magazine_volume) or weapon.current_cartridges_in_magazine == 0:
                weapon.reload()
                weapon.start_reload_time = time.time()
    for bullet in bullets:
        bullet.draw()
        bullet.move()
    if keys[pg.K_f] and hero.is_ready_to_tp():
        window_width, window_height = screen.get_size()
        hero.tp(random.randint(0, window_width), random.randint(0, window_height))
        hero.reset_cooldown()
    for i in range(len(mines) - 1, -1, -1):
        mines[i].activation(enemies)
        if mines[i].activated:
            mines[i].boom(enemies)
            mines.pop(i)
        else:
            mines[i].draw()
    for event in pg.event.get():
        if event.type == pg.KEYDOWN and hero.health_check():
            if event.key == pg.K_p:
                mines.append(
                    Mine(x=hero.x, y=hero.y, size=(10, 10), image_name='images/mina.png', damage=25, damage_radius=50,
                         activation_radius=10))
        if event.type == pg.MOUSEWHEEL and hero.health_check():
            hero.current_weapon -= event.y
            if hero.current_weapon >= len(weapons):
                hero.current_weapon = 0
            if hero.current_weapon < 0:
                hero.current_weapon = len(weapons) - 1
        if event.type == pg.QUIT:
            running = False
    hero.warm_up()
    pg.display.flip()
    clock.tick(st.FPS)
pg.quit()
