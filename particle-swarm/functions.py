import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def ackley(x, y):
    # -5 <= x,y <= 5
    # min: f(0,0) = 0

    term1 = -20.0 * np.exp(-0.2 * (np.sqrt(0.5 * (x ** 2 + y ** 2))))
    term2 = -np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
    return term1 + term2 + np.e + 20


def himmelblaus(x, y):
    # -5 <= x,y <= 5
    # min:
    # f(3.0, 2.0) = 0
    # f(-2.805118, 3.131312) = 0
    # f(-3.779310, -3.283186) = 0
    # f(3.584428, -1.848126) = 0

    term1 = (x ** 2 + y - 11) ** 2
    term2 = (x + y ** 2 - 7) ** 2
    return term1 + term2


def plot2d_ackley():
    # Generating data
    x = np.linspace(-5, 5, 400)
    y = np.linspace(-5, 5, 400)
    x, y = np.meshgrid(x, y)
    z = ackley(x, y)

    # Creating the contour plot
    plt.contourf(x, y, z, cmap='viridis', levels=20)
    plt.colorbar()

    # Adding labels
    plt.xlabel('X')
    plt.ylabel('Y')

    plt.show()


def plot2d_himmelblaus():
    # Generating data
    x = np.linspace(-5, 5, 400)
    y = np.linspace(-5, 5, 400)
    X, Y = np.meshgrid(x, y)
    Z = himmelblaus(X, Y)

    # Creating the contour plot
    plt.contourf(X, Y, Z, cmap='viridis', levels=100, norm=plt.Normalize(vmin=0, vmax=100))
    plt.colorbar()

    # contour = plt.contourf(
    #     X, Y, Z,
    #     levels=np.logspace(-2, 5, 150),  # Logarytmiczne poziomy
    #     cmap='viridis',  # Mapa kolorów
    #     norm=LogNorm(vmin=1e-1, vmax=1e3)  # Logarytmiczna normalizacja
    # )
    # cbar = plt.colorbar(contour)
    # cbar.set_ticks([1, 10, 100, 1000])  # Określenie pozycji
    # cbar.set_ticklabels(['0', '10', '100', '1000'])  # Określenie etykiet

    # Adding labels
    plt.xlabel('X')
    plt.ylabel('Y')

    # plt.scatter([3, -2.805118, -3.779310, 3.584428],
    #             [2, 3.131312, -3.283186, -1.848126],
    #             color='red', label='Minima', zorder=5)
    # plt.legend()

    plt.show()


if __name__ == '__main__':
    plot2d_ackley()
    plot2d_himmelblaus()
