from math import exp
from time import time
import random
from dataclasses import dataclass
from sys import stderr


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
    def __init__(self, blocks, n, m):
        self.blocks = blocks 
        self.n = n
        self.m = m

    @classmethod
    def get_initialized(cls, n, m, k):
        new = cls([], n, m)
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
        return BlockMatrix(self.blocks.copy(), self.n, self.m)

    def __repr__(self):
        return '\n'.join(' ' .join(str(self[i,j]) for j in range(self.m)) for i in range(self.n))



def matrix_distance(matrix, block_matrix, n, m):
    return 1 / (n * m) * sum((matrix[i][j] - block_matrix[i, j])**2 for j in range(m) for i in range(n))



def change_value(block_matrix, k):
    matrix_copy = block_matrix.copy()
    block = random.choice(matrix_copy.blocks)
    block.value = random.choice(list(filter(lambda val: val != block.value, VALUES)))
    return matrix_copy


def merge_blocks(block_matrix, k):
    for b1 in block_matrix.blocks:
        for b2 in block_matrix.blocks:
            if b1.start_column == b2.start_column and b1.width == b2.width:
                start_row = min(b1.start_row, b2.start_row)
                new_block = Block(start_row, b1.start_column, b1.width, b1.height+b2.height, b1.value)

                return BlockMatrix(list(filter(lambda b: b != b1 and b != b2, block_matrix.blocks)) + [new_block], block_matrix.n, block_matrix.m)
            elif b1.start_row == b2.start_row and b1.height == b2.height:
                start_column = min(b1.start_column, b2.start_column)
                new_block = Block(b1.start_row, start_column, b1.width+b2.width, b1.height, b1.value)
                return BlockMatrix(list(filter(lambda b: b != b1 and b != b2, block_matrix.blocks)) + [new_block], block_matrix.n, block_matrix.m)

    return block_matrix


def split_blocks(block_matrix, k):
    matrix_copy = block_matrix.copy()

    for b in block_matrix.blocks:
        if b.width > 2*k:
            split_point = k + random.randrange(0, 2)
            b1 = Block(b.start_row, b.start_column, split_point, b.height, b.value)
            b2 = Block(b.start_row+split_point, b.start_column, b.width-split_point, b.height, b.value)

            return BlockMatrix(list(filter(lambda block: block != b, block_matrix.blocks)) + [b1, b2], block_matrix.n, block_matrix.m)

        elif b.height > 2*k:
            split_point = k + random.randrange(0, 2)
            b1 = Block(b.start_row, b.start_column, b.width, split_point, b.value)
            b2 = Block(b.start_row, b.start_column+split_point, b.width, b.height-split_point, b.value)

            return BlockMatrix(list(filter(lambda block: block != b, block_matrix.blocks)) + [b1, b2], block_matrix.n, block_matrix.m)

    return matrix_copy


def merge_and_split(block_matrix, k):
    return split_blocks(merge_blocks(block_matrix, k), k)


def tweak(block_matrix, k):
    return random.choice([change_value, merge_and_split])(block_matrix, k)



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

        if quality_r <= quality_s or random.random() < exp((quality_s - quality_r) / t):
            s = r
            quality_s = quality_r

        t *= DECREASE_FACTOR

        if quality_s < quality_best:
            # if abs(quality_s - quality_best)/quality_best < 0.000000001:
            #     return quality_best
            best = s
            quality_best = quality_s

    return best, quality_best


def main():
    time, n, m, k = list(map(int, input().split()))
    matrix = [list(map(int, input().split())) for _ in range(n)]

    result, quality = simulated_annealing(time, matrix, n, m, k)
    print(quality)
    print(result, file=stderr)



if __name__ == "__main__":
    main()
