import numpy as np


class Food:
    def __init__(self, hp=1, r=5e-3):
        self.hp = hp
        self.r = r
        self.spawn()

    def spawn(self):
        self.pos = np.random.uniform(self.r, 1 - self.r, size=2)
