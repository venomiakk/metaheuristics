from algorithm import funkcja3, funkcja4

import numpy as np
import matplotlib.pyplot as plt

def funkcja(x, y):
    return np.sin(np.sqrt(x**2 + y**2))

def test():
        # Generowanie danych
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = funkcja(X, Y)

    # Rysowanie wykresu
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')

    # Dodanie etykiet
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    # Wyświetlenie wykresu
    plt.show()

def plot_f3(points):
    x = np.linspace(-15, 15, 100)
    y = np.linspace(-15, 15, 100)
    X, Y = np.meshgrid(x, y)
    Z = funkcja3(X, Y)

    # Rysowanie wykresu
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')

    # Dodanie etykiet
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    point_x = 12
    point_y = 12
    point_z = funkcja3(point_x, point_y)
    ax.scatter(point_x, point_y, point_z, color='b', s=10)
    if points != 0:
        for i in points:
            x = i[0]
            y = i[1]
            point_z = funkcja3(x, y)
            if point_z > 1:
                ax.scatter(x, y, point_z, color='r', s=10)
    

    # Wyświetlenie wykresu
    plt.show()

def plot_f4(points = 0):
    x = np.linspace(-3, 12, 100)
    y = np.linspace(4.1, 5.8, 100)
    X, Y = np.meshgrid(x, y)
    Z = funkcja4(X, Y)

    # Rysowanie wykresu
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')

    # Dodanie etykiet
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    point_x = 11.625545 
    point_y = 5.7250444
    point_z = funkcja4(point_x, point_y)
    ax.scatter(point_x, point_y, point_z, color='b', s=10)
    if points != 0:
        for i in points:
            x = i[0]
            y = i[1]
            point_z = funkcja4(x, y)
            if point_z > 1:
                ax.scatter(x, y, point_z, color='r', s=10)

    # Wyświetlenie wykresu
    plt.show()

if __name__ == '__main__':
    plot_f4([[10.625421402360546, 5.62518297494726]])
    plot_f4([[11.627450148431231, 5.625280941034024]])
    plot_f4([[10.124836606863752, 5.62511416723113]])
    plot_f4([[11.626194195323352, 5.424591815159771]])
    plot_f4([[10.625707096299958, 5.725147579688085]])
    plot_f4([[11.624687227089039, 5.625570867314836]])
    plot_f4([[11.625378265624132, 5.624648762610548]])