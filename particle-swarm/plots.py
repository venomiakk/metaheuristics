import numpy as np
import matplotlib.pyplot as plt
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
            f"Himmelblau, iteracje: {iteration}, cząstki: {no_particles}, inercja: {inertia}, \n"
            f"współczynnik poznawczy: {cognition}, współczynnik społeczny: {social}")
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


def histogram_ackley(particles):
    z = [obj.fitness for obj in particles]

    bins = np.linspace(0, 10, 20)  # Przedziały od 0 do 100 co 10
    counts, edges, bars = plt.hist(z, bins=bins, edgecolor='black', color='skyblue')

    # Dodanie etykiet
    plt.title("Histogram wartości funkcji celu (z)")
    plt.xlabel("Przedziały wartości funkcji celu (z)")
    plt.ylabel("Liczba cząstek")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(edges, rotation=45)

    # Wyświetlenie liczby cząstek nad słupkami
    for count, bar in zip(counts, bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, int(count), ha='center', va='bottom')

    plt.show()


def histogram_himmelblaus(particles):
    #TODO zrobic na sztywno biny, podpisac jako stringi
    z = [obj.fitness for obj in particles]

    # Logarytmiczne biny
    bins = np.logspace(np.log10(1), np.log10(810), 20)
    print(bins)
    # Histogram
    counts, edges, bars = plt.hist(z, bins=bins, edgecolor='black', color='skyblue')

    # Skala logarytmiczna na osi X
    plt.xscale('log')

    # Ustawienie ticków na osi X
    plt.xticks(bins, labels=[f"{int(b)}" for b in bins], rotation=45)

    plt.title("Histogram rozkładu cząstek")
    plt.xlabel("Przedziały wartości funkcji")
    plt.ylabel("Liczba cząstek")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Wyświetlenie liczby cząstek nad słupkami
    for count, bar in zip(counts, bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, int(count), ha='center', va='bottom')

    plt.show()

if __name__ == '__main__':
    plot_ackley()
    plot_himmelblaus()
