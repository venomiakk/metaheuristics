from algorithm import AntAlgorithm
from plots import plot_ant_path, plot_all_ants_paths, plot_linear, plot_bars


def test():
    file1 = 'data/A-n32-k5.txt'
    file2 = 'data/A-n80-k10.txt'
    bests = []
    avgs = []
    worsts = []
    ants = []
    best_dsts = []
    for i in range(5):
        aa = AntAlgorithm(1, 10, file_path=file2)
        best_ant, best_dst = aa.run()
        ants.append(best_ant)
        best_dsts.append(best_dst)
        plot_ant_path(best_ant, best_dst, filepath=file2)
        best, avg, worst = aa.get_all_distances_stats_from_colony()
        bests.append(best)
        avgs.append(avg)
        worsts.append(worst)
    print(bests, '\n', avgs, '\n', worsts)
    plot_all_ants_paths(ants, best_dsts, filepath=file2)
    plot_bars(bests, avgs, worsts)
    plot_linear(bests, avgs, worsts)


if __name__ == '__main__':
    print("ex")
    test()
