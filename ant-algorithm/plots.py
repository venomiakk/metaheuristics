import matplotlib.pyplot as plt


def get_coords(filepath='data/A-n32-k5.txt'):
    data = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.split()
            index = int(parts[0])
            x = int(parts[1])
            y = int(parts[2])
            data.append((index, x, y))
    indices, x_coords, y_coords = zip(*data)
    return indices, x_coords, y_coords


def plot_ant_path(ant, dst, filepath='data/A-n32-k5.txt'):
    indices, x_coords, y_coords = get_coords(filepath)
    plt.scatter(x_coords, y_coords)
    for i, txt in enumerate(indices):
        plt.annotate(txt, (x_coords[i], y_coords[i]))

    path_x = [x_coords[attraction - 1] for attraction in ant.visited_attractions]
    path_y = [y_coords[attraction - 1] for attraction in ant.visited_attractions]
    start_x = path_x[0]
    start_y = path_y[0]
    start_index = ant.visited_attractions[0]
    plt.scatter(start_x, start_y, color='deepskyblue', s=100, label=f'Start: {start_index}')
    plt.plot(path_x, path_y, color='orchid', marker='o')

    plt.title(f'Trasa najlepszej mrówki')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.plot([], [], ' ', label=f'Dystans: {round(dst, 2):.2f}')
    plt.legend(bbox_to_anchor=(1., 1.), frameon=False, fontsize=8)

    plt.tight_layout()
    plt.show()


def plot_all_ants_paths(ants, dsts, filepath='data/A-n32-k5.txt'):
    indices, x_coords, y_coords = get_coords(filepath)
    plt.scatter(x_coords, y_coords)
    for i, txt in enumerate(indices):
        plt.annotate(txt, (x_coords[i], y_coords[i]))

    for i, ant in enumerate(ants):
        path_x = [x_coords[attraction - 1] for attraction in ant.visited_attractions]
        path_y = [y_coords[attraction - 1] for attraction in ant.visited_attractions]
        plt.plot(path_x, path_y, marker='o', label=f'Start {ant.visited_attractions[0]}\n'
                                                   f'Dystans: {round(dsts[i], 2):.2f}')


    plt.title(f'Trasy najlepszych mrówek dla kolejnych uruchomień')
    plt.xlabel('X')
    plt.ylabel('Y')
    legend = plt.legend(bbox_to_anchor=(1., 1.), frameon=False, fontsize=8)
    legend.set_title("Kolejne mrówki")

    plt.tight_layout()
    plt.show()


def plot_linear(bests, avgs, worsts):
    runs = [str(i) for i in range(1, len(bests) + 1)]
    int_runs = list(range(len(bests)))

    plt.plot(runs, worsts, label='Najgorszy', color='red', marker='o')
    plt.plot(runs, avgs, label='Średni', color='blue', marker='o')
    plt.plot(runs, bests, label='Najlepszy', color='green', marker='o')
    for i in range(len(bests)):
        plt.annotate(f'{bests[i]:.2f}', (int_runs[i], bests[i]), textcoords="offset points", xytext=(0, 8),
                     ha='center')
    for i in range(len(avgs)):
        plt.annotate(f'{avgs[i]:.2f}', (int_runs[i], avgs[i]), textcoords="offset points", xytext=(0, 8), ha='center')
    for i in range(len(worsts)):
        plt.annotate(f'{worsts[i]:.2f}', (int_runs[i], worsts[i]), textcoords="offset points", xytext=(0, 8),
                     ha='center')

    plt.ylim(min(bests) - 100, max(worsts) + 100)
    plt.margins(x=0.1)
    plt.title('Wyniki dla badanych parametrów')
    plt.xlabel('Uruchomienia algorytmu')
    plt.ylabel('Pokonany dystans (niższa=lepsza)')
    legend = plt.legend(bbox_to_anchor=(1., 1.), frameon=False, fontsize=9)
    legend.set_title("Wynik")
    plt.grid(True, linestyle='--', alpha=0.8, linewidth=1.5, axis='x')
    plt.grid(True, linestyle='--', alpha=0.6, linewidth=0.8, axis='y')

    plt.tight_layout()
    plt.show()


def plot_bars(bests, avgs, worsts):
    runs = [str(i) for i in range(1, len(bests) + 1)]
    int_runs = list(range(len(bests)))

    plt.bar(runs, worsts, color='plum', edgecolor='black', label='Najgorszy')
    plt.bar(runs, avgs, color='violet', edgecolor='black', label='Średni')
    plt.bar(runs, bests, color='mediumslateblue', edgecolor='black', label='Najlepszy')

    for i in range(len(bests)):
        plt.text(int_runs[i], worsts[i] + 0.05, f'{worsts[i]:.2f}', ha='center', va='bottom')
        plt.text(int_runs[i], avgs[i] + 0.05, f'{avgs[i]:.2f}', ha='center', va='bottom')
        plt.text(int_runs[i], bests[i] + 0.05, f'{bests[i]:.2f}', ha='center', va='bottom')

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylim(min(bests)-100, max(worsts)+100)
    plt.title('Wyniki dla badanych parametrów')
    plt.xlabel('Uruchomienia algorytmu')
    plt.ylabel('Pokonany dystans (mniej=lepiej)')
    legend = plt.legend(bbox_to_anchor=(1., 1.), frameon=False, fontsize=9)
    legend.set_title("Wynik")

    plt.tight_layout()
    plt.show()
