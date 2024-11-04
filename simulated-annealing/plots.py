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

def plot_f3():
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
    ax.scatter(point_x, point_y, point_z, color='r', s=10)

    # Wyświetlenie wykresu
    plt.show()

def plot_f4():
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
    ax.scatter(point_x, point_y, point_z, color='r', s=10)

    # Wyświetlenie wykresu
    plt.show()

if __name__ == '__main__':
    plot_f4()