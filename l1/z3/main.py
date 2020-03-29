from enum import Enum
from typing import List
from sys import maxsize
from random import random, randrange
from time import time
from sys import stderr

MAX_TABU_LEN = 64
NEIGHBOUR_SWAPS = 16


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


def tabu_search(maze: Maze, max_time):
    s = maze.generate_naive_path()
    best = s
    tabu_list = []
    tabu_list.append(s)

    start = time()
    while time() - start < max_time:
        if len(tabu_list) > MAX_TABU_LEN:
            tabu_list.pop(0)

        r = s
        for _ in range(NEIGHBOUR_SWAPS):
            w = s.copy()
            i = randrange(len(s))
            j = randrange(len(s))
            w[i], w[j] = w[j], w[i]
            if w not in tabu_list and (maze.eval_path(w) < maze.eval_path(r) or r in tabu_list):
                r = w

        if r not in tabu_list:
            s = r
            tabu_list.append(s)
        if maze.eval_path(s) < maze.eval_path(best):
            best = s

    return best


if __name__ == "__main__":
    max_time, n, m = [int(word) for word in input().split()]

    maze_map = [[int(char) for char in input()[:m]] for _ in range(n)]

    maze = Maze(maze_map, n*m)

    best = tabu_search(maze, max_time)

    move_names = {Direction.UP: 'U', Direction.DOWN: 'D',
                  Direction.RIGHT: 'R', Direction.LEFT: 'L'}

    print(maze.eval_path(best))
    print(''.join(move_names[move] for move in best), file=stderr)
