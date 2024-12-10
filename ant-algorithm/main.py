from ant import Ant
from readdata import get_distances_matrix
from algorithm import AntAlgorithm
from plots import plot_ant_path

filepath = 'data/A-n32-k5.txt'

if __name__ == '__main__':
    aa = AntAlgorithm(stop_condition=1)

    best_ant, best_dst = aa.run()
    print("MAIN:")
    print(best_ant.visited_attractions)
    print(best_dst)
    plot_ant_path(best_ant, best_dst)
