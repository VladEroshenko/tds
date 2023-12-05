from item import Item, Bullet
import time
from characters import Hero
from math import sqrt, asin, degrees, radians, sin, cos
import random


class Weapon(Item):
    def __init__(self, x, y, size, color, name, damage, reload_speed, cooldown, magazine_volume, cartridges,
                 bullets_spread, image_name, bullet_speed):
        super().__init__(x, y, size, color, image_name)
        self.name = name
        self.damage = damage
        self.reload_speed = reload_speed
        self.cooldown = cooldown
        self.magazine_volume = magazine_volume
        self.cartridges = cartridges
        self.bullets_spread = bullets_spread
        self.bullet_speed = bullet_speed
        self.last_shot_time = time.time()
        self.current_cartridges_in_magazine = magazine_volume
        self.start_reload_time = time.time()

    def check_cooldown(self, shot_time):
        return shot_time - self.last_shot_time >= self.cooldown

    def reload(self):
        tmp_cartridges = self.cartridges
        self.cartridges -= min(self.magazine_volume - self.current_cartridges_in_magazine, self.cartridges)
        self.current_cartridges_in_magazine += min(self.magazine_volume - self.current_cartridges_in_magazine, tmp_cartridges)

    def check_reload(self):
        return time.time() - self.start_reload_time >= self.reload_speed

    def move_to(self, hero: Hero):
        self.x = hero.x
        self.y = hero.y


class Pistol(Weapon):
    def __init__(self, x, y, color, name, image_name):
        super().__init__(x=x, y=y, size=(20, 20), color=color, name=name, damage=1, reload_speed=1.5, cooldown=0.2,
                         magazine_volume=12, cartridges=24, bullets_spread=3, image_name=image_name, bullet_speed=10)

    def shoot(self, click: tuple):
        x_0 = click[0] - self.x
        y_0 = click[1] - self.y
        distance = sqrt(x_0 ** 2 + y_0 ** 2)
        sin_beta = y_0 / distance
        rad_beta = asin(sin_beta)
        beta = degrees(rad_beta)
        new_beta = random.uniform(beta - self.bullets_spread, beta + self.bullets_spread)
        new_beta_in_rads = radians(new_beta)
        if x_0 > 0:
            new_xys = [cos(new_beta_in_rads), sin(new_beta_in_rads)]
            angle = 360 - new_beta - 90
        else:
            new_xys = [-cos(new_beta_in_rads), sin(new_beta_in_rads)]
            angle = 360 + new_beta + 90
        new_xys[0] += self.x
        new_xys[1] += self.y
        return [Bullet(x=self.x, y=self.y, size=(10, 10), color=(0, 0, 0), image_name='images/bullet.png',
                    speed=self.bullet_speed, damage=self.damage, x_click=new_xys[0], y_click=new_xys[1], angle=angle)]


class Shotgun(Weapon):
    def __init__(self, x, y, color, name, image_name):
        super().__init__(x=x, y=y, size=(20, 20), color=color, name=name, damage=2, reload_speed=5, cooldown=1,
                         magazine_volume=7, cartridges=14, bullets_spread=5, image_name=image_name, bullet_speed=5)

    def shoot(self, click: tuple):
        x_0 = click[0] - self.x
        y_0 = click[1] - self.y
        distance = sqrt(x_0 ** 2 + y_0 ** 2)
        sin_beta = y_0 / distance
        rad_beta = asin(sin_beta)
        beta = degrees(rad_beta)
        new_betas = [radians(random.uniform(beta - self.bullets_spread, beta + self.bullets_spread)),
                     radians(random.uniform(beta - self.bullets_spread, beta + self.bullets_spread)),
                     radians(random.uniform(beta - self.bullets_spread, beta + self.bullets_spread))]
        if x_0 > 0:
            new_xys = [[cos(new_betas[0]), sin(new_betas[0])],
                       [cos(new_betas[1]), sin(new_betas[1])],
                       [cos(new_betas[2]), sin(new_betas[2])]]
            angle1 = 360 - degrees(new_betas[0]) - 90
            angle2 = 360 - degrees(new_betas[1]) - 90
            angle3 = 360 - degrees(new_betas[2]) - 90
        else:
            new_xys = [[-cos(new_betas[0]), sin(new_betas[0])],
                       [-cos(new_betas[1]), sin(new_betas[1])],
                       [-cos(new_betas[2]), sin(new_betas[2])]]
            angle1 = 360 + degrees(new_betas[0]) - 90
            angle2 = 360 + degrees(new_betas[1]) - 90
            angle3 = 360 + degrees(new_betas[2]) - 90
        new_xys[0][0] += self.x
        new_xys[0][1] += self.y
        new_xys[1][0] += self.x
        new_xys[1][1] += self.y
        new_xys[2][0] += self.x
        new_xys[2][1] += self.y
        return [Bullet(x=self.x, y=self.y, size=(10, 10), color=(0, 0, 0), image_name='images/bullet.png',
                       speed=self.bullet_speed, damage=self.damage, x_click=new_xys[0][0], y_click=new_xys[0][1], angle=angle1),
                Bullet(x=self.x, y=self.y, size=(10, 10), color=(0, 0, 0), image_name='images/bullet.png',
                       speed=self.bullet_speed, damage=self.damage, x_click=new_xys[1][0], y_click=new_xys[1][1], angle=angle2),
                Bullet(x=self.x, y=self.y, size=(10, 10), color=(0, 0, 0), image_name='images/bullet.png',
                       speed=self.bullet_speed, damage=self.damage, x_click=new_xys[2][0], y_click=new_xys[2][1], angle=angle3)]