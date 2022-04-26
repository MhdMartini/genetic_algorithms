import pygame as pg
import numpy as np
from bloop import Bloop
from food import Food
from dna import DNA


SCALE = 900
bg_color = pg.Color(0, 0, 0)
bloop_color = pg.Color(255, 255, 255)


class BloopEnv:
    def __init__(self,
                 bloops: np.array,
                 food: np.array,
                 dt,
                 ):
        self.bloops = bloops
        self.food = food
        self.fps = int(1 / dt)

    def init_pg(self):
        pg.init()
        screen = pg.display.set_mode((SCALE, SCALE), pg.SRCALPHA)
        screen.fill(bg_color)
        pg.display.set_caption("Mohamed Martini - Bloops")
        return screen

    def main(self):
        self.screen = self.init_pg()
        self.clock = pg.time.Clock()
        run = True
        while run:
            self.clock.tick(self.fps)
            self.screen.fill(bg_color)

            # handle bloops and food
            bloops_len = len(self.bloops)
            if not bloops_len:
                break
            for idx in range(bloops_len - 1, -1, -1):
                bloop = bloops[idx]
                # iterate bloops
                bloop.iterate()
                if bloop.hp <= 0:
                    self.bloops.remove(bloop)
                    continue
                elif bloop.hp > 2:
                    if len(self.bloops) < 20:
                        bloop.hp /= 2
                        bloops.append(bloop.copy())
                # draw bloops
                bloop.show(self.screen, SCALE)
                # bloops eat food
                for food in self.food:
                    # draw food
                    if np.linalg.norm(bloop.pos - food.pos) < bloop.r:
                        bloop.hp += food.hp
                        food.spawn()

            for food in self.food:
                food.show(self.screen, SCALE)

            pg.display.flip()
            for event in pg.event.get():
                # look for quit command
                if event.type == pg.QUIT:
                    run = False
                    break

        pg.quit()


def make_bloops(n_bloops, mutation_rate, bloop_hp, dt):
    bloops = []
    for i in range(n_bloops):
        bloops.append(Bloop(dna=DNA(size_gene=None, mutation_rate=mutation_rate),
                            pos=None,
                            hp=bloop_hp,
                            dt=dt))
    return bloops


def make_food(n_food, food_hp, food_r):
    food = []
    for _ in range(n_food):
        food.append(Food(hp=food_hp, r=food_r))
    return food


if __name__ == '__main__':
    # generate bloops
    mutation_rate = 1e-2
    dt = 1e-2
    bloop_hp = 1
    n_bloops = 10

    # generate food
    n_food = 75
    food_hp = 1
    food_r = 5e-3

    while not input("Press enter to continue..."):
        bloops = make_bloops(n_bloops, mutation_rate, bloop_hp, dt)
        food = make_food(n_food, food_hp, food_r)
        env = BloopEnv(bloops, food, dt)
        env.main()
