from enum import Enum
from typing import List
from sys import maxsize
import random
from time import time
from sys import stderr
import math

INIT_TEMP = 200
DECREASE_FACTOR = 0.99


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


MOVE_NAMES = {Direction.UP: 'U', Direction.DOWN: 'D',
              Direction.RIGHT: 'R', Direction.LEFT: 'L'}


class Maze:
    EMPTY = 0
    AGENT = 5
    WALL = 1
    GOAL = 8
    HORIZONTAL_TUNNEL = 3
    VERTICAL_TUNNEL = 2

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

            if self.map[new_y][new_x] == self.HORIZONTAL_TUNNEL and direction in (Direction.UP, Direction.DOWN):
                pass
            elif self.map[new_y][new_x] == self.VERTICAL_TUNNEL and direction in (Direction.LEFT, Direction.RIGHT):
                pass
            elif self.map[new_y][new_x] == self.WALL:
                pass
            else:
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
            if self.map[y+ymove][x+xmove] == self.GOAL:
                path.append(direction)
                return path, True
            elif (self.map[y+ymove][x+xmove] == self.WALL) \
                    or (self.map[y+ymove][x+xmove] == self.HORIZONTAL_TUNNEL and direction in (Direction.UP, Direction.DOWN)) \
                    or (self.map[y+ymove][x+xmove] == self.VERTICAL_TUNNEL and direction in (Direction.LEFT, Direction.RIGHT)):
                if self.map[y][x] == self.HORIZONTAL_TUNNEL:
                    direction = random.choice(
                        (Direction.LEFT, Direction.RIGHT))
                elif self.map[y][x] == self.VERTICAL_TUNNEL:
                    direction = random.choice((Direction.UP, Direction.DOWN))
                else:
                    direction = random.choice(list(Direction))
                xmove, ymove = direction.value
            else:
                x += xmove
                y += ymove
                path.append(direction)
                if random.random() < 0.15:
                    if self.map[y][x] == self.HORIZONTAL_TUNNEL:
                        direction = random.choice(
                            (Direction.LEFT, Direction.RIGHT))
                    elif self.map[y][x] == self.VERTICAL_TUNNEL:
                        direction = random.choice(
                            (Direction.UP, Direction.DOWN))
                    else:
                        direction = random.choice(list(Direction))
                    xmove, ymove = direction.value

        return path, False

    def generate_naive_path(self):
        found = False
        while not found:
            path, found = self.random_walk()

        return path


def tweak(path):
    i = random.randrange(len(path))
    j = random.randrange(i, len(path))

    if random.random() < 0.5:
        return path[:i+1] + path[j:i:-1] + path[j+1:]
    else:
        return path[:i+1] + [random.choice(list(Direction)) for _ in range(j-i)] + path[j+1:]



def simulated_annealing(max_time, maze, init_solution):
    t = INIT_TEMP

    # s = maze.generate_naive_path()
    s = init_solution
    best = s
    quality_best = maze.eval_path(best)
    # t = 3*maze.eval_path(init_solution)

    start = time()
    last_best = time()
    while time() - start < max_time and t > 0:
        r = tweak(s)
        quality_s = maze.eval_path(s)
        quality_r = maze.eval_path(r)

        if quality_r < quality_s or random.random() < math.exp((quality_s - quality_r) / t):
            s = r
            quality_s = quality_r

        t *= DECREASE_FACTOR

        if quality_s < quality_best:
            best = s
            quality_best = quality_s
            last_best = time()
        if time() - last_best > math.log(max_time):
            break

    return best, quality_best


if __name__ == "__main__":
    max_time, n, m = [int(word) for word in input().split()]

    maze_map = [[int(char) for char in input()[:m]] for _ in range(n)]

    moves = {'U': Direction.UP, 'D': Direction.DOWN,
             'R': Direction.RIGHT, 'L': Direction.LEFT}

    init_solution = [moves[c] for c in input().strip()]

    maze = Maze(maze_map, n*m)

    # max_time = 10
    best, cost = simulated_annealing(max_time, maze, init_solution)

    print(cost)
    print(''.join(MOVE_NAMES[move] for move in best[:cost]), file=stderr)
