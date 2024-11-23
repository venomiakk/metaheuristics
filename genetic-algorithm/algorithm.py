import random


class Individual:
    def __init__(self, chromosome_binary_list):
        self.chromosome = chromosome_binary_list
        self.weight = 0  # value of fitness function
        self.value = 0


class geneticAlgorithm:
    def __init__(self, dicts_list_binary_data, population_size, backpack_capacity=6404180):
        self.backpack_capacity = backpack_capacity
        self.items = dicts_list_binary_data
        self.individual_size = len(self.items)
        self.population_size = population_size
        self.population = self.__generate_starting_population()

    def run(self):
        # print(self.population[0].chromosome)
        # self.__fitness(self.population[0])
        for i in self.population:
            self.__fitness(i)
        # self.__roulette_selection()
        self.__rank_selection()
        # print(len(self.population))
        # print(self.population_size)

    def __generate_starting_population(self):
        population = []
        for _ in range(0, self.population_size):
            population.append(Individual([random.randint(0, 1) for _ in range(self.individual_size)]))
        return population

    def __fitness(self, individual):
        weight = 0
        value = 0
        for index, gene in enumerate(individual.chromosome):
            if gene == 1:
                weight += self.items[index]["weight"]
                value += self.items[index]["value"]
        if weight <= self.backpack_capacity:
            individual.weight = weight
            individual.value = value
        # print(individual.weight, individual.value)

    def __roulette_selection(self):
        # print('roulette')
        fitness_sum = sum(individual.weight for individual in self.population)
        # if fitness_sum == 0: ...
        probabilities = [i.weight / fitness_sum for i in self.population]
        cumulative_probability = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
        # print(probabilities)
        # print(cumulative_probability)
        selected_individuals = []
        for _ in range(self.population_size):
            r = random.random()
            for i, individual in enumerate(self.population):
                if r <= cumulative_probability[i]:
                    selected_individuals.append(individual)
                    break

        self.population = selected_individuals

    def __rank_selection(self):
        # print('rank selection')
        sorted_population = sorted(self.population, key=lambda individual: individual.weight, reverse=True)

        rank_sum = sum(range(1, self.population_size + 1))  # sum of an arithmetic series
        probabilities = [(self.population_size - rank) / rank_sum for rank in range(self.population_size)]
        cumulative_probability = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]

        # Baker's linear ranking selection
        # sp = 1.0  # selection pressure, typically between 1 and 2
        # rank_sum = self.population_size * (self.population_size + 1) / 2  # sum of an arithmetic series
        # probabilities = [
        #     (2 - sp) / self.population_size + 2 * rank * (sp - 1) / (self.population_size * (self.population_size - 1))
        #     for rank in range(self.population_size)]
        # cumulative_probability = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]

        # print(rank_sum)
        # print(probabilities)
        # print(cumulative_probability)

        selected_individuals = []
        for _ in range(self.population_size):
            r = random.random()
            for i, individual in enumerate(sorted_population):
                if r <= cumulative_probability[i]:
                    selected_individuals.append(individual)
                    break

        self.population = selected_individuals
