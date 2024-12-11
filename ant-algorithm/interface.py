from algorithm import AntAlgorithm
from plots import plot_ant_path


def run_interface():
    iters_num = 10
    no_change_items = 10
    print("Algorytm mrowkowy\n")
    stop = int(input("Podaj warunek stopu (0 - iteracje, 1 - stagnacja): "))
    if stop == 0:
        iters_num = int(input(" Podaj ilosc iteracji: "))
    else:
        no_change_items = int(input(" Podaj ilosc ostatnich wynikow branych pod uwage: "))

    ants_num = int(input("Podaj mnoznik ilosci mrowek: "))
    alpha = float(input("Podaj wage feromonow (alfa): "))
    beta = float(input("Podaj wage metaheurystyki (beta): "))
    evap = float(input("Podaj wspolczynnik wyparowywania (0.0 - 1.0): "))
    rap = float(input("Podaj prawdopodobienstwo wybrania losowej atrakcji (0.0 - 1.0): "))
    file = int(input("Wybierz plik z danymi: (0 - A-n32-k5.txt, 1 - A-n80-k10.txt): "))
    print("\n")
    filepath = 'data/A-n32-k5.txt'
    if file != 0:
        filepath = 'data/A-n80-k10.txt'

    aa = AntAlgorithm(file_path=filepath, num_ants=ants_num, num_of_iterations=iters_num, alpha=alpha, beta=beta,
                      evaporation=evap, random_attraction_probability=rap, no_changed_items=no_change_items,
                      stop_condition=stop)
    best_ant, best_dst = aa.run()

    best, avg, worst = aa.get_all_distances_stats_from_colony()

    print(f"Trasa najlepszej mrowki {best_ant.visited_attractions}\n"
          f"Odleglosci:\n"
          f"Najlepsza: {round(best_dst, 2)}\n"
          f"Srednia: {round(avg, 2)}\n"
          f"Najgorsza: {round(worst, 2)}")
    plot_ant_path(best_ant, best_dst, filepath=filepath)


if __name__ == '__main__':
    run_interface()
