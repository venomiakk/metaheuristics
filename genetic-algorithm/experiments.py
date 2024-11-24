from algorithm import GeneticAlgorithm
from data import items
from plots import bar_plot_values, bar_plot_weights
from logs import save_results_txt


def experiment5(crossover_m):
    """
    @brief  Wplyw metody krzyzowania
    """
    population_size = 20
    no_of_generations = 100
    backpack_capacity = 6404180
    stop_condition = 0
    selection_method = 0
    crossover_method = crossover_m
    results_to_store = 3
    chance_for_mutation = 0.7
    chance_for_crossover = 0.7

    best_values = []
    avg_values = []
    worst_values = []
    best_weights = []
    avg_weights = []
    worst_weights = []
    all_populations = []

    # loop
    for _ in range(0, 10):
        ga1 = GeneticAlgorithm(items, population_size, no_of_generations=no_of_generations,
                               backpack_capacity=backpack_capacity,
                               stop_condition=stop_condition, selection_method=selection_method,
                               crossover_method=crossover_method, results_to_store=results_to_store,
                               chance_for_mutation=chance_for_mutation, chance_for_crossover=chance_for_crossover)
        population1 = ga1.run()
        all_populations.append(population1)
        run_values = [individual.value for individual in population1]
        best_values.append(max(run_values))
        avg_values.append(sum(run_values) / len(run_values))
        worst_values.append(min(run_values))
        run_weights = [individual.weight for individual in population1]
        best_weights.append(max(run_weights))
        avg_weights.append(sum(run_weights) / len(run_weights))
        worst_weights.append(min(run_weights))

    bar_plot_values(best_values, avg_values, worst_values)
    bar_plot_weights(best_weights, avg_weights, worst_weights)
    with open('experiments/ex5.txt', 'a') as file:
        file.write(f"\nWplyw metody krzyzowania\n\n")
    save_results_txt('experiments/ex5.txt', all_populations, population_size, no_of_generations=no_of_generations,
                     backpack_capacity=backpack_capacity,
                     stop_condition=stop_condition, selection_method=selection_method,
                     crossover_method=crossover_method, results_to_store=results_to_store,
                     chance_for_mutation=chance_for_mutation, chance_for_crossover=chance_for_crossover)


def experiment4(selection_m):
    """
    @brief  Wplyw metody selekcji
    """
    population_size = 20
    no_of_generations = 100
    backpack_capacity = 6404180
    stop_condition = 0
    selection_method = selection_m
    crossover_method = 0
    results_to_store = 3
    chance_for_mutation = 0.7
    chance_for_crossover = 0.7

    best_values = []
    avg_values = []
    worst_values = []
    best_weights = []
    avg_weights = []
    worst_weights = []
    all_populations = []

    # loop
    for _ in range(0, 10):
        ga1 = GeneticAlgorithm(items, population_size, no_of_generations=no_of_generations,
                               backpack_capacity=backpack_capacity,
                               stop_condition=stop_condition, selection_method=selection_method,
                               crossover_method=crossover_method, results_to_store=results_to_store,
                               chance_for_mutation=chance_for_mutation, chance_for_crossover=chance_for_crossover)
        population1 = ga1.run()
        all_populations.append(population1)
        run_values = [individual.value for individual in population1]
        best_values.append(max(run_values))
        avg_values.append(sum(run_values) / len(run_values))
        worst_values.append(min(run_values))
        run_weights = [individual.weight for individual in population1]
        best_weights.append(max(run_weights))
        avg_weights.append(sum(run_weights) / len(run_weights))
        worst_weights.append(min(run_weights))

    bar_plot_values(best_values, avg_values, worst_values)
    bar_plot_weights(best_weights, avg_weights, worst_weights)
    with open('experiments/ex4.txt', 'a') as file:
        file.write(f"\nWplyw metody selekcji\n\n")
    save_results_txt('experiments/ex4.txt', all_populations, population_size, no_of_generations=no_of_generations,
                     backpack_capacity=backpack_capacity,
                     stop_condition=stop_condition, selection_method=selection_method,
                     crossover_method=crossover_method, results_to_store=results_to_store,
                     chance_for_mutation=chance_for_mutation, chance_for_crossover=chance_for_crossover)


def experiment3(pop_size):
    """
    @brief  Wplyw wielkosci populacji
    """
    population_size = pop_size
    no_of_generations = 100
    backpack_capacity = 6404180
    stop_condition = 0
    selection_method = 0
    crossover_method = 0
    results_to_store = 3
    chance_for_mutation = 0.7
    chance_for_crossover = 0.7

    best_values = []
    avg_values = []
    worst_values = []
    best_weights = []
    avg_weights = []
    worst_weights = []
    all_populations = []

    # loop
    for _ in range(0, 10):
        ga1 = GeneticAlgorithm(items, population_size, no_of_generations=no_of_generations,
                               backpack_capacity=backpack_capacity,
                               stop_condition=stop_condition, selection_method=selection_method,
                               crossover_method=crossover_method, results_to_store=results_to_store,
                               chance_for_mutation=chance_for_mutation, chance_for_crossover=chance_for_crossover)
        population1 = ga1.run()
        all_populations.append(population1)
        run_values = [individual.value for individual in population1]
        best_values.append(max(run_values))
        avg_values.append(sum(run_values) / len(run_values))
        worst_values.append(min(run_values))
        run_weights = [individual.weight for individual in population1]
        best_weights.append(max(run_weights))
        avg_weights.append(sum(run_weights) / len(run_weights))
        worst_weights.append(min(run_weights))

    bar_plot_values(best_values, avg_values, worst_values)
    bar_plot_weights(best_weights, avg_weights, worst_weights)
    with open('experiments/ex3.txt', 'a') as file:
        file.write(f"\nWplyw wielkosci populacji\n\n")
    save_results_txt('experiments/ex3.txt', all_populations, population_size, no_of_generations=no_of_generations,
                     backpack_capacity=backpack_capacity,
                     stop_condition=stop_condition, selection_method=selection_method,
                     crossover_method=crossover_method, results_to_store=results_to_store,
                     chance_for_mutation=chance_for_mutation, chance_for_crossover=chance_for_crossover)


def experiment2(mutation_probability):
    """
    @brief  Wplyw prawdopodobienstwa mutacji
    """
    population_size = 20
    no_of_generations = 100
    backpack_capacity = 6404180
    stop_condition = 0
    selection_method = 0
    crossover_method = 0
    results_to_store = 3
    chance_for_mutation = mutation_probability
    chance_for_crossover = 0.7

    best_values = []
    avg_values = []
    worst_values = []
    best_weights = []
    avg_weights = []
    worst_weights = []
    all_populations = []

    # loop
    for _ in range(0, 10):
        ga1 = GeneticAlgorithm(items, population_size, no_of_generations=no_of_generations,
                               backpack_capacity=backpack_capacity,
                               stop_condition=stop_condition, selection_method=selection_method,
                               crossover_method=crossover_method, results_to_store=results_to_store,
                               chance_for_mutation=chance_for_mutation, chance_for_crossover=chance_for_crossover)
        population1 = ga1.run()
        all_populations.append(population1)
        run_values = [individual.value for individual in population1]
        best_values.append(max(run_values))
        avg_values.append(sum(run_values) / len(run_values))
        worst_values.append(min(run_values))
        run_weights = [individual.weight for individual in population1]
        best_weights.append(max(run_weights))
        avg_weights.append(sum(run_weights) / len(run_weights))
        worst_weights.append(min(run_weights))

    bar_plot_values(best_values, avg_values, worst_values)
    bar_plot_weights(best_weights, avg_weights, worst_weights)
    with open('experiments/ex2.txt', 'a') as file:
        file.write(f"\nWplyw prawdopodobienstwa mutacji\n\n")
    save_results_txt('experiments/ex2.txt', all_populations, population_size, no_of_generations=no_of_generations,
                     backpack_capacity=backpack_capacity,
                     stop_condition=stop_condition, selection_method=selection_method,
                     crossover_method=crossover_method, results_to_store=results_to_store,
                     chance_for_mutation=chance_for_mutation, chance_for_crossover=chance_for_crossover)


def experiment1(crossover_probability):
    """
    @brief  Wplyw prawdopodobienstwa krzyzowania
    """
    population_size = 20
    no_of_generations = 100
    backpack_capacity = 6404180
    stop_condition = 0
    selection_method = 0
    crossover_method = 0
    results_to_store = 3
    chance_for_mutation = 0.7
    chance_for_crossover = crossover_probability

    best_values = []
    avg_values = []
    worst_values = []
    best_weights = []
    avg_weights = []
    worst_weights = []
    all_populations = []

    # loop
    for _ in range(0, 10):
        ga1 = GeneticAlgorithm(items, population_size, no_of_generations=no_of_generations,
                               backpack_capacity=backpack_capacity,
                               stop_condition=stop_condition, selection_method=selection_method,
                               crossover_method=crossover_method, results_to_store=results_to_store,
                               chance_for_mutation=chance_for_mutation, chance_for_crossover=chance_for_crossover)
        population1 = ga1.run()
        all_populations.append(population1)
        run_values = [individual.value for individual in population1]
        best_values.append(max(run_values))
        avg_values.append(sum(run_values) / len(run_values))
        worst_values.append(min(run_values))
        run_weights = [individual.weight for individual in population1]
        best_weights.append(max(run_weights))
        avg_weights.append(sum(run_weights) / len(run_weights))
        worst_weights.append(min(run_weights))

    bar_plot_values(best_values, avg_values, worst_values)
    bar_plot_weights(best_weights, avg_weights, worst_weights)
    with open('experiments/ex1.txt', 'a') as file:
        file.write(f"\nWplyw prawdopodobienstwa krzyzowania\n\n")
    save_results_txt('experiments/ex1.txt', all_populations, population_size, no_of_generations=no_of_generations,
                     backpack_capacity=backpack_capacity,
                     stop_condition=stop_condition, selection_method=selection_method,
                     crossover_method=crossover_method, results_to_store=results_to_store,
                     chance_for_mutation=chance_for_mutation, chance_for_crossover=chance_for_crossover)

def test():
    """
    @brief  Wplyw prawdopodobienstwa krzyzowania
    """
    # data:
    population_size = 20
    no_of_generations = 100
    backpack_capacity = 6404180
    stop_condition = 0
    selection_method = 0
    crossover_method = 0
    results_to_store = 3
    chance_for_mutation = 0.7
    chance_for_crossover = 0.7

    best_values = []
    avg_values = []
    worst_values = []
    best_weights = []
    avg_weights = []
    worst_weights = []
    all_populations = []

    # loop
    for _ in range(0, 10):
        ga1 = GeneticAlgorithm(items, population_size, no_of_generations=no_of_generations,
                               backpack_capacity=backpack_capacity,
                               stop_condition=stop_condition, selection_method=selection_method,
                               crossover_method=crossover_method, results_to_store=results_to_store,
                               chance_for_mutation=chance_for_mutation, chance_for_crossover=chance_for_crossover)
        population1 = ga1.run()
        all_populations.append(population1)
        run_values = [individual.value for individual in population1]
        best_values.append(max(run_values))
        avg_values.append(sum(run_values) / len(run_values))
        worst_values.append(min(run_values))
        run_weights = [individual.weight for individual in population1]
        best_weights.append(max(run_weights))
        avg_weights.append(sum(run_weights) / len(run_weights))
        worst_weights.append(min(run_weights))

    bar_plot_values(best_values, avg_values, worst_values)
    bar_plot_weights(best_weights, avg_weights, worst_weights)
    save_results_txt('results/test.txt', all_populations, population_size, no_of_generations=no_of_generations,
                     backpack_capacity=backpack_capacity,
                     stop_condition=stop_condition, selection_method=selection_method,
                     crossover_method=crossover_method, results_to_store=results_to_store,
                     chance_for_mutation=chance_for_mutation, chance_for_crossover=chance_for_crossover)
