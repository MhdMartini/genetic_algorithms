import numpy as np


def softmax(array):
    exp = np.exp(array - np.max(array))  # shift to avoid overflow
    return exp / np.sum(exp)


class DNA:
    def __init__(self, sequence: np.array,  # 1d numpy array
                 mutation_rate,  # prob of a nucleotide changing during replication
                 nuc_count):  # number of different nucelotides - values to populate the sequence
        self.sequence = sequence
        self.length = self.sequence.shape[0]
        self.mutation_rate = mutation_rate
        self.nuc_count = nuc_count

    def crossover(self, other_dna):
        idx = np.random.choice(self.length)
        self.sequence[idx:] = other_dna.sequence[idx:]

    def mutate(self):
        rand = np.random.random(size=self.length)
        mut = rand < self.mutation_rate
        num_mut = np.sum(mut)
        self.sequence[mut] = np.random.choice(self.nuc_count, size=num_mut)


class Population:
    def __init__(self, dna: DNA, n_individuals):
        """given a dna object, generate a random population like the dna"""
        self.gene_shape = dna.sequence.shape
        self.gene_length = dna.length
        self.gene_nuc_count = dna.nuc_count
        self.gene_mutation_rate = dna.mutation_rate
        self.n_individuals = n_individuals
        self.pop = self.get_rand_pop()

    def get_rand_pop(self):
        pop = np.empty(self.n_individuals, dtype=DNA)
        for i in range(self.n_individuals):
            pop[i] = DNA(sequence=np.random.choice(self.gene_nuc_count, size=self.gene_length),
                         mutation_rate=self.gene_mutation_rate, nuc_count=self.gene_nuc_count)
        return pop

    def copy(self, dna):
        return DNA(sequence=np.copy(dna.sequence), mutation_rate=dna.mutation_rate, nuc_count=dna.nuc_count)

    def breed(self, fitness_array):
        # fitness_array = fitness_array / np.sum(fitness_array)
        fitness_array = softmax(fitness_array)
        for i in range(self.n_individuals):
            dna1 = np.random.choice(self.n_individuals, p=fitness_array)
            dna2 = np.random.choice(self.n_individuals, p=fitness_array)
            child_dna = self.copy(self.pop[dna1])
            child_dna.crossover(self.pop[dna2])
            child_dna.mutate()
            self.pop[i] = child_dna
