import os
import csv
import numpy as np
from src.config import get_experiments
from src.env_runner import EnvRunner
from src.network import FeedForwardNet
from src.ga import GeneticAlgorithm


def run_experiment(exp: dict, log_dir: str = 'logs'):
    """
    Run neuroevolution on a single environment as specified in exp dict.

    exp should contain:
      - env_id: str
      - ga_params: dict with pop_size, crossover_rate, mutation_rate, mutation_sigma, tournament_size, elitism, elitism_frac
      - net_arch: list of hidden layer sizes (without obs_dim or action_dim)
      - seeds: list of int
      - generations: int
      - episodes_per_eval: int

    Writes one CSV per seed to log_dir/{env_id}_seed{seed}.csv
    """
    env_id = exp['env_id']
    ga_params = exp['ga_params']
    net_arch = exp['net_arch']
    seeds = exp['seeds']
    generations = exp['generations']
    episodes = exp['episodes_per_eval']

    os.makedirs(log_dir, exist_ok=True)

    for seed in seeds:
        print(f"Running {env_id}  seed={seed}")
        # Prepare environment runner
        runner = EnvRunner(env_id, seed)
        # Build network (input + hidden + output)
        layer_sizes = [runner.obs_dim] + net_arch + [runner.action_dim]
        net = FeedForwardNet(layer_sizes)
        # Build GA
        ga = GeneticAlgorithm(
            pop_size=ga_params['pop_size'],
            genome_length=net.num_weights,
            crossover_rate=ga_params.get('crossover_rate', 0.9),
            mutation_rate=ga_params.get('mutation_rate', 0.05),
            mutation_sigma=ga_params.get('mutation_sigma', 0.1),
            tournament_size=ga_params.get('tournament_size', 3),
            elitism=ga_params.get('elitism', True),
            elitism_frac=ga_params.get('elitism_frac', 0.05)
        )
        # Initialize population
        population = ga.init_population()

        # Prepare log file
        log_path = os.path.join(log_dir, f"{env_id}_seed{seed}.csv")
        with open(log_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['seed', 'generation', 'best_fitness'])

            # Evolve
            for gen in range(generations):
                fitnesses = np.zeros(ga.pop_size)
                for i in range(ga.pop_size):
                    genome = population[i]
                    net.decode(genome)
                    fitnesses[i] = runner.evaluate(net, episodes)
                best = float(np.max(fitnesses))
                if gen % 10 == 0 or gen == generations - 1:
                    print(f"{env_id}  seed={seed}  gen={gen:3d}  best={best:.1f}")
                writer.writerow([seed, gen, best])
                population = ga.step(population, fitnesses)

        runner.close()
        print(f"Finished {env_id} seed={seed}, logs -> {log_path}")


def main():
    experiments = get_experiments()
    for exp in experiments:
        run_experiment(exp)


if __name__ == '__main__':
    main()