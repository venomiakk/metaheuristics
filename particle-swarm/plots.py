import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from functions import ackley, himmelblaus


def plot_ackley(title=True, particles=None, best_particle=None, iteration=None, no_particles=None, inertia=None,
                cognition=None, social=None):
    x = np.linspace(-5, 5, 400)
    y = np.linspace(-5, 5, 400)
    x, y = np.meshgrid(x, y)
    z = ackley(x, y)
    plt.contourf(x, y, z, cmap='viridis', levels=20)
    plt.colorbar()
    plt.xlabel('X')
    plt.ylabel('Y')
    px = []
    py = []
    if particles:
        for particle in particles:
            px.append(particle.x)
            py.append(particle.y)
        plt.scatter(px, py, color='#b52828', label='Cząstki')
        plt.legend()
    if best_particle:
        plt.scatter(best_particle.x, best_particle.y, color='#05e6f2', label='Najlepsza cząstka')
        plt.legend()
    if title:
        plt.title(
            f"Ackley, iteracje: {iteration}, cząstki: {no_particles}, inercja: {inertia}, \n"
            f"współczynnik poznawczy: {cognition}, współczynnik społeczny: {social}")
    plt.show()
    plt.close()


def plot_himmelblaus(title=True, particles=None, best_particle=None, iteration=None, no_particles=None, inertia=None,
                     cognition=None, social=None):
    # Generating data
    x = np.linspace(-5, 5, 400)
    y = np.linspace(-5, 5, 400)
    X, Y = np.meshgrid(x, y)
    Z = himmelblaus(X, Y)

    plt.contourf(X, Y, Z, cmap='viridis', levels=100, norm=plt.Normalize(vmin=0, vmax=100))
    plt.colorbar()

    plt.xlabel('X')
    plt.ylabel('Y')

    px = []
    py = []
    if particles:
        for particle in particles:
            px.append(particle.x)
            py.append(particle.y)
        plt.scatter(px, py, color='#b52828', label='Cząstki')
        plt.legend()
    if best_particle:
        plt.scatter(best_particle.x, best_particle.y, color='#05e6f2', label='Najlepsza cząstka')
        plt.legend()
    if title:
        plt.title(
            f"Ackley, iteracje: {iteration}, cząstki: {no_particles}, inercja: {inertia}, \n"
            f"współczynnik poznawczy: {cognition}, współczynnik społeczny: {social}")
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_ackley()
    plot_himmelblaus()
