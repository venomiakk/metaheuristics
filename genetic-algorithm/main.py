from algorithm import GeneticAlgorithm
from data import items
from datetime import datetime


def select_highest_value_individual(individuals):
    return max(individuals, key=lambda individual: individual.value)


def select_highest_weight_individual(individuals):
    return max(individuals, key=lambda individual: individual.weight)


def find_phrases_in_file(file_path, phrase):
    results = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            start = 0
            while (start := line.find(phrase, start)) != -1:
                start += len(phrase)
                end = line.find(',', start)
                if end != -1:
                    extracted_text = line[start:end].strip()
                    results.append([int(extracted_text), line_number])
                start = end if end != -1 else start
    results = sorted(results, key=lambda x: x[0])
    return results


def save_results_txt(filename, population_size, no_of_generations, backpack_capacity,
                     stop_condition, selection_method, crossover_method, results_to_store,
                     chance_for_mutation, run_iterations):
    with open(filename, 'a') as file1:
        file1.write(f'\n{datetime.now()}\n\n'
                    f'params:\npop_size: {population_size}, no_of_generations: {no_of_generations}, backpack_capacity: {backpack_capacity}\n'
                    f'stop_condition: {stop_condition} - 0: generations, 1: stagnation\n'
                    f'selection_method: {selection_method} - 0: roulette, 1: ranked\n'
                    f'crossover_method: {crossover_method} - 0: single point, 1: masked random\n'
                    f'chance_for_mutation: {chance_for_mutation}\n'
                    f'results_to_store: {results_to_store} - for stagnation stop condition, difference between last best weights\n')
    for i in range(run_iterations):

        ga = GeneticAlgorithm(items, population_size, selection_method=selection_method,
                              no_of_generations=no_of_generations, crossover_method=crossover_method,
                              stop_condition=stop_condition, results_to_store=results_to_store,
                              chance_for_mutation=chance_for_mutation, backpack_capacity=backpack_capacity)
        result = ga.run()
        all_weights = []
        all_values = []
        for j in result:
            all_weights.append(j.weight)
            all_values.append(j.value)
        bestValue = select_highest_value_individual(result)
        bestWeight = select_highest_weight_individual(result)
        stored_weights = []
        for k in ga.stored_results:
            stored_weights.append(k)

        expectedBestValue = 13692887
        expectedBestWeight = 6397822
        with open(filename, 'a') as file:
            file.write(f'\n--------------Iteration {i + 1}--------------------\n'
                       f'Generations: {ga.final_iterations}\n'
                       f'Stored weights: {stored_weights}\n'
                       f'All weights: {all_weights}\n'
                       f'All values: {all_values}\n'
                       f'Best by weight: {bestWeight}\n'
                       f'Best (by value) {bestWeight.chromosome} value: {bestWeight.value}, weight: {bestWeight.weight}, to backpack_capacity: {backpack_capacity - bestWeight.weight}\n'
                       f'Best by value:  {bestValue}\n'
                       f'Best (by value) {bestValue.chromosome} value: {bestValue.value}, weight: {bestValue.weight}, to backpack_capacity: {backpack_capacity - bestValue.weight}\n'
                       f'\nExpected        [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1]'
                       f' value: {expectedBestValue}, weight: {expectedBestWeight}\n'
                       f'\nCompare best by value:\n'
                       f'v_value_diff: {expectedBestValue - bestValue.value}, v_weight_diff: {expectedBestWeight - bestValue.weight},\n'
                       f'v_result_to_backpack_capacity: {backpack_capacity - bestValue.weight},\n'
                       f'\nCompare best by weight:\n'
                       f'w_value_diff: {expectedBestValue - bestWeight.value}, w_weight_diff: {expectedBestWeight - bestWeight.weight},\n'
                       f'w_result_to_backpack_capacity: {backpack_capacity - bestWeight.weight},\n'
                       f'\nvalue - weight best, value: {bestValue.value - bestWeight.value}, weight: {bestValue.weight - bestWeight.weight}')
            if bestValue.weight >= expectedBestWeight or bestValue.value >= expectedBestValue:
                file.write(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')

    res1 = find_phrases_in_file(filename, 'v_result_to_backpack_capacity:')
    res2 = find_phrases_in_file(filename, 'v_weight_diff:')
    res3 = find_phrases_in_file(filename, 'v_value_diff:')
    res4 = find_phrases_in_file(filename, 'w_result_to_backpack_capacity:')
    res5 = find_phrases_in_file(filename, 'w_weight_diff:')
    res6 = find_phrases_in_file(filename, 'w_value_diff:')
    with open(filename, 'a') as f2:
        f2.write(f'\n\n-------------BEST RESULTS------------'
                 f'\n[[result_to_backpack_capacity,line_number]] by value\n'
                 f'{res1}\n'
                 f'[[weight_diff,line_number]]\n'
                 f'{res2}\n'
                 f'[[value_diff,line_number]]\n'
                 f'{res3}\n'
                 f'\n[[result_to_backpack_capacity,line_number]] by weight\n'
                 f'{res4}\n'
                 f'[[weight_diff,line_number]]\n'
                 f'{res5}\n'
                 f'[[value_diff,line_number]]\n'
                 f'{res6}\n')


if __name__ == '__main__':
    save_results_txt('results/r1.txt', 50, no_of_generations=100, backpack_capacity=6404180,
                     stop_condition=0, selection_method=0, crossover_method=0, results_to_store=3,
                     chance_for_mutation=0.7, run_iterations=1)

# Maximum value: 13692887
# Maximum weight: 6397822
# Expected chromosome: [0,0,0,0,1,1,0,1,0,0,1,1,0,1,0,1,0,0,0,0,1,1,0,1,0,1]

# TODO co zrobic gdy mamy wiele osobnikow z fitness = 0
# * rodzic moze byc rodzicem wiecej niz raz
# ? czy podczas selekcji powinien moc byc wybrany wiecej niz raz?
# * dodać selekcje rankingową jako druga metoda
