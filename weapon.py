from item import Item, Bullet
from screen_init import screen
import time


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

    # def draw(self):
    #     screen.blit(self.image, (self.x, self.y))


class Pistol(Weapon):
    def __init__(self, x, y, color, name, image_name):
        super().__init__(x=x, y=y, size=(20, 20), color=color, name=name, damage=10, reload_speed=3, cooldown=0.333,
                         magazine_volume=12, cartridges=24, bullets_spread=5, image_name=image_name, bullet_speed=10)

    def shoot(self, click: tuple):
        return [Bullet(x=self.x, y=self.y, size=(10, 10), color=(0, 255, 0), image_name='images/bullet.png',
                    speed=self.bullet_speed, damage=self.damage, x_click=click[0], y_click=click[1])]

    def check_cooldown(self, shot_time):
        return shot_time - self.last_shot_time >= self.cooldown


class Shotgun(Weapon):
    def __init__(self, x, y, color, name, image_name):
        super().__init__(x=x, y=y, size=(20, 20), color=color, name=name, damage=20, reload_speed=5, cooldown=1,
                         magazine_volume=7, cartridges=14, bullets_spread=15, image_name=image_name, bullet_speed=5)