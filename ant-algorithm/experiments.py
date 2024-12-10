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
        aa = AntAlgorithm(file_path=filepath, num_ants=antsnum)
        best_ant, best_dst = aa.run()
        ants.append(best_ant)
        best_dsts.append(best_dst)
        # plot_ant_path(best_ant, best_dst, filepath=filepath)
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
        # plot_ant_path(best_ant, best_dst, filepath=filepath)
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
        aa = AntAlgorithm(file_path=filepath, alpha=alpha)
        best_ant, best_dst = aa.run()
        ants.append(best_ant)
        best_dsts.append(best_dst)
        # plot_ant_path(best_ant, best_dst, filepath=filepath)
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


def experminet4(beta, file=0):
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
        aa = AntAlgorithm(file_path=filepath, beta=beta)
        best_ant, best_dst = aa.run()
        ants.append(best_ant)
        best_dsts.append(best_dst)
        # plot_ant_path(best_ant, best_dst, filepath=filepath)
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
        # plot_ant_path(best_ant, best_dst, filepath=filepath)
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
        # plot_ant_path(best_ant, best_dst, filepath=filepath)
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
    pass


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
        aa = AntAlgorithm(file_path=filepath)
        best_ant, best_dst = aa.run()
        ants.append(best_ant)
        best_dsts.append(best_dst)
        # plot_ant_path(best_ant, best_dst, filepath=filepath)
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
    print("ex")
    test(file=1)
