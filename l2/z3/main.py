from enum import Enum
from typing import List
from sys import maxsize
from random import random, choice, randrange
from time import time
from sys import stderr
from math import exp


INIT_TEMP = 1000000
DECREASE_FACTOR = 0.999


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

    def __init__(self, maze_map, max_steps):
        self.map = maze_map
        self.start_pos = self.find_agent()
        self.max_steps = max_steps

    def find_agent(self):
        for i, _ in enumerate(self.map):
            for j, el in enumerate(self.map[i]):
                if el == self.AGENT:
                    return (j, i)


    def get_move_to_goal(self, x, y):
        if self.map[y+1][x] == self.GOAL:
            return Direction.DOWN
        elif self.map[y-1][x] == self.GOAL:
            return Direction.UP
        elif self.map[y][x+1] == self.GOAL:
            return Direction.RIGHT
        elif self.map[y][x-1] == self.GOAL:
            return Direction.LEFT
        else:
            return None

    def eval_path(self, path: List[Direction]):
        cost = 0
        x_pos, y_pos = self.start_pos

        for direction in path:
            cost += 1
            if cost > self.max_steps:
                return maxsize

            x_move, y_move = direction.value
            new_x = x_pos + x_move
            new_y = y_pos + y_move

            if self.map[new_y][new_x] == self.GOAL:
                return cost

            if self.map[new_y][new_x] != self.WALL:
                x_pos, y_pos = new_x, new_y

        return maxsize

    def generate_naive_path(self):
        moves = []
        x_pos, y_pos = self.start_pos
        new_x, new_y = x_pos, y_pos

        directions = list(Direction)
        cur_direction = 0
        while self.map[y_pos][x_pos] != self.GOAL:
            move_to_goal = self.get_move_to_goal(x_pos, y_pos)
            if move_to_goal:
                moves.append(move_to_goal)
                break

            x_move, y_move = directions[cur_direction].value
            new_x = x_pos + x_move
            new_y = y_pos + y_move

            if self.map[new_y][new_x] == self.WALL:
                cur_direction = (cur_direction + 1) % len(directions)
            else:
                x_pos, y_pos = new_x, new_y
                moves.append(directions[cur_direction])

        return moves


def tweak(path):
    copy = path.copy()
    i = randrange(len(path))
    j = randrange(len(path))
    copy[i], copy[j] = copy[j], copy[i]

    return copy


def simulated_annealing(maze, max_time):
    t = INIT_TEMP

    s = maze.generate_naive_path()
    best = s
    quality_best = maze.eval_path(best)
    print(quality_best)

    start = time()
    while time() - start < max_time:
        r = tweak(s)
        quality_s = maze.eval_path(s)
        quality_r = maze.eval_path(r)

        if quality_r < quality_s or random() < exp((quality_s - quality_r) / t):
            s = r
            quality_s = quality_r

        t *= DECREASE_FACTOR

        if quality_s < quality_best:
            if abs(quality_s - quality_best)/quality_best < 0.000000001:
                return best
            best = s
            quality_best = quality_s

    return best


if __name__ == "__main__":
    max_time, n, m = [int(word) for word in input().split()]

    maze_map = [[int(char) for char in input()[:m]] for _ in range(n)]

    maze = Maze(maze_map, n*m)

    best = simulated_annealing(maze, max_time)

    move_names = {Direction.UP: 'U', Direction.DOWN: 'D',
                  Direction.RIGHT: 'R', Direction.LEFT: 'L'}

    print(maze.eval_path(best))
    print(''.join(move_names[move] for move in best), file=stderr)
