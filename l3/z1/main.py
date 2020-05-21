import random
import time
import math

POPSIZE = 10
T_SIZE = 4
NOISE = 0.01


def yang(x, eps):
    return sum(epsi * abs(xi)**i for i, (xi, epsi) in enumerate(zip(x, eps), 1))


def crossover(parent_a, parent_b):
    v = parent_a.copy()
    w = parent_b.copy()

    c = random.randrange(len(v))
    d = random.randrange(len(w))

    if c > d:
        c, d = d, c

    if c != d:
        for i in range(c, d):
            v[i], w[i] = w[i], v[i]

    return v, w


def mutate(individual):
    mutation_point = random.randrange(len(individual))
    return [gene if i == mutation_point else random.gauss(gene, NOISE) for i, gene in enumerate(individual)]

def tournament_selection(fitnesses):
    popsize = len(fitnesses)

    best = random.randrange(popsize)

    for i in range(1, T_SIZE):
        n = random.randrange(popsize)
        if fitnesses[n] < fitnesses[best]:
            best = n

    return best


def genetic_algorithm(max_time, x, assess_fitness):
    population = []

    for _ in range(POPSIZE):
        population.append(mutate(x))

    best = None
    best_fitness = 100000

    start = time.time()

    while time.time() - start < max_time:
        fitnesses = []
        for individual in population:
            fitness = assess_fitness(individual)
            fitnesses.append(fitness)

            if best is None or fitness < best_fitness:
                best = individual
                best_fitness = fitness
                last_best = time.time()

        q = []

        for _ in range(POPSIZE//2):
            parent_a = population[tournament_selection(fitnesses)]
            parent_b = population[tournament_selection(fitnesses)]

            child_a, child_b = crossover(parent_a, parent_b)

            q += [mutate(child_a), mutate(child_b)]

        population = q

        if time.time() - last_best > math.log(max_time):
            break

    return best, best_fitness


def main():
    inputs = input().split()
    t = int(inputs[0])
    x = list(map(float, inputs[1:6]))
    eps = list(map(float, inputs[6:11]))

    best, fitness = genetic_algorithm(t, x, lambda x: yang(x, eps))

    print(*best, fitness)


if __name__ == "__main__":
    main()
