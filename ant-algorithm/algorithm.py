import random

from readdata import get_distances_matrix
from ant import Ant
import numpy as np


class AntAlgorithm:
    def __init__(self, num_ants=1, num_of_iterations=10, alpha=0.5, beta=0.5, evaporation=0.5,
                 random_attraction_probability=0.0, file_path='data/A-n32-k5.txt', stop_condition=0,
                 no_changed_items=10):
        self.distances = get_distances_matrix(filepath=file_path)
        self.traces = self.__generate_traces()
        self.num_of_attractions = len(self.distances)

        self.num_ants_multiplier = num_ants
        self.ants_colony = self.__generate_colony()

        self.num_of_iterations = num_of_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_factor = evaporation
        self.random_attraction_probability = random_attraction_probability

        self.all_distances_accross_iters = []

        self.stop_cond = stop_condition
        self.no_changed_items = no_changed_items

    def run(self):
        last_bests = []
        # 1. generate traces - constructor
        # 2. generate first colony - constructor

        best_ant = self.ants_colony[0]
        best_dst = float('inf')

        # main loop
        iteration = 0
        while True:
            iteration += 1

            for ant in self.ants_colony:
                self.__visit_attractions(ant)
            self.__update_pheromones()

            # choose best ant
            for ant in self.ants_colony:
                dst = ant.get_travelled_distance(self.distances)
                self.all_distances_accross_iters.append(dst)
                if dst < best_dst:
                    best_ant = ant
                    best_dst = dst

            # checking for stop
            if self.stop_cond == 0:
                if iteration >= self.num_of_iterations:
                    return best_ant, best_dst
            else:
                last_bests.append(best_dst)
                if len(last_bests) > self.no_changed_items:
                    last_bests.pop(0)
                    avg_diff = np.mean(np.abs(np.diff(last_bests)))
                    if avg_diff < 1:
                        print(f'Iterations: {iteration}')
                        return best_ant, best_dst

            # generate colony for next iteration
            self.ants_colony = self.__generate_colony()

    def __visit_attractions(self, ant):
        for i in range(self.num_of_attractions):
            random_chance = random.random()
            if random_chance <= self.random_attraction_probability:
                ant.visit_random_attraction()
            else:
                if len(ant.visited_attractions) <= 0:
                    ant.visit_random_attraction()
                else:
                    used_indexes, result_probabilities = ant.calculate_attractions_probabilities(self.traces,
                                                                                                 self.distances,
                                                                                                 self.alpha, self.beta)
                    ant.visit_attraction_roulette_selection(used_indexes, result_probabilities)

    def __generate_traces(self):
        return [[1 for _ in i] for i in self.distances]

    def __generate_colony(self):
        num_of_ants = round(self.num_of_attractions * self.num_ants_multiplier)
        return [Ant(self.num_of_attractions) for _ in range(num_of_ants)]

    def __update_pheromones(self):
        for x in range(self.num_of_attractions):
            for y in range(self.num_of_attractions):
                self.traces[x][y] *= self.evaporation_factor
                self.traces[y][x] *= self.evaporation_factor

        for ant in self.ants_colony:
            travelled_distance = ant.get_travelled_distance(self.distances)
            for k in range(1, len(ant.visited_attractions)):
                # !!
                i = ant.visited_attractions[k - 1] - 1
                # !!
                j = ant.visited_attractions[k] - 1
                self.traces[i][j] += 1.0 / travelled_distance
                self.traces[j][i] += 1.0 / travelled_distance

    def get_all_distances_stats_from_colony(self):
        best = min(self.all_distances_accross_iters)
        worst = max(self.all_distances_accross_iters)
        avg = sum(self.all_distances_accross_iters) / len(self.all_distances_accross_iters)
        return best, avg, worst
