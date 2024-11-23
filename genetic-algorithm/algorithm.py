import random


class Individual:
    def __init__(self, chromosome_binary_list):
        self.chromosome = chromosome_binary_list
        self.weight = 0     # value of fitness function
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
        self.__roulette_selection()

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
        print(individual.weight, individual.value)

    def __roulette_selection(self):
        print('roulette')
        fitness_sum = sum(individual.weight for individual in self.population)
        probabilities = []
        for i in self.population:
            probabilities.append(i.weight / fitness_sum)

        print(probabilities)
        print(fitness_sum)