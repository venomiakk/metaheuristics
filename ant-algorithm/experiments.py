from algorithm import AntAlgorithm
from plots import plot_ant_path, plot_all_ants_paths, plot_linear, plot_bars

num_of_iter_in_experiment = 5


def experiment1(antsnum, file=0):
    print(f'Eksperyment 1: wplyw liczebnosci mrowek, mnoznik={antsnum}')
    filepath = 'data/A-n32-k5.txt'
    if file != 0:
        filepath = 'data/A-n80-k10.txt'
    bests = []
    avgs = []
    worsts = []
    ants = []
    best_dsts = []
    for i in range(num_of_iter_in_experiment):
        aa = AntAlgorithm(file_path=filepath, num_ants=antsnum, num_of_iterations=5)
        best_ant, best_dst = aa.run()
        ants.append(best_ant)
        best_dsts.append(best_dst)
        plot_ant_path(best_ant, best_dst, filepath=filepath)
        best, avg, worst = aa.get_all_distances_stats_from_colony()
        bests.append(round(best, 2))
        avgs.append(round(avg, 2))
        worsts.append(round(worst, 2))
        print(f"{i + 1}. best ant {best_ant.visited_attractions}, dst {round(best_dst, 2)}")
    print("distances:")
    print(f'bests: {bests}\navgs: {avgs}\nworsts: {worsts}')
    plot_all_ants_paths(ants, best_dsts, filepath=filepath)
    plot_bars(bests, avgs, worsts)
    plot_linear(bests, avgs, worsts)


def experiment2(rand_attraction_prob, file=0):
    print(f'Eksperyment 2: Prawdopodobienstwo wyboru losowej atrakcji: {rand_attraction_prob}')
    filepath = 'data/A-n32-k5.txt'
    if file != 0:
        filepath = 'data/A-n80-k10.txt'
    bests = []
    avgs = []
    worsts = []
    ants = []
    best_dsts = []
    for i in range(num_of_iter_in_experiment):
        aa = AntAlgorithm(file_path=filepath, random_attraction_probability=rand_attraction_prob)
        best_ant, best_dst = aa.run()
        ants.append(best_ant)
        best_dsts.append(best_dst)
        plot_ant_path(best_ant, best_dst, filepath=filepath)
        best, avg, worst = aa.get_all_distances_stats_from_colony()
        bests.append(round(best, 2))
        avgs.append(round(avg, 2))
        worsts.append(round(worst, 2))
        print(f"{i + 1}. best ant {best_ant.visited_attractions}, dst {round(best_dst, 2)}")
    print("distances:")
    print(f'bests: {bests}\navgs: {avgs}\nworsts: {worsts}')
    plot_all_ants_paths(ants, best_dsts, filepath=filepath)
    plot_bars(bests, avgs, worsts)
    plot_linear(bests, avgs, worsts)


def experiment3(alpha, file=0):
    print(f'Eksperymrnt 3: Wplyw wagi feromonow (alfa): {alpha}')
    filepath = 'data/A-n32-k5.txt'
    if file != 0:
        filepath = 'data/A-n80-k10.txt'
    bests = []
    avgs = []
    worsts = []
    ants = []
    best_dsts = []
    for i in range(num_of_iter_in_experiment):
        aa = AntAlgorithm(file_path=filepath, alpha=alpha, beta=1)
        best_ant, best_dst = aa.run()
        ants.append(best_ant)
        best_dsts.append(best_dst)
        plot_ant_path(best_ant, best_dst, filepath=filepath)
        best, avg, worst = aa.get_all_distances_stats_from_colony()
        bests.append(round(best, 2))
        avgs.append(round(avg, 2))
        worsts.append(round(worst, 2))
        print(f"{i + 1}. best ant {best_ant.visited_attractions}, dst {round(best_dst, 2)}")
    print("distances:")
    print(f'bests: {bests}\navgs: {avgs}\nworsts: {worsts}')
    plot_all_ants_paths(ants, best_dsts, filepath=filepath)
    plot_bars(bests, avgs, worsts)
    plot_linear(bests, avgs, worsts)


def experiment4(beta, file=0):
    print(f'Eksperyment 4: Wplyw wagi metaheurystyki (beta): {beta}')
    filepath = 'data/A-n32-k5.txt'
    if file != 0:
        filepath = 'data/A-n80-k10.txt'
    bests = []
    avgs = []
    worsts = []
    ants = []
    best_dsts = []
    for i in range(num_of_iter_in_experiment):
        aa = AntAlgorithm(file_path=filepath, beta=beta, alpha=1)
        best_ant, best_dst = aa.run()
        ants.append(best_ant)
        best_dsts.append(best_dst)
        plot_ant_path(best_ant, best_dst, filepath=filepath)
        best, avg, worst = aa.get_all_distances_stats_from_colony()
        bests.append(round(best, 2))
        avgs.append(round(avg, 2))
        worsts.append(round(worst, 2))
        print(f"{i + 1}. best ant {best_ant.visited_attractions}, dst {round(best_dst, 2)}")
    print("distances:")
    print(f'bests: {bests}\navgs: {avgs}\nworsts: {worsts}')
    plot_all_ants_paths(ants, best_dsts, filepath=filepath)
    plot_bars(bests, avgs, worsts)
    plot_linear(bests, avgs, worsts)


def experiment5(iters, file=0):
    print(f"Eksperyment 5: Wplyw liczby iteracji: {iters}")
    filepath = 'data/A-n32-k5.txt'
    if file != 0:
        filepath = 'data/A-n80-k10.txt'
    bests = []
    avgs = []
    worsts = []
    ants = []
    best_dsts = []
    for i in range(num_of_iter_in_experiment):
        aa = AntAlgorithm(file_path=filepath, num_of_iterations=iters)
        best_ant, best_dst = aa.run()
        ants.append(best_ant)
        best_dsts.append(best_dst)
        plot_ant_path(best_ant, best_dst, filepath=filepath)
        best, avg, worst = aa.get_all_distances_stats_from_colony()
        bests.append(round(best, 2))
        avgs.append(round(avg, 2))
        worsts.append(round(worst, 2))
        print(f"{i + 1}. best ant {best_ant.visited_attractions}, dst {round(best_dst, 2)}")
    print("distances:")
    print(f'bests: {bests}\navgs: {avgs}\nworsts: {worsts}')
    plot_all_ants_paths(ants, best_dsts, filepath=filepath)
    plot_bars(bests, avgs, worsts)
    plot_linear(bests, avgs, worsts)


def experiment6(evaporation, file=0):
    print(f"Wplyw wpolczynnika wyparowywania: {evaporation}")
    filepath = 'data/A-n32-k5.txt'
    if file != 0:
        filepath = 'data/A-n80-k10.txt'
    bests = []
    avgs = []
    worsts = []
    ants = []
    best_dsts = []
    for i in range(num_of_iter_in_experiment):
        aa = AntAlgorithm(file_path=filepath, evaporation=evaporation)
        best_ant, best_dst = aa.run()
        ants.append(best_ant)
        best_dsts.append(best_dst)
        plot_ant_path(best_ant, best_dst, filepath=filepath)
        best, avg, worst = aa.get_all_distances_stats_from_colony()
        bests.append(round(best, 2))
        avgs.append(round(avg, 2))
        worsts.append(round(worst, 2))
        print(f"{i + 1}. best ant {best_ant.visited_attractions}, dst {round(best_dst, 2)}")
    print("distances:")
    print(f'bests: {bests}\navgs: {avgs}\nworsts: {worsts}')
    plot_all_ants_paths(ants, best_dsts, filepath=filepath)
    plot_bars(bests, avgs, worsts)
    plot_linear(bests, avgs, worsts)


def run_all_experiments():
    print("experiment1: param=1, file=0")
    experiment1(1, 0)
    print("experiment1: param=3, file=0")
    experiment1(3, 0)
    print("experiment1: param=5, file=0")
    experiment1(5, 0)
    print("experiment1: param=1, file=1")
    experiment1(1, 1)
    print("experiment1: param=3, file=1")
    experiment1(3, 1)
    print("experiment1: param=5, file=1")
    experiment1(5, 1)

    print("experiment2: param 0.1, file=0")
    experiment2(0.1, file=0)
    print("experiment2: param 0.5, file=0")
    experiment2(0.5, file=0)
    print("experiment2: param 0.9, file=0")
    experiment2(0.9, file=0)
    print("experiment2: param 0.1, file=1")
    experiment2(0.1, file=1)
    print("experiment2: param 0.5, file=1")
    experiment2(0.5, file=1)
    print("experiment2: param 0.9, file=1")
    experiment2(0.9, file=1)

    print("experiment3: param=1, file=0")
    experiment3(1, 0)
    print("experiment3: param=3, file=0")
    experiment3(3, 0)
    print("experiment3: param=5, file=0")
    experiment3(5, 0)
    print("experiment3: param=1, file=1")
    experiment3(1, 1)
    print("experiment3: param=3, file=1")
    experiment3(3, 1)
    print("experiment3: param=5, file=1")
    experiment3(5, 1)

    print("experiment4: param=1, file=0")
    experiment4(1, 0)
    print("experiment4: param=3, file=0")
    experiment4(3, 0)
    print("experiment4: param=5, file=0")
    experiment4(5, 0)
    print("experiment4: param=1, file=1")
    experiment4(1, 1)
    print("experiment4: param=3, file=1")
    experiment4(3, 1)
    print("experiment4: param=5, file=1")
    experiment4(5, 1)

    print("experiment5: param=5, file=0")
    experiment5(5, 0)
    print("experiment5: param=30, file=0")
    experiment5(30, 0)
    print("experiment5: param=100, file=0")
    experiment5(100, 0)
    print("experiment5: param=5, file=1")
    experiment5(5, 1)
    print("experiment5: param=30, file=1")
    experiment5(30, 1)
    print("experiment5: param=100, file=1")
    experiment5(100, 1)

    print("experiment6: param=0.1, file=0")
    experiment6(0.1, 0)
    print("experiment6: param=0.5, file=0")
    experiment6(0.5, 0)
    print("experiment6: param=0.9, file=0")
    experiment6(0.9, 0)
    print("experiment6: param=0.1, file=1")
    experiment6(0.1, 1)
    print("experiment6: param=0.5, file=1")
    experiment6(0.5, 1)
    print("experiment6: param=0.9, file=1")
    experiment6(0.9, 1)


def test(file=0):
    filepath = 'data/A-n32-k5.txt'
    if file != 0:
        filepath = 'data/A-n80-k10.txt'
    bests = []
    avgs = []
    worsts = []
    ants = []
    best_dsts = []
    for i in range(num_of_iter_in_experiment):
        aa = AntAlgorithm(file_path=filepath, num_of_iterations=100, alpha=2, beta=2, random_attraction_probability=0.1,
                          num_ants=1, evaporation=0.5)
        best_ant, best_dst = aa.run()
        ants.append(best_ant)
        best_dsts.append(best_dst)
        plot_ant_path(best_ant, best_dst, filepath=filepath)
        best, avg, worst = aa.get_all_distances_stats_from_colony()
        bests.append(round(best, 2))
        avgs.append(round(avg, 2))
        worsts.append(round(worst, 2))
        print(f"{i + 1}. best ant {best_ant.visited_attractions}, dst {round(best_dst, 2)}")
    print("distances:")
    print(f'bests: {bests}\navgs: {avgs}\nworsts: {worsts}')
    plot_all_ants_paths(ants, best_dsts, filepath=filepath)
    plot_bars(bests, avgs, worsts)
    plot_linear(bests, avgs, worsts)


def experiment7(alpha, beta, file=0):
    print(f"Porownanie alfy i bety")
    filepath = 'data/A-n32-k5.txt'
    if file != 0:
        filepath = 'data/A-n80-k10.txt'
    bests = []
    avgs = []
    worsts = []
    ants = []
    best_dsts = []
    for i in range(num_of_iter_in_experiment):
        aa = AntAlgorithm(file_path=filepath, alpha=alpha, beta=beta)
        best_ant, best_dst = aa.run()
        ants.append(best_ant)
        best_dsts.append(best_dst)
        plot_ant_path(best_ant, best_dst, filepath=filepath)
        best, avg, worst = aa.get_all_distances_stats_from_colony()
        bests.append(round(best, 2))
        avgs.append(round(avg, 2))
        worsts.append(round(worst, 2))
        print(f"{i + 1}. best ant {best_ant.visited_attractions}, dst {round(best_dst, 2)}")
    print("distances:")
    print(f'bests: {bests}\navgs: {avgs}\nworsts: {worsts}')
    plot_all_ants_paths(ants, best_dsts, filepath=filepath)
    plot_bars(bests, avgs, worsts)
    plot_linear(bests, avgs, worsts)


if __name__ == '__main__':
    experiment7(alpha=2, beta=0, file=0)
    experiment7(alpha=0, beta=2, file=0)

    experiment7(alpha=2, beta=0, file=1)
    experiment7(alpha=0, beta=2, file=1)
