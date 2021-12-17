"""
for gen in range(n_generations):
    fitness_array = evaluate(population, fitness_func)
    population = breed(population, fitness_array)
"""
import numpy as np
from dna import DNA, Population
import string
from env import VectorEnv
from itertools import count


if __name__ == '__main__':
    chars = list(string.ascii_letters + string.punctuation + string.digits + " ")
    nuc_count = len(chars)
    target = f"to be or not to be, that is the question"
    target_vector = np.array([chars.index(c) for c in target])
    gene_len = target_vector.shape[0]

    n_individuals = 300
    mutation_rate = 1e-2

    gene_sample = DNA(sequence=np.random.choice(nuc_count, size=gene_len),
                      mutation_rate=mutation_rate,
                      nuc_count=nuc_count)
    population = Population(gene_sample, n_individuals)
    env = VectorEnv(population.pop, target_vector)

    for gen in count():
        fitness_array = env.evaluate()
        population.breed(fitness_array)

        s = population.pop[np.argmax(fitness_array)].sequence
        print("".join([chars[i] for i in s]))
        if np.array_equal(s, target_vector):
            print(f"Done in {gen} generations!")
            break
