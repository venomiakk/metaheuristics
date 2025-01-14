import numpy as np


def get_distances_matrix(filepath='data/A-n32-k5.txt'):
    data = []

    with open(filepath, 'r') as file:
        for line in file:
            parts = line.split()
            index = int(parts[0])
            x = int(parts[1])
            y = int(parts[2])
            data.append((index, x, y))

    distances_matix = []
    for i in data:
        xi = i[1]
        yi = i[2]
        ij_distances = []

        for j in data:
            xj = j[1]
            yj = j[2]
            ij_distances.append(np.sqrt(((xj - xi) ** 2) + ((yj - yi) ** 2)))

        distances_matix.append(ij_distances)
    return distances_matix


if __name__ == '__main__':
    print('readdata')
