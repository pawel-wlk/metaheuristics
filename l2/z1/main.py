from math import cos, pi, sqrt, exp
from time import time
from random import random, gauss

INIT_TEMP = 10**10
DECREASE_FACTOR = 0.99


def salomon(x):
    norm = sqrt(sum(xi**2 for xi in x))
    return 1 - cos(2 * pi * norm) + 0.1 * norm


def tweak(x):
    return [xi * gauss(1, 0.1) for xi in x]


def simulated_annealing(init_solution, max_time, tweak, quality):
    t = INIT_TEMP

    s = init_solution
    best = s
    quality_best = quality(best)

    start = time()
    while time() - start < max_time:
        r = tweak(s)
        quality_s = quality(s)
        quality_r = quality(r)

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


def main():
    time, *x = list(map(float, input().split()))
    best = simulated_annealing(x, time, tweak, salomon)
    print(*best, salomon(best))

if __name__ == "__main__":
    main()