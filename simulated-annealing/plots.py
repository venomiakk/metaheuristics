from algorithm import funkcja3, funkcja4

import numpy as np
import matplotlib.pyplot as plt


def plot_f3(points=0):
    x = np.linspace(-15, 15, 100)
    y = np.linspace(-15, 15, 100)
    X, Y = np.meshgrid(x, y)
    Z = funkcja3(X, Y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    point_x = 12
    point_y = 12
    point_z = funkcja3(point_x, point_y)
    blue_sc = ax.scatter(point_x, point_y, point_z, color='b', s=10, label='Maksimum globalne')
    if points != 0:
        for i in points:
            x = i[0]
            y = i[1]
            point_z = funkcja3(x, y)
            red_sc = ax.scatter(x, y, point_z, color='r', s=10, label='Wyniki algorytmu')
    

    handles, labels = ax.get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))
    ax.legend(unique_labels.values(), unique_labels.keys())
    plt.show()

def plot_f4(points = 0):
    x = np.linspace(-3, 12, 100)
    y = np.linspace(4.1, 5.8, 100)
    X, Y = np.meshgrid(x, y)
    Z = funkcja4(X, Y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')

    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    point_x = 11.625545 
    point_y = 5.7250444
    point_z = funkcja4(point_x, point_y)
    blue_sc = ax.scatter(point_x, point_y, point_z, color='b', s=10, label='Maksimum globalne')
    if points != 0:
        for i in points:
            x = i[0]
            y = i[1]
            point_z = funkcja4(x, y)
            red_sc = ax.scatter(x, y, point_z, color='r', s=10, label='Wyniki algorytmu')

    handles, labels = ax.get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))
    ax.legend(unique_labels.values(), unique_labels.keys())
    plt.show()

if __name__ == '__main__':
    plot_f3()
    plot_f4()
