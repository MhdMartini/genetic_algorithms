import pygame as pg
import numpy as np
from bloop import Bloop
from food import Food
from dna import DNA


SCALE = 900
bg_color = pg.Color(0, 0, 0)
bloop_color = pg.Color(255, 255, 255)
food_color = pg.Color(23, 53, 105)


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

    def draw_bloop(self, bloop):
        color = np.ones(3) * 255 * min(bloop.hp, 1)
        color = color.astype(np.uint8)
        pg.draw.circle(self.screen,
                       color=color,
                       center=(bloop.pos[0] * SCALE, bloop.pos[1] * SCALE),
                       radius=bloop.r * SCALE)

    def draw_food(self, food):
        pg.draw.rect(self.screen,
                     color=np.random.randint(255, size=3),
                     rect=(food.pos[0] * SCALE, food.pos[1] * SCALE, food.r * SCALE, food.r * SCALE))

    def copy_bloop(self, bloop):
        new_dna = DNA(size_gene=bloop.dna.size_gene, mutation_rate=bloop.dna.mutation_rate)
        new_dna.mutate()
        return Bloop(dna=new_dna,
                     pos=np.copy(bloop.pos),
                     hp=bloop.hp,
                     dt=bloop.dt)

    def main(self):
        self.screen = self.init_pg()
        self.clock = pg.time.Clock()
        run = True
        while run:
            self.clock.tick(self.fps)
            self.screen.fill(bg_color)

            # handle bloops and food
            for idx in range(len(self.bloops) - 1, -1, -1):
                bloop = bloops[idx]
            # for bloop in self.bloops:
                # iterate bloops
                bloop.iterate()
                if bloop.hp <= 0:
                    self.bloops.remove(bloop)
                    continue
                elif bloop.hp > 2:
                    if len(self.bloops) < 20:
                        bloop.hp /= 2
                        bloops.append(self.copy_bloop(bloop))
                # draw bloops
                self.draw_bloop(bloop)
                # bloops eat food
                for food in self.food:
                    # draw food
                    if np.linalg.norm(bloop.pos - food.pos) < bloop.r:
                        bloop.hp += food.hp
                        food.spawn()

            for food in self.food:
                self.draw_food(food)

            pg.display.flip()
            for event in pg.event.get():
                # look for quit command
                if event.type == pg.QUIT:
                    run = False
                    break

        pg.quit()


if __name__ == '__main__':
    # generate bloops
    mutation_rate = 1e-2
    dt = 1e-2
    bloop_hp = 1
    n_bloops = 10
    bloops = []
    for i in range(n_bloops):
        bloops.append(Bloop(dna=DNA(size_gene=None, mutation_rate=mutation_rate),
                            pos=None,
                            hp=bloop_hp,
                            dt=dt))

    # generate food
    n_food = 75
    food_hp = 1
    food_r = 5e-3
    food = []
    for i in range(n_food):
        food.append(Food(food_hp, food_r))

    env = BloopEnv(bloops=bloops,
                   food=food,
                   dt=dt)
    env.main()
