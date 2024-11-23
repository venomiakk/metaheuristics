import random


class Individual:
    def __init__(self, chromosome_binary_list):
        # 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25
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
        parents = self.__rank_selection()
        # print(len(new_generation))
        # print(self.population_size)

        # test = self.__crossover_masked_random(parents[0], parents[1])
        test = self.__crossover_single_point(parents[0], parents[1])
        self.__mutation_single_gene(test[0])


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

        return selected_individuals

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

        return selected_individuals

    def __crossover_single_point(self, parent_a, parent_b, point_deviation=4):
        middle_point = int(len(parent_a.chromosome) / 2)
        crossover_point = random.randint(middle_point - point_deviation, middle_point + point_deviation)
        # print(crossover_point)
        ab_child_chromosome = []
        ba_child_chromosome = []
        # print(parent_a.chromosome)
        # print(parent_b.chromosome)
        for index, (a_gene, b_gene) in enumerate(zip(parent_a.chromosome, parent_b.chromosome)):
            if index < crossover_point:
                ab_child_chromosome.append(a_gene)
                ba_child_chromosome.append(b_gene)
            else:
                ab_child_chromosome.append(b_gene)
                ba_child_chromosome.append(a_gene)

        return Individual(ab_child_chromosome), Individual(ba_child_chromosome)

    def __crossover_masked_random(self, parent_a, parent_b, min_crossings=6, max_crossings=15):
        # crossing_points = random.randint(min_crossings, max_crossings)
        # interval = int(len(parent_a.chromosome) / crossing_points) + 1
        # print(crossing_points)
        # print(interval)

        crossing_mask = [random.randint(0, 1) for _ in range(len(parent_a.chromosome))]
        a_child_chromosome = [a_gene if mask_bit == 1 else b_gene for a_gene, b_gene, mask_bit in
                              zip(parent_a.chromosome, parent_b.chromosome, crossing_mask)]
        b_child_chromosome = [b_gene if mask_bit == 1 else a_gene for a_gene, b_gene, mask_bit in
                              zip(parent_a.chromosome, parent_b.chromosome, crossing_mask)]
        # print(parent_a.chromosome)
        # print(parent_b.chromosome)
        # print(crossing_mask)
        # print(a_child_chromosome)
        # print(b_child_chromosome)
        return Individual(a_child_chromosome), Individual(b_child_chromosome)

    def __mutation_single_gene(self, individual, mutation_chance=1):
        # print(individual.chromosome)
        gene_index = random.randint(0, len(individual.chromosome) - 1)
        # print(f'{gene_index}, gene: {individual.chromosome[gene_index]}')
        if random.random() <= mutation_chance:
            # print('mutation')
            individual.chromosome[gene_index] ^= 1  # flip bit

        # print(individual.chromosome)
        # print(f'gene: {individual.chromosome[gene_index]}')
