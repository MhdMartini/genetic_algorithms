import numpy as np
from dna import DNA
import pygame as pg


class Bloop:
    def __init__(self,
                 dna: DNA,  # dna, contains radius info 1 to 255
                 pos: np.array,  # position
                 hp=1,  # health
                 dt=1e-2,  # time increment
                 ):

        self.dna = dna
        self.r = dna.size_gene
        self.pos = pos if pos is not None else np.random.uniform(self.r, 1 - self.r, size=2)
        self.v = self.get_v0()
        self.hp = hp
        self.dt = dt
        self.dc = 255 * dt

    def get_v0(self):
        v_mag = np.interp(self.r, (0, 0.03), (1, 0.01))  # 1 / self.r
        heading = np.random.random() * 2 * np.pi
        v = v_mag * np.array([np.cos(heading), np.sin(heading)])
        return v

    def move(self):
        # handle boundary collisions
        corr = (self.pos > 1 - self.r) | (self.pos < self.r)
        self.v *= np.interp(corr, (0, 1), (1, -1))

        # update position
        self.pos += self.v * self.dt

    def iterate(self):
        self.move()
        self.hp -= self.dt

    def copy(self):
        new_dna = self.dna.copy()
        new_dna.mutate()
        return Bloop(dna=new_dna,
                     pos=np.copy(self.pos),
                     hp=self.hp,
                     dt=self.dt)

    def show(self, screen, scale):
        color = np.ones(3) * 255 * min(self.hp, 1)
        color = color.astype(np.uint8)
        pg.draw.circle(screen,
                       color=color,
                       center=(self.pos[0] * scale, self.pos[1] * scale),
                       radius=self.r * scale)


if __name__ == '__main__':
    size_gene = np.random.uniform()
    mutation_rate = 1e-2
    nuc_count = 2
    dna = DNA(size_gene, mutation_rate)
    b = Bloop(dna, np.array([0., 0.]))
    print(b.pos, b.hp)
    b.iterate()
    print(b.pos, b.hp)
