import time
import random
import math
from collections import defaultdict, Counter
import sys

POP_SIZE = 10
ELITE_SIZE = 4
T_SIZE = 2


def drop_duplicates(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


def word_score(word):
    counts = Counter(word)

    for letter, count in counts.items():
        if count > letter_count[letter]:
            return 0

    score = sum(letter_value[char] for char in word)

    if word in dictionary:
        return score
    else:
        return 0


def mutate(word):
    letters = Counter(word)
    remaining_dict = {
        char: letter_count[char]-letters[char] for char in letter_count}
    remaining = [char for char, value in remaining_dict.items() if value > 0]
    if not remaining:
        return word

    letter = random.choice(remaining)
    index = random.randint(0, len(word))

    rand = random.random()
    if rand > 0.1:
        word = word[:index] + letter + word[index+1:]
    else:
        word = word[:index] + letter + word[index:]

    return word



def crossover(parent_a, parent_b):
    v = list(parent_a)
    w = list(parent_b)
    p = 0.1

    l = min(len(v), len(w))

    for i in range(l):
        if random.random() < p:
            v[i], w[i] = w[i], v[i]

    return ''.join(v), ''.join(w)


def tournament_selection(fitnesses):
    popsize = len(fitnesses)

    best = random.randrange(popsize)

    for i in range(1, T_SIZE):
        n = random.randrange(popsize)
        if fitnesses[n] > fitnesses[best]:
            best = n

    return best


def genetic_algorithm(max_time, initial_population):
    population = initial_population

    best = None
    best_fitness = 100000

    start = time.time()

    while time.time() - start < max_time:
        fitnesses = []
        for individual in population:
            fitness = word_score(individual)
            fitnesses.append(fitness)

            if best is None or fitness > best_fitness:
                best = individual
                best_fitness = fitness
                last_best = time.time()

        q = drop_duplicates(map(lambda pair: pair[1], sorted(enumerate(
            population), key=lambda pair: fitnesses[pair[0]], reverse=True)))[:ELITE_SIZE]

        for _ in range((POP_SIZE - ELITE_SIZE)//2):
            parent_a = population[tournament_selection(fitnesses)]
            parent_b = population[tournament_selection(fitnesses)]

            child_a, child_b = crossover(parent_a, parent_b)

            q += [mutate(child_a), mutate(child_b)]

        population = q

        # if time.time() - last_best > math.log(max_time):
        #     break

    return best, best_fitness


if __name__ == "__main__":
    with open('dict.txt') as f:
        dictionary = set((word for word in f.read().split()))
    max_time, letters_num, words_num = [int(word) for word in input().split()]
    letter_value = {}
    letter_count = defaultdict(int)
    for _ in range(letters_num):
        char, value = input().split()
        letter_value[char] = int(value)
        letter_count[char] += 1

    words = []
    for _ in range(words_num):
        words.append(input().strip())

    best, fitness = genetic_algorithm(max_time, words)
    print(fitness)
    print(best, file=sys.stderr)
