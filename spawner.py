import pygame as pg
import time
import settings as st
from characters import Enemy, FastEnemy, SlowEnemy
from typing import List
import random
from threading import Timer


class Spawner:
    def __init__(self):
        self.wave = 0


    def start_wave(self, enemies_list) -> None:
        # print('start_wave')
        self.wave += 1
        enemies_list[:] = [Enemy(x=random.randint(10, st.MAP_WIDTH - 10), y=random.randint(10, st.MAP_HEIGHT - 10), hp=25, speed=0.6, size=(10, 10), color=st.RED, view_range=2000) for i in range(self.wave * 5)]
        enemies_list.extend([FastEnemy(x=random.randint(10, st.MAP_WIDTH - 10), y=random.randint(10, st.MAP_HEIGHT - 10)) for i in range(self.wave)])
        enemies_list.extend([SlowEnemy(x=random.randint(10, st.MAP_WIDTH - 10), y=random.randint(10, st.MAP_HEIGHT - 10)) for i in range(self.wave*2)])
        # print(enemies_list)
        # enemies_list.extend([Enemy(x=random.randint(10, st.MAP_WIDTH - 10), y=random.randint(10, st.MAP_HEIGHT - 10), hp=50, speed=0.6, size=(20, 20), color=st.RED, view_range=2000) for i in range(self.wave * 2)])