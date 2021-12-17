import numpy as np


class DNA:
    def __init__(self,
                 size_gene: float,  # 0 to 1
                 mutation_rate,  # prob of a nucleotide changing during replication
                 ):
        self.mutation_rate = mutation_rate
        self.size_gene = size_gene if size_gene is not None else np.random.uniform(0.001, 0.03)

    def mutate(self):
        if np.random.random() < self.mutation_rate:
            d_size = np.random.uniform()
            d_size *= np.random.choice([-1, 1])
            self.size_gene = min(max(0.001, self.size_gene + d_size), 0.03)

    def copy(self):
        return DNA(self.size_gene, self.mutation_rate)
