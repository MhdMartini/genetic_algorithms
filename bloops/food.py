import numpy as np
import pygame as pg


class Food:
    def __init__(self, hp=1, r=5e-3):
        self.hp = hp
        self.r = r
        self.spawn()

    def spawn(self):
        self.pos = np.random.uniform(self.r, 1 - self.r, size=2)

    def show(self, screen, scale):
        pg.draw.rect(screen,
                     color=np.random.randint(255, size=3),
                     rect=(self.pos[0] * scale, self.pos[1] * scale, self.r * scale, self.r * scale))
