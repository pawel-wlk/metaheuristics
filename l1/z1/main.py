from math import cos, prod, sqrt
from typing import Tuple, Callable
from time import time
from random import uniform

DELTA = 0.01
NEIGHBOURS_COUNT = 8

vector = Tuple[float, float, float, float]
testfunc = Callable[[vector], float]


def norm(x: vector) -> float:
    return sqrt(sum(xi**2 for xi in x))


def happy_cat(x: vector) -> float:
    return ((norm(x)**2-4)**2)**(1/8) + (norm(x)**2 / 2 + sum(x))/4 + 1/2


def griewank(x: vector) -> float:
    return 1 + sum(xi**2/4000 for xi in x) - prod(cos(xi / sqrt(i))
                                                  for i, xi in enumerate(x, 1))


def new_point():
    return tuple(uniform(-1, 1) for _ in range(4))


def tweak(x: vector, func: testfunc) -> vector:
    neighbours = (tuple(xi + uniform(-DELTA, DELTA) for xi in x)
                  for _ in range(NEIGHBOURS_COUNT))
    return min(neighbours, key=func)


def hill_climb(func: testfunc, max_time: int):
    s = new_point()
    best = s
    start_time = time()
    while time() - start_time < max_time:
        s = tweak(s, func)
        if s == best:
            s = new_point()
        if func(s) < func(best):
            best = s

    return best


if __name__ == "__main__":
    max_time, func_num = list(map(int, input().split()))
    func = happy_cat if func_num == 0 else griewank

    result = hill_climb(func, max_time)

    print(' '.join(str(xi) for xi in result), func(result))
