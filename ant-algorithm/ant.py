import random


class Ant:
    def __init__(self, num_of_attractions):
        self.visited_attractions = []
        self.possible_to_visit = [i + 1 for i in range(num_of_attractions)]

    def visit_random_attraction(self):
        self.visited_attractions.append(random.choice(self.possible_to_visit))
        self.possible_to_visit = [attraction for attraction in self.possible_to_visit if
                                  attraction not in self.visited_attractions]

    def calculate_attractions_probabilities(self, traces, distances, alpha, beta):
        current_attraction = self.visited_attractions[-1]
        used_indexes = []
        used_pobabilties = []
        probabilities_sum = 0

        for attraction in self.possible_to_visit:
            used_indexes.append(attraction)
            # !!
            pheromones = traces[current_attraction - 1][attraction - 1] ** alpha
            # !!
            attractions_dst = distances[current_attraction - 1][attraction - 1]
            if attractions_dst == 0:
                attractions_dst = 1e-10

            heuristics = (1 / attractions_dst) ** beta
            probability = pheromones * heuristics
            probabilities_sum += probability
            used_pobabilties.append(probability)

        result_probabilities = [x / probabilities_sum for x in used_pobabilties]

        return used_indexes, result_probabilities

    def visit_attraction_roulette_selection(self, used_indexes, probabilities):
        intervals = []
        cumulative = 0
        for probability in probabilities:
            cumulative += probability
            intervals.append(cumulative)

        random_value = random.random()
        result = 0
        for index, interval in zip(used_indexes, intervals):
            if random_value < interval:
                result = index
                self.visited_attractions.append(index)
                self.possible_to_visit.remove(index)
                break
            # TODO is there a chance to not choose anything?
        return result

    def get_travelled_distance(self, distances_matrix):
        total_distance = 0
        for i in range(1, len(self.visited_attractions)):
            # !!
            first = self.visited_attractions[i - 1] - 1
            # !!
            second = self.visited_attractions[i] - 1
            total_distance += distances_matrix[first][second]
        return total_distance
