from math import exp
from time import time
import random
from dataclasses import dataclass


INIT_TEMP = 100
DECREASE_FACTOR = 0.99

VALUES = [0, 32, 64, 128, 160, 192, 223, 255]


@dataclass
class Block:
    start_row: int
    start_column: int
    width: int
    height: int
    value: int


class BlockMatrix:
    def __init__(self, blocks = []):
        self.blocks = blocks 

    @classmethod
    def get_initialized(cls, n, m, k):
        new = cls()
        new.n = n
        new.m = m
        value_index = 0
        for i in range(0, n-k+1, k):
            block_height = n - i if i + 2*k > n else k
            for j in range(0, m-k+1, k):
                block_width = m - j if j + 2*k > m else k

                new.blocks.append(
                    Block(i, j, block_width, block_height, VALUES[value_index]))

                value_index = (value_index + 1) % len(VALUES)

        return new

    def __getitem__(self, key):
        row, column = key

        for block in self.blocks:
            if block.start_row <= row and block.start_column <= column \
                    and block.start_row + block.height > row and block.start_column + block.width > column:
                return block.value

        return -1


    def copy(self):
        return BlockMatrix(self.blocks.copy())

    def __repr__(self):
        return '\n'.join(' ' .join(str(self[i,j]) for j in range(self.m)) for i in range(self.n))



def matrix_distance(matrix, block_matrix, n, m):
    return 1 / (n * m) * sum((matrix[i][j] - block_matrix[i, j])**2 for j in range(m) for i in range(n))



def change_value(block_matrix, k):
    matrix_copy = block_matrix.copy()
    block = random.choice(matrix_copy.blocks)
    block.value = random.choice(list(filter(lambda val: val != block.value, VALUES)))
    return matrix_copy


def change_size(block_matrix, k):
    matrix_copy = block_matrix.copy()
    filtered = [block for block in matrix_copy.blocks if block.width > k or block.height > k]
    if len(filtered) == 0:
        return matrix_copy

    block = random.choice(filtered)

    if block.width > k:
        if block.start_column != 0:
            for b in matrix_copy.blocks:
                if b.start_column + b.width == block.start_column:
                    b.width += 1

            block.start_column += 1
        else:
            for b in matrix_copy.blocks:
                if block.start_column + block.width == b.start_column:
                    b.start_column -= 1

            block.width -= 1

    if block.height > k:
        if block.start_row != 0:
            for b in matrix_copy.blocks:
                if b.start_row + b.height == block.start_row:
                    b.height += 1

            block.start_row += 1
        else:
            for b in matrix_copy.blocks:
                if block.start_row + block.height == b.start_row:
                    b.start_row -= 1

            block.height -= 1

    return matrix_copy


def swap_blocks(block_matrix, k):
    matrix_copy = block_matrix.copy()
    block1 = random.choice(matrix_copy.blocks)
    block2 = random.choice(list(filter(lambda b: b != block1, matrix_copy.blocks)))

    block1.value, block2.value = block2.value, block1.value

    return matrix_copy



def tweak(block_matrix, k):
    return random.choice([change_value, change_value, swap_blocks])(block_matrix, k)



def simulated_annealing(max_time, matrix, n, m, k):
    quality = lambda solution: matrix_distance(matrix, solution, n, m)
    t = INIT_TEMP

    s = BlockMatrix.get_initialized(n, m, k)
    best = s
    quality_best = quality(best)

    start = time()
    while time() - start < max_time:
        r = tweak(s, k)
        quality_s = quality(s)
        quality_r = quality(r)

        if quality_r < quality_s or random.random() < exp((quality_s - quality_r) / t):
            s = r
            quality_s = quality_r

        t *= DECREASE_FACTOR

        if quality_s < quality_best:
            # if abs(quality_s - quality_best)/quality_best < 0.000000001:
            #     return quality_best
            best = s
            quality_best = quality_s

    return quality_best


def main():
    time, n, m, k = list(map(int, input().split()))
    matrix = [list(map(int, input().split())) for _ in range(n)]
    print(simulated_annealing(time, matrix, n, m, k))



if __name__ == "__main__":
    main()
