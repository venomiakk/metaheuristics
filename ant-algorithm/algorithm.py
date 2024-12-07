from readdata import get_distances_matrix
from ant import Ant


class AntAlgorithm:
    def __init__(self, num_ants):
        self.distances = get_distances_matrix()
        self.traces = self.__generate_traces()
        self.num_of_attractions = len(self.distances)

        self.num_ants_multiplier = num_ants
        self.ants_colony = self.__generate_colony()

        # TODO add to arguments
        self.alpha = 0.5
        self.beta = 0.5
        self.evaporation_factor = 0.5

    def run(self):
        ant = Ant(len(self.distances))
        # print(ant.visited_attractions)
        # print(ant.possible_to_visit)
        ant.visit_random_attraction()
        ant.visit_random_attraction()
        ant.visit_random_attraction()
        ant.visit_random_attraction()
        ant.visit_random_attraction()
        ant.visit_random_attraction()
        ant.visit_random_attraction()

        # print(ant.visited_attractions)
        # print(ant.possible_to_visit)

        used_indexes, result_probabilities = ant.calculate_attractions_probabilities(self.traces, self.distances,
                                                                                     self.alpha, self.beta)

        ant.visit_attraction_roulette_selection(used_indexes, result_probabilities)
        self.__update_pheromones()

    def __generate_traces(self):
        return [[1 for _ in i] for i in self.distances]

    def __generate_colony(self):
        num_of_ants = round(self.num_of_attractions * self.num_ants_multiplier)
        return [Ant(self.num_of_attractions) for _ in range(num_of_ants)]

    def __update_pheromones(self):
        for x in range(self.num_of_attractions):
            for y in range(self.num_of_attractions):
                self.traces[x][y] *= self.evaporation_factor

        for ant in self.ants_colony:
            travelled_distance = ant.get_travelled_distance(self.distances)
            for k in range(1, len(ant.visited_attractions)):
                i = ant.visited_attractions[k - 1] - 1
                j = ant.visited_attractions[k - 1] - 1
                self.traces[i][j] += 1.0 / travelled_distance
                self.traces[j][i] += 1.0 / travelled_distance

    def __get_best_ant(self, previous_best_ant):
        best_ant = previous_best_ant
        for ant in self.ants_colony:
            travelled_dst = ant.get_travelled_distance()
            if travelled_dst < best_ant.get_travelled_distance:
                best_ant = ant

        return best_ant
