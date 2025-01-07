import numpy as np
import matplotlib.pyplot as plt
from functions import ackley, himmelblaus
from matplotlib.ticker import MaxNLocator


def plot_ackley(title=True, particles=None, best_particle=None, iteration=None, no_particles=None, inertia=None,
                cognition=None, social=None, file=None):
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
    if file:
        plt.savefig(f'{file}.png')
    plt.show()
    plt.close()


def plot_himmelblaus(title=True, particles=None, best_particle=None, iteration=None, no_particles=None, inertia=None,
                     cognition=None, social=None, file=None):
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
            f"Himmelblau, iteracje: {iteration}, cząstki: {no_particles}, inercja: {inertia}, \n"
            f"współczynnik poznawczy: {cognition}, współczynnik społeczny: {social}")
    if file:
        plt.savefig(f'{file}.png')
    plt.show()
    plt.close()


def heatmap(particles):
    x = [obj.x for obj in particles]
    y = [obj.y for obj in particles]
    counts, xedges, yedges, im = plt.hist2d(x, y, bins=100, cmap='afmhot')

    # Dodanie osi i legendy
    plt.colorbar(im, label="Liczba cząstek")
    plt.title("Heatmapa liczby cząstek")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


def histogram_ackley(particles, file=None):
    z = [obj.fitness for obj in particles]
    bins = np.linspace(0, 10, 20)  # Przedziały od 0 do 100 co 10
    counts, edges, bars = plt.hist(z, bins=bins, edgecolor='black', color='skyblue')
    plt.title("Rozkład cząstek")
    plt.xlabel("Przedziały wartości funkcji")
    plt.ylabel("Liczba cząstek")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(edges, rotation=45)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    for count, bar in zip(counts, bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, int(count), ha='center', va='bottom')
    plt.tight_layout()
    if file:
        plt.savefig(f'{file}.png')
    plt.show()
    plt.close()


def histogram_himmelblaus(particles, file=None):
    z = [obj.fitness for obj in particles]
    bins = [0.0, 0.5, 1.0, 1.5, 2.0, 4.0, 8.0, 11.0, 16.0, 23.0, 33.0, 48.0, 68.0, 139.0, 197.0, 281.0, 400.0, 569.0,
            810.0, np.inf]
    counts, bin_edges = np.histogram(z, bins=bins)
    bin_counts = list(counts)
    categories = [str(num) for num in bins]
    categories = categories[:-1]
    bars = plt.bar(categories, bin_counts, width=1.0, align='edge', edgecolor='black', color='skyblue')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.title("Rozkład cząstek")
    plt.xlabel("Przedziały wartości funkcji")
    plt.ylabel("Liczba cząstek")
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')
    plt.tight_layout()
    if file:
        plt.savefig(f'{file}.png')
    plt.show()
    plt.close()


if __name__ == '__main__':
    plot_ackley()
    plot_himmelblaus()
