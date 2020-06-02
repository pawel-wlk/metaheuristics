from enum import Enum
from typing import List
from sys import maxsize
import random
import time
from sys import stderr
import math

T_SIZE = 4


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


class Maze:
    EMPTY = 0
    AGENT = 5
    WALL = 1
    GOAL = 8
    HORIZONTAL_TUNNEL = 2
    VERTICAL_TUNNEL = 3

    def __init__(self, maze_map, max_steps):
        self.map = maze_map
        self.start_pos = self.find_agent()
        self.max_steps = max_steps
        self.n = len(maze_map)
        self.m = len(maze_map[0])

    def find_agent(self):
        for i, _ in enumerate(self.map):
            for j, el in enumerate(self.map[i]):
                if el == self.AGENT:
                    return (j, i)

    def eval_path(self, path: List[Direction]):
        cost = 0
        x_pos, y_pos = self.start_pos

        for direction in path:
            cost += 1
            if cost > self.max_steps:
                return maxsize

            if self.map[y_pos][x_pos] == self.HORIZONTAL_TUNNEL and direction in (Direction.UP, Direction.DOWN):
                continue

            if self.map[y_pos][x_pos] == self.VERTICAL_TUNNEL and direction in (Direction.LEFT, Direction.RIGHT):
                continue

            x_move, y_move = direction.value
            new_x = x_pos + x_move
            new_y = y_pos + y_move

            if self.map[new_y][new_x] == self.GOAL:
                return cost

            if self.map[new_y][new_x] != self.WALL:
                x_pos, y_pos = new_x, new_y

        return maxsize

    def random_walk(self):
        path = []
        x, y = self.start_pos


        if self.map[y][x] == self.HORIZONTAL_TUNNEL:
            direction = random.choice((Direction.LEFT, Direction.RIGHT))
        elif self.map[y][x] == self.VERTICAL_TUNNEL:
            direction = random.choice((Direction.UP, Direction.DOWN))
        else:
            direction = random.choice(list(Direction))

        xmove, ymove = direction.value

        while len(path) < self.n * self.m / 3:
            if self.map[y+ymove][x+xmove] == 8:
                path.append(direction)
                return path, True
            elif self.map[y+ymove][x+xmove] == 1:
                direction = random.choice(list(Direction))
                xmove, ymove = direction.value
            else:
                x += xmove
                y += ymove
                path.append(direction)
                if random.random() < 0.15:
                    direction = random.choice(list(Direction))
                    xmove, ymove = direction.value

        return path, False

    def generate_naive_path(self):
        found = False
        while not found:
            path, found = self.random_walk()

        return path


def crossover(parent_a, parent_b):
    v = parent_a.copy()
    w = parent_b.copy()

    l = min(len(v), len(w))

    c = random.randrange(l)
    d = random.randrange(l)

    if c > d:
        c, d = d, c

    if c != d:
        for i in range(c, d):
            v[i], w[i] = w[i], v[i]

    return v, w


def mutate(individual):
    i = random.randrange(len(individual))
    j = random.randrange(len(individual))
    individual[i], individual[j] = individual[j], individual[i]
    return individual


def tournament_selection(fitnesses):
    popsize = len(fitnesses)

    best = random.randrange(popsize)

    for i in range(1, T_SIZE):
        n = random.randrange(popsize)
        if fitnesses[n] < fitnesses[best]:
            best = n

    return best


def genetic_algorithm(max_time, maze):
    popsize = 10
    population = [maze.generate_naive_path() for _ in range(popsize)]

    best = None
    best_fitness = 100000

    start = time.time()

    while time.time() - start < max_time:
        fitnesses = []
        for individual in population:
            fitness = maze.eval_path(individual)
            fitnesses.append(fitness)

            if best is None or fitness < best_fitness:
                best = individual
                best_fitness = fitness
                last_best = time.time()

        q = []

        for _ in range(popsize//2):
            parent_a = population[tournament_selection(fitnesses)]
            parent_b = population[tournament_selection(fitnesses)]

            child_a, child_b = crossover(parent_a, parent_b)

            q += [mutate(child_a), mutate(child_b)]

        population = q

        if time.time() - last_best > math.log(max_time):
            break

    return best, best_fitness


if __name__ == "__main__":
    max_time, n, m = [int(word) for word in input().split()]

    maze_map = [[int(char) for char in input()[:m]] for _ in range(n)]

    moves = {'U': Direction.UP, 'D': Direction.DOWN,
             'R': Direction.RIGHT, 'L': Direction.LEFT}

    maze = Maze(maze_map, n*m)

    best, fitness = genetic_algorithm(max_time, maze)

    move_names = {Direction.UP: 'U', Direction.DOWN: 'D',
                  Direction.RIGHT: 'R', Direction.LEFT: 'L'}

    print(fitness)
    print(''.join(move_names[move] for move in best[:fitness]), file=stderr)
