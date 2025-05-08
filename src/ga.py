import numpy as np
from typing import Tuple, List, Optional

class GeneticAlgorithm:
    """
    A simple real-valued genetic algorithm for evolving weight vectors.
    """
    def __init__(
        self,
        pop_size: int,
        genome_length: int,
        crossover_rate: float = 0.9,
        mutation_rate: float = 0.05,
        mutation_sigma: float = 0.1,
        tournament_size: int = 3,
        elitism: bool = True,
        elitism_frac: float = 0.05,
        rng: Optional[np.random.Generator] = None
    ):
        """
        Args:
            pop_size: Number of individuals in population.
            genome_length: Length of the genome vector per individual.
            crossover_rate: Probability of performing crossover.
            mutation_rate: Probability of mutating each gene.
            mutation_sigma: Std dev of Gaussian noise for mutation.
            tournament_size: Number of individuals per tournament.
            elitism: Whether to carry top individuals unchanged to next gen.
            elitism_frac: Fraction of population to carry over as elites.
            rng: Optional NumPy random Generator for reproducibility.
        """
        self.pop_size = pop_size
        self.genome_length = genome_length
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.mutation_sigma = mutation_sigma
        self.tournament_size = tournament_size
        self.elitism = elitism
        self.elitism_frac = elitism_frac
        self.rng = rng or np.random.default_rng()

    def init_population(self) -> np.ndarray:
        """
        Initialize population uniformly in [-1, 1].

        Returns:
            pop: array of shape (pop_size, genome_length).
        """
        return self.rng.uniform(-1.0, 1.0, size=(self.pop_size, self.genome_length))

    def tournament_selection(self, fitnesses: np.ndarray) -> List[int]:
        """
        Perform tournament selection to choose parent indices.

        Args:
            fitnesses: 1D array of length pop_size.
        Returns:
            List of selected parent indices (length pop_size).
        """
        parents = []
        for _ in range(self.pop_size):
            # sample k distinct individuals
            contenders = self.rng.choice(self.pop_size, size=self.tournament_size, replace=False)
            # pick the best
            winner = contenders[np.argmax(fitnesses[contenders])]
            parents.append(winner)
        return parents

    def crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Uniform crossover between two parents.

        Args:
            parent1, parent2: 1D genome arrays.
        Returns:
            Two offspring genome arrays.
        """
        if self.rng.random() < self.crossover_rate:
            mask = self.rng.random(self.genome_length) < 0.5
            child1 = np.where(mask, parent1, parent2)
            child2 = np.where(mask, parent2, parent1)
        else:
            child1 = parent1.copy()
            child2 = parent2.copy()
        return child1, child2

    def mutate(self, genome: np.ndarray) -> np.ndarray:
        """
        Mutate a genome by adding Gaussian noise to random genes.

        Args:
            genome: 1D genome array.
        Returns:
            Mutated genome.
        """
        mutation_mask = self.rng.random(self.genome_length) < self.mutation_rate
        noise = self.rng.normal(0.0, self.mutation_sigma, size=self.genome_length)
        genome[mutation_mask] += noise[mutation_mask]
        return genome

    def step(self, population: np.ndarray, fitnesses: np.ndarray) -> np.ndarray:
        """
        Create the next generation from current population and fitnesses.

        Args:
            population: array shape (pop_size, genome_length).
            fitnesses: array shape (pop_size,).
        Returns:
            new_population: array shape (pop_size, genome_length).
        """
        new_pop = []

        # Elitism: carry over top individuals
        if self.elitism and self.elitism_frac > 0:
            n_elites = max(1, int(self.elitism_frac * self.pop_size))
            elite_indices = np.argsort(fitnesses)[-n_elites:]
            elites = population[elite_indices]
        else:
            elites = np.empty((0, self.genome_length))

        # Parent selection
        parent_indices = self.tournament_selection(fitnesses)

        # Generate new individuals
        for i in range(0, self.pop_size - elites.shape[0], 2):
            idx1 = parent_indices[i]
            idx2 = parent_indices[i+1]
            p1 = population[idx1]
            p2 = population[idx2]
            c1, c2 = self.crossover(p1, p2)
            new_pop.append(self.mutate(c1))
            new_pop.append(self.mutate(c2))

        # Trim if overfilled and concatenate elites
        new_pop = np.array(new_pop)[: self.pop_size - elites.shape[0]]
        if elites.size:
            new_pop = np.vstack([new_pop, elites])

        return new_pop