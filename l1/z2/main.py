from time import time
from sys import stderr
from random import random


class TSP:
    MAX_TABU_LEN = 64

    def __init__(self, cities):
        self.cities = cities
        self.cities_count = len(cities)

    def evaluate(self, path):
        cost = 0
        last_city = path[0]
        for city in path[1:]:
            cost += cities[last_city][city]
            last_city = city
        return cost

    def greedy_solution(self):
        visited = [0]
        i = 0
        while len(visited) != self.cities_count:
            i, _ = min((city for city in enumerate(
                self.cities[i]) if city[0] not in visited), key=lambda x: x[1])
            visited.append(i)

        solution = visited + [0]
        return solution, self.evaluate(solution)

    def tabu_search(self, max_time):
        # s = [0] + shuffled(list(range(1, self.cities_count))) + [0]
        s, _ = self.greedy_solution()
        best = s
        tabu_list = []
        tabu_list.append(s)

        start = time()
        while time() - start < max_time:
            if len(tabu_list) > self.MAX_TABU_LEN:
                tabu_list.pop(0)

            r = s
            for i in range(1, self.cities_count-1):
                for j in range(1, self.cities_count-1):
                    if j == i:
                        continue
                    w = s.copy()
                    w[i], w[j] = w[j], w[i]
                    if w not in tabu_list and (self.evaluate(w) < self.evaluate(r) or r in tabu_list):
                        r = w

            if r not in tabu_list:
                s = r
                tabu_list.append(s)
            if self.evaluate(s) < self.evaluate(best):
                best = s

        return best, self.evaluate(best)


if __name__ == "__main__":
    first_line = input()
    max_time, cities_count = [int(num) for num in first_line.split()]
    cities = [[int(num) for num in input().split()]
              for _ in range(cities_count)]

    tsp = TSP(cities)
    best_path, cost = tsp.tabu_search(max_time)
    print(cost)
    print(' '.join(str(city) for city in best_path), file=stderr)
