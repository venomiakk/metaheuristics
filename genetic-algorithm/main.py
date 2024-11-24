import experiments
from algorithm import GeneticAlgorithm
from data import items


def interface():
    population_size = 20
    no_of_generations = 100
    backpack_capacity = 6404180
    stop_condition = 0
    selection_method = 0
    crossover_method = 0
    results_to_store = 3
    chance_for_mutation = 0.7
    chance_for_crossover = 0.7
    print("Algorytm genetyczny dla problemu plecakowego\n")
    pop_size = int(input("Podaj wielkosc populacji: "))
    stop_condition = int(input("\nWybierz warunek stopu, 0 - iteracje, 1 - stagnacja: "))
    if stop_condition == 0:
        no_of_generations = int(input("\nPodaj ilosc generacji: "))
    else:
        results_to_store = int(input("\nPodaj ilosc zapisywanych wynikow: "))
    selection_method = int(input("Podaj metode selekcji, 0 - ruletkowa, 1 - rankingowa: "))
    crossover_method = int(input("\nPodaj metode krzyzowania, 0 - jednopunktowe, 1 - rownomierne: "))
    chance_for_mutation = float(input("\nPodaj szanse na mutacje od 0.0 do 1.0: "))
    chance_for_crossover = float(input("\nPodaj szanse na krzyzowanie od 0.0 do 1.0: "))

    ga = GeneticAlgorithm(items, population_size, no_of_generations, stop_condition=stop_condition,
                          selection_method=selection_method, crossover_method=crossover_method,
                          results_to_store=results_to_store, chance_for_mutation=chance_for_mutation,
                          chance_for_crossover=chance_for_crossover)
    ga.run()


def set_run_all_experiments():
    # szansa na krzyzowanie
    experiments.experiment1(0.1)
    experiments.experiment1(0.5)
    experiments.experiment1(1)

    # szansa na mutacje
    experiments.experiment2(0.1)
    experiments.experiment2(0.5)
    experiments.experiment2(1)

    # wielkosc populacji
    experiments.experiment3(10)
    experiments.experiment3(20)
    experiments.experiment3(30)

    # metody selekcji
    experiments.experiment4(0)
    experiments.experiment4(1)

    # metody krzyzowania
    experiments.experiment5(0)
    experiments.experiment5(1)

    # TODO czy jeszcze szansa na krzyzowanie z druga metoda?


if __name__ == '__main__':
    # interface()
    #
    experiments.experiment1(0.1)

    # experiments.test()

# Maximum value: 13692887
# Maximum weight: 6397822
# Expected chromosome: [0,0,0,0,1,1,0,1,0,0,1,1,0,1,0,1,0,0,0,0,1,1,0,1,0,1]
