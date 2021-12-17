import numpy as np


class Env:
    def __init__(self, population: np.array):
        self.population = population
        self.pop_size = self.population.shape[0]

    def fitness(self):
        pass

    def evaluate(self):
        fitness_array = np.zeros(self.pop_size, dtype=np.float64)
        for i in range(self.pop_size):
            fitness_array[i] = self.fitness(self.population[i].sequence)
        return fitness_array


class VectorEnv(Env):
    def __init__(self, population: np.array, target_vector):
        super(VectorEnv, self).__init__(population)
        self.target_vector = target_vector

    def fitness(self, sequence: np.array):
        return np.sum(sequence == self.target_vector) ** 6
