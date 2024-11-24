import random

import numpy as np


def select_highest_value_individual(individuals):
    return max(individuals, key=lambda individual: individual.value)


def select_highest_weight_individual(individuals):
    return max(individuals, key=lambda individual: individual.weight)


class Individual:
    def __init__(self, chromosome_binary_list):
        # 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25
        self.chromosome = chromosome_binary_list
        self.weight = 0  # value of fitness function
        self.value = 0


class GeneticAlgorithm:
    def __init__(self, dicts_list_binary_data, population_size, no_of_generations=100, backpack_capacity=6404180,
                 stop_condition=0, selection_method=0, crossover_method=0, results_to_store=2, chance_for_mutation=0.7,
                 chance_for_crossover=0.7):
        self.backpack_capacity = backpack_capacity
        self.items = dicts_list_binary_data
        self.individual_size = len(self.items)
        self.population_size = population_size + 1 if population_size % 2 != 0 else population_size
        self.no_of_generations = no_of_generations
        self.stop_condition = stop_condition
        self.selection_method = selection_method
        self.crossover_method = crossover_method
        self.chance_for_mutation = chance_for_mutation
        self.chance_for_crossover = chance_for_crossover

        self.final_iterations = 0
        self.results_to_store = results_to_store
        self.stored_results = []

    def run(self):
        population = self.__generate_starting_population()
        [self.__fitness(individual) for individual in population]
        starting_fitness_sum = sum(individual.weight for individual in population)

        while starting_fitness_sum == 0:
            population = self.__generate_starting_population()
            [self.__fitness(individual) for individual in population]
            starting_fitness_sum = sum(individual.weight for individual in population)

        generations_iter = 0

        while True:
            generations_iter += 1
            # Choosing parents
            if self.selection_method == 0:
                parents = self.__roulette_selection(population)
            else:
                parents = self.__rank_selection(population)

            # Creating new generation
            new_generation = []
            for i in range(0, len(parents), 2):
                # Creating offspring
                if self.crossover_method == 0:
                    a_child, b_child = self.__crossover_single_point(parents[i], parents[i + 1])
                else:
                    a_child, b_child = self.__crossover_masked_random(parents[i], parents[i + 1])

                # Mutation of offspring
                self.__mutation_single_gene(a_child)
                self.__mutation_single_gene(b_child)

                # Calculating fitenss of offspring
                self.__fitness(a_child)
                self.__fitness(b_child)
                new_generation.extend([a_child, b_child])

            population = new_generation
            #TODO best by value or best by weight?
            best_individual = select_highest_value_individual(population)

            if self.stop_condition == 0:
                if generations_iter >= self.no_of_generations:
                    break
            else:
                if len(self.stored_results) >= self.results_to_store:
                    self.stored_results.pop(0)
                self.stored_results.append(best_individual.weight)
                if len(self.stored_results) == self.results_to_store:
                    avg_diff = np.mean(np.abs(np.diff(self.stored_results)))
                    if avg_diff < 1:
                        break

        self.final_iterations = generations_iter
        expectedBestValue = 13692887
        expectedBestWeight = 6397822
        # print(f'\nGenerations: {generations_iter}\n'
        #       f'Best by value: {best_individual.chromosome}\n'
        #       f'Value: {best_individual.value}, Weight: {best_individual.weight}, '
        #       f'{best_individual.weight / self.backpack_capacity * 100}% of backpack\n'
        #       f'Diff to expected best values:\n'
        #       f'value_diff: {expectedBestValue - best_individual.value}, '
        #       f'{best_individual.value / expectedBestValue * 100}%, '
        #       f'weight_diff: {expectedBestWeight - best_individual.weight}, '
        #       f'{best_individual.weight / expectedBestWeight * 100}%')
        return population

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

    def __roulette_selection(self, population):
        # print('roulette')
        fitness_sum = sum(individual.weight for individual in population)
        if fitness_sum == 0:
            return population
        probabilities = [i.weight / fitness_sum for i in population]
        cumulative_probability = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
        # print(probabilities)
        # print(cumulative_probability)
        selected_individuals = []
        for _ in range(self.population_size):
            r = random.random()
            for i, individual in enumerate(population):
                if r <= cumulative_probability[i]:
                    selected_individuals.append(individual)
                    break

        return selected_individuals

    def __rank_selection(self, population):
        # print('rank selection')
        sorted_population = sorted(population, key=lambda individual: individual.weight, reverse=True)

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
        if random.random() <= self.chance_for_crossover:
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
        else:
            return parent_a, parent_b

    def __crossover_masked_random(self, parent_a, parent_b, min_crossings=6, max_crossings=15):
        if random.random() <= self.chance_for_crossover:
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
        else:
            return parent_a, parent_b

    def __mutation_single_gene(self, individual):
        # print(individual.chromosome)
        gene_index = random.randint(0, len(individual.chromosome) - 1)
        # print(f'{gene_index}, gene: {individual.chromosome[gene_index]}')
        if random.random() <= self.chance_for_mutation:
            # print('mutation')
            individual.chromosome[gene_index] ^= 1  # flip bit

        # print(individual.chromosome)
        # print(f'gene: {individual.chromosome[gene_index]}')
